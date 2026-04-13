from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.note import Note, NoteCreate, NoteUpdate
from app.models.share import ShareRol
from app.repositories.label_repository import LabelReository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository


class NoteService:
    def __init__(self, db: Session):
        self.db = db
        self.notes = NoteRepository(db=db)
        self.labels = LabelReository(db=db)
        self.shares = ShareRepository(db=db)

    # permisos
    def user_can_read(self, user_id: int, note: Note) -> bool:
        if note.owner_id==user_id:
            return True
        
        if self.shares.has_note_share(note_id=note.id, user_id=user_id):
            return True
        
        labels_id = self.labels.list_note_ids_by_label_ids(note.id)

        return self.shares.has_any_label_share(
            label_ids=labels_id, 
            user_id=user_id
        )
    

    def user_can_edit(self, user_id: int, note: Note) -> bool:
        if note.owner_id==user_id:
            return True
        
        if self.shares.has_note_share(note_id=note.id, user_id=user_id, role=ShareRol.EDIT):
            return True
        
        labels_id = self.labels.list_note_ids_by_label_ids(note.id)

        return self.shares.has_any_label_share(
            label_ids=labels_id, 
            user_id=user_id,
            role=ShareRol.EDIT
        )
    
    
    def list_visible(self, user_id: int) -> list[Note]:
        owned = self.notes.list_owner(user_id)

        direct_ids = self.shares.list_note_ids_shared_directly(user_id=user_id)

        shared_label_ids = self.shares.list_label_ids_shared_with_user(user_id=user_id)
        ids_by_label = self.labels.list_note_ids_by_label_ids(shared_label_ids)

        combined_ids = list({*direct_ids, *ids_by_label})
        shared = self.notes.list_by_ids(ids=combined_ids)

        combined = {note.id: note for note in owned}

        for note in shared:
            combined.setdefault(note.id, note)
        
        return sorted(combined.values(), key=lambda note: note.id, reverse=True)
    

    def create(self, owner_id: int, playload: NoteCreate) -> Note:
        note = self.notes.create(
            owner_id=owner_id,
            **playload.model_dump(exclude={"label_ids"})
        )

        if playload.label_ids:
            self._set_labels(owner_id=owner_id, note_id=note.id, label_ids=playload.label_ids)        
        return note
    

    def update(self, user_id: int, note_id: int, playload: NoteUpdate) -> Note:
        note = self.notes.get(note_id=note_id)        

        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Nota no encontrada'
            )     

        if not self.user_can_edit(user_id=user_id, note=note):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='No autorizado'
            )
        
        updates = playload.model_dump(exclude=True)
        label_ids = self.updates.pop('label_ids', None)

        for key, value in updates.items():
            setattr(note, key, value)

        note = self.notes.update(note=note)

        if label_ids is not None:
            if note.owner_id != user_id:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No existe o no autorizado'
            )
        else:
            self._set_labels(owner_id=user_id, note_id=note.id, label_ids=label_ids)

        return note
    
    def delete(self, user_id: int, note_id: int) -> None:
        note = self.notes.get(note_id)
        if not note or note.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No existe la nota o no autorizado"
            )
        
        self.notes.delete(note)
    
    
    # helper
    def _set_labels(self, owner_id: int, note_id: int, label_ids: list[int]) -> None:
        valid_ids = self.labels.list_ids_for_owner_subset(
            owner_id=owner_id, 
            ids=label_ids or []
        )

        self.notes.replace_labels(
            note_id=note_id, 
            label_ids=label_ids
        )
