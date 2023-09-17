from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from database import schemas
from sqlalchemy.orm import Session
from models import evidence_crud, oauth2, gcs
from database.database import get_db
from typing import Annotated, Optional

router = APIRouter(tags=["Evidences"])


## Evidencias rotas


@router.get("/evidences/{id}", response_model=Optional[schemas.Evidence])
def get_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    id: int,
    db: Session = Depends(get_db),
):
    """Rota para buscar uma evidencia pelo id"""
    return evidence_crud.get_evidence(id=id, db=db)


@router.get("/evidences/", response_model=Optional[list[schemas.Evidence]])
def get_all_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    db: Session = Depends(get_db),
):
    """Rota para buscar todas evidencia"""
    return evidence_crud.get_all_evidence( db=db)


@router.post("/evidences/", response_model=Optional[schemas.Evidence])
def create_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    evidence: schemas.EvidenceCreate,
    db: Session = Depends(get_db),
):

    """Rota para criar uma nova evidencia"""
    return evidence_crud.create_evidence(db=db, evidence=evidence)


@router.put("/evidences/", response_model=Optional[schemas.Evidence])
def update_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    evidence: schemas.Evidence,
    db: Session = Depends(get_db),
):
    """Rota para alterar uma evidencia pelo id"""
    return evidence_crud.update_evidence(evidence=evidence, db=db)


@router.delete("/evidences/{id}")
def delete_evidence(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    id: int,
    db: Session = Depends(get_db),
):
    """Rota para deletar uma evidencia pelo id"""
    return evidence_crud.delete_evidence(id=id, db=db)

@router.post("/uploadfile/")
async def create_upload_file(
    current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)],
    file: UploadFile = File(...)
):
    """Rota para fazer upload de algum arquivo"""
    link = await gcs.GCStorage().upload_file(file)

    return link