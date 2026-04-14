from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.label import Label, LabelCreate

from app.repositories.label_repository import LabelRepository


class LabelService:
    def __init__(self, db: Session):
        self.repo = LabelRepository(db=db)

    def list(self, owner_id: int) -> list[Label]:
        return self.repo.list_by_user(owner_id=owner_id)
    
    def create(self, owner_id: int, playload: LabelCreate) -> Label:
        if self.repo.get_by_name(owner_id=owner_id, name=playload.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='La etiqueta ya existe!!'
            )
        self.repo.create(owner_id=owner_id, name=playload.name)

    def delete(self, owner_id: int, label_id: int) -> None:
        label = self.repo.get(label_id=label_id)
        if not label or label.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No existe la etiqueta!!'
            )