from fastapi import APIRouter, status

from app.api.deps import DBSession
from app.api.deps import current_user
from app.models.label import LabelRead, LabelCreate
from app.services.label_services import LabelService

router = APIRouter(prefix='/labels', tags=['labels'])


@router.get('/', response_model=list[LabelRead])
def list_labels(db: DBSession, user: current_user):
    return LabelService(db=db).list(owner_id=user.id)


@router.post('/', response_model=LabelRead, status_code=status.HTTP_201_CREATED)
def create(payload: LabelCreate, db: DBSession, user: current_user):
    return LabelService(db=db).create(owner_id=user.id, payload=payload)


@router.put('/{label_id}', response_model=LabelRead, status_code=status.HTTP_201_CREATED)
def delete(label_id: int, db: DBSession, user: current_user):
    return LabelService(db=db).delete(owner_id=user.id, label_id=label_id)