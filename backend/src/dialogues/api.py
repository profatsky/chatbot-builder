from fastapi import APIRouter, status, HTTPException

from src.auth.dependencies.jwt_dependencies import AuthJWTDI
from src.dialogues.dependencies.services_dependencies import DialogueServiceDI
from src.dialogues.exceptions import DialoguesLimitExceededError, DialogueNotFoundError
from src.dialogues.schemas import DialogueCreateSchema, DialogueReadSchema, TriggerUpdateSchema
from src.projects.exceptions import ProjectNotFoundError, NoPermissionForProjectError

router = APIRouter(
    prefix='/projects/{project_id}/dialogues',
    tags=['dialogues'],
)


@router.post(
    '',
    response_model=DialogueReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_dialogue(
        project_id: int,
        dialogue_data: DialogueCreateSchema,
        auth_jwt: AuthJWTDI,
        dialogue_service: DialogueServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        dialogue = await dialogue_service.check_access_and_create_dialogue(
            user_id=user_id,
            project_id=project_id,
            dialogue_data=dialogue_data,
        )
    except ProjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project does not exist',
        )
    except NoPermissionForProjectError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Dont have permission',
        )
    except DialoguesLimitExceededError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The specified project has the maximum number of dialogues',
        )
    return dialogue


@router.put('/{dialogue_id}', response_model=DialogueReadSchema)
async def update_dialogue_trigger(
        project_id: int,
        dialogue_id: int,
        trigger: TriggerUpdateSchema,
        auth_jwt: AuthJWTDI,
        dialogue_service: DialogueServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        dialogue = await dialogue_service.check_access_and_update_dialogue_trigger(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
            trigger=trigger,
        )
    except ProjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project does not exist',
        )
    except NoPermissionForProjectError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Dont have permission',
        )
    except DialogueNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dialogue does not exist',
        )
    return dialogue


@router.delete('/{dialogue_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_dialogue(
        project_id: int,
        dialogue_id: int,
        auth_jwt: AuthJWTDI,
        dialogue_service: DialogueServiceDI,
):
    await auth_jwt.jwt_required()
    user_id = await auth_jwt.get_jwt_subject()

    try:
        await dialogue_service.check_access_and_delete_dialogue(
            user_id=user_id,
            project_id=project_id,
            dialogue_id=dialogue_id,
        )
    except ProjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project does not exist',
        )
    except NoPermissionForProjectError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Dont have permission',
        )
    except DialogueNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dialogue does not exist',
        )
    return {'detail': 'Диалог успешно удален'}
