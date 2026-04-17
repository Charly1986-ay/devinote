from fastapi import APIRouter, status
from app.api.deps import DBSession
from app.api.deps import current_user
from app.models.share import ShareRequest
from app.services.share_services import ShareServices


router = APIRouter(prefix='/shares', tags=['shares'])


@router.post('/notes/{note_id}', status_code=status.HTTP_201_CREATED)
def share_note(
    note_id: int, 
    payload: ShareRequest, 
    db: DBSession, 
    user: current_user
):
    share = ShareServices(db).share_note(
        owner_id=user.id, 
        note_id=note_id, 
        target_user_id=payload.target_id, 
        role=payload.role
    )

    return {
        'id': share.id,
        'note_id': note_id,
        'user_target_id': share.user_id,
        'role': share.role
    }


@router.delete('/notes/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
def unhare_note(
    note_id: int, 
    target_id: int,    
    db: DBSession, 
    user: current_user
):
    ShareServices(db).unshare_note(
        owner_id=user.id, 
        note_id=note_id, 
        target_user_id=target_id        
    )
    return None


@router.post('/labels/{label_id}', status_code=status.HTTP_201_CREATED)
def share_label(
    label_id: int, 
    payload: ShareRequest, 
    db: DBSession, 
    user: current_user
):
    share = ShareServices(db).share_label(
        owner_id=user.id, 
        label_id=label_id, 
        target_user_id=payload.target_id, 
        role=payload.role
    )

    return {
        'id': share.id,
        'label_id': label_id,
        'user_target_id': share.user_id,
        'role': share.role
    }


@router.delete('/labels/{label_id}', status_code=status.HTTP_204_NO_CONTENT)
def unhare_label(
    label_id: int, 
    target_id: int,    
    db: DBSession, 
    user: current_user
):
    ShareServices(db).unshare_label(
        owner_id=user.id, 
        label_id=label_id, 
        target_user_id=target_id        
    )
    return None