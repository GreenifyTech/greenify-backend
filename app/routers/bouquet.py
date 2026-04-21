from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.bouquet import BouquetCreate, BouquetResponse
from app.services.bouquet_service import create_bouquet, delete_bouquet, list_my_bouquets

router = APIRouter(prefix="/api/bouquets", tags=["Bouquet Builder"])


@router.post("/", response_model=BouquetResponse, status_code=201)
def bouquets_create(
    payload: BouquetCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return create_bouquet(db=db, user=user, payload=payload)


@router.get("/me", response_model=list[BouquetResponse])
def bouquets_me(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return list_my_bouquets(db=db, user=user)


@router.delete("/{bouquet_id}", status_code=204)
def bouquets_delete(
    bouquet_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    delete_bouquet(db=db, user=user, bouquet_id=bouquet_id)

