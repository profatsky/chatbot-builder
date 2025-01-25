from fastapi import APIRouter, status, HTTPException

from src.auth.dependencies.jwt_dependencies import AuthJWTDI
from src.dialogues.dependencies.services_dependencies import DialogueServiceDI
from src.dialogues.exceptions.http_exceptions import DialoguesLimitExceededHTTPException, DialogueNotFoundHTTPException
from src.dialogues.exceptions.services_exceptions import DialoguesLimitExceededError, DialogueNotFoundError
from src.dialogues.schemas import DialogueCreateSchema, DialogueReadSchema, TriggerUpdateSchema
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException, NoPermissionForProjectHTTPException
from src.projects.exceptions.services_exceptions import ProjectNotFoundError, NoPermissionForProjectError

router = APIRouter(
    prefix='/projects/{project_id}/dialogues',
    tags=['Dialogues'],
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
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except DialoguesLimitExceededError:
        raise DialoguesLimitExceededHTTPException

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
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException

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
        raise ProjectNotFoundHTTPException

    except NoPermissionForProjectError:
        raise NoPermissionForProjectHTTPException

    except DialogueNotFoundError:
        raise DialogueNotFoundHTTPException

    return {'detail': 'Диалог успешно удален'}
