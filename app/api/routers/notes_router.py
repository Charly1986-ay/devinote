from fastapi import APIRouter, status

from app.api.deps import DBSession
from app.models.note import NoteCreate, NoteRead
from app.api.deps import current_user
from app.services.note_services import NoteService

router = APIRouter(prefix='/notes', tags=['notes'])


@router.get('/', response_model=list[NoteRead])
def list_notes(db: DBSession, user: current_user):
    return NoteService(db).list_visible(user.id)


@router.post('/', response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(playload: NoteCreate, db: DBSession, user: current_user):
    return NoteService(db=db).create(owner_id=user.id, playload=playload)


@router.patch('/{note_id}', response_model=NoteRead)
def update_note(
    note_id: int, 
    playload: NoteCreate, 
    db: DBSession, 
    user: current_user
):
    return NoteService(db=db).update(
        user_id=user.id, 
        note_id=note_id, 
        playload=playload
    )


@router.patch('/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,    
    db: DBSession, 
    user: current_user
):
    NoteService(db=db).delete(user_id=user.id, note_id=note_id)