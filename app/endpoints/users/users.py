from typing import List

from fastapi import APIRouter, Depends
from injector import Injector
from pydantic import NonNegativeInt
from sqlalchemy.orm import Session

from app.db.orm.crud.common import UserCRUD
from app.endpoints.users.schema import UserSchemaInput, UserSchemaOutput

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
def read_many(
    skip: NonNegativeInt = 0,
    take: int = 5,
    injector: Injector = Depends(lambda: router.injector),  # type: ignore
) -> List[UserSchemaOutput]:
    users = UserCRUD().read(session=injector.get(Session), skip=skip, take=take)
    response = [UserSchemaOutput(**user.__dict__) for user in users]
    return response


@router.get("/{id}")
def read_one(
    id: int,
    injector: Injector = Depends(lambda: router.injector),  # type: ignore
) -> UserSchemaOutput:
    user = UserCRUD().get(session=injector.get(Session), id=id)
    response = UserSchemaOutput(**user.__dict__)

    return response


@router.post("/")
def create(
    user_schema: UserSchemaInput,
    injector: Injector = Depends(lambda: router.injector),  # type: ignore
) -> UserSchemaOutput:
    user = UserCRUD().create(
        session=injector.get(Session), payload=user_schema.dict(exclude_none=True)
    )
    response = UserSchemaOutput(**user.__dict__)

    return response


@router.put("/{id}")
def put(
    id: int,
    user_schema: UserSchemaInput,
    injector: Injector = Depends(lambda: router.injector),  # type: ignore
) -> UserSchemaOutput:
    user = UserCRUD().update(
        id=id,
        payload=user_schema.dict(exclude_none=True),
        session=injector.get(Session),
    )
    response = UserSchemaOutput(**user.__dict__)

    return response


@router.delete("/{id}")
def delete(
    id: int,
    injector: Injector = Depends(lambda: router.injector),  # type: ignore
) -> UserSchemaOutput:
    user = UserCRUD().delete(id=id, session=injector.get(Session))
    response = UserSchemaOutput(**user.__dict__)

    return response
