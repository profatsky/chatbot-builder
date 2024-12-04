import os
import shutil
from typing import Optional

from src.projects.dependencies.repositories_dependencies import ProjectRepositoryDI
from src.projects.schemas import (
    ProjectReadSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
    ProjectToGenerateCodeReadSchema,
)
from src.projects.exceptions import ProjectNotFound, NoPermissionForProject, ProjectsLimitExceeded


class ProjectService:
    def __init__(self, project_repository: ProjectRepositoryDI):
        self._project_repository = project_repository

    async def create_project(
            self,
            user_id: int,
            project_data: ProjectCreateSchema,
    ) -> ProjectReadSchema:
        project_count = await self._project_repository.count_projects(user_id)
        if project_count >= 5:
            raise ProjectsLimitExceeded

        project = await self._project_repository.create_project(
            user_id=user_id,
            project_data=project_data,
        )
        return project

    async def get_projects(self, user_id: int) -> list[ProjectReadSchema]:
        projects = await self._project_repository.get_projects(user_id)
        return projects

    async def check_access_and_get_project_to_generate_code(
            self,
            user_id: int,
            project_id: int,
    ) -> Optional[ProjectToGenerateCodeReadSchema]:
        project = await self._project_repository.get_project_to_generate_code(project_id)
        if project is None:
            raise ProjectNotFound

        if project.user_id != user_id:
            raise NoPermissionForProject

        return project

    async def check_access_and_get_project(
            self,
            user_id: int,
            project_id: int,
    ) -> ProjectReadSchema:
        project = await self._project_repository.get_project(project_id)
        if project is None:
            raise ProjectNotFound

        if project.user_id != user_id:
            raise NoPermissionForProject

        return project

    async def check_access_and_update_project(
            self,
            user_id: int,
            project_id: int,
            project_data: ProjectUpdateSchema,
    ) -> Optional[ProjectReadSchema]:
        _ = await self.check_access_and_get_project(
            user_id=user_id,
            project_id=project_id,
        )
        project = await self._project_repository.update_project(
            project_id=project_id,
            project_data=project_data,
        )
        return project

    async def delete_project(
            self,
            user_id: int,
            project_id: int,
    ):
        _ = await self.check_access_and_get_project(
            user_id=user_id,
            project_id=project_id,
        )

        media_dir_path = os.path.join(
            'src', 'media', 'users', str(user_id), 'projects', str(project_id)
        )
        if os.path.exists(media_dir_path):
            shutil.rmtree(media_dir_path)

        await self._project_repository.delete_project(project_id)
