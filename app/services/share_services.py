from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.share import ShareRole
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository


class ShareServices:
    def __int__(self, db: Session):
        self.shares = ShareRepository(db=db)
        self.notes = NoteRepository(db=db)
        self.labels = LabelRepository(db=db)


    def share_note(self, owner_id: int, note_id: int, target_user_id: int, role: ShareRole):
        note = self.notes.get(note_id=note_id)

        if not note or note.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No nota no encontrada o no autorizada!!'
            )
        
        share = self.shares.upser_note_share(
            note_id=note_id, 
            user_id=target_user_id, 
            role=role.value if hasattr(role, 'value') else role)
        
        return share
    

    def unshare_note(self, owner_id: int, note_id: int, target_user_id: int):
        note = self.notes.get(note_id=note_id)

        if not note or note.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No nota no encontrada o no autorizada!!'
            )
        
        self.shares.remove_note_share(note_id=note_id, user_id=target_user_id)


    def share_label(self, owner_id: int, label_id: int, target_user_id: int, role: ShareRole):
        label = self.labels.get(label_id)
        if not label or label.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Etiqueta no encontrada o no autorizada!!'
            )
        
        share = self.shares.upser_label_share(
            label_id=label_id, 
            user_id=target_user_id, 
            role=role.value if hasattr(role, 'value') else role
        )

        return share
    
    def unshare_label(self, owner_id: int, label_id: int, target_user_id: int):
        label = self.labels.get(label_id)
        if not label or label.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Etiqueta no encontrada o no autorizada!!'
            )
        
        share = self.shares.remove_label_share(
            label_id=label_id, 
            user_id=target_user_id           
        )

        return share