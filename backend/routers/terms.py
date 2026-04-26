from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/api/terms", tags=["学期管理"])


@router.get("")
def list_terms(db: Session = Depends(get_db)):
    terms = crud.get_terms(db)
    return {"code": 0, "data": [schemas.TermOut.model_validate(t).model_dump() for t in terms]}


@router.post("")
def create_term(data: schemas.TermCreate, db: Session = Depends(get_db)):
    if data.end_date <= data.start_date:
        raise HTTPException(status_code=400, detail="结束日期必须晚于开始日期")
    term = crud.create_term(db, data)
    return {"code": 0, "data": schemas.TermOut.model_validate(term).model_dump()}


@router.get("/{term_id}")
def get_term(term_id: int, db: Session = Depends(get_db)):
    term = crud.get_term(db, term_id)
    if not term:
        raise HTTPException(status_code=404, detail="学期不存在")
    return {"code": 0, "data": schemas.TermOut.model_validate(term).model_dump()}


@router.put("/{term_id}")
def update_term(term_id: int, data: schemas.TermUpdate, db: Session = Depends(get_db)):
    term = crud.get_term(db, term_id)
    if not term:
        raise HTTPException(status_code=404, detail="学期不存在")
    term = crud.update_term(db, term, data)
    return {"code": 0, "data": schemas.TermOut.model_validate(term).model_dump()}


@router.delete("/{term_id}")
def delete_term(term_id: int, db: Session = Depends(get_db)):
    term = crud.get_term(db, term_id)
    if not term:
        raise HTTPException(status_code=404, detail="学期不存在")
    crud.delete_term(db, term)
    return {"code": 0, "message": "删除成功"}


@router.post("/{term_id}/generate-lessons")
def generate_lessons(term_id: int, db: Session = Depends(get_db)):
    term = crud.get_term(db, term_id)
    if not term:
        raise HTTPException(status_code=404, detail="学期不存在")
    generated = crud.generate_lessons(db, term)
    return {"code": 0, "message": f"成功生成 {len(generated)} 节课程", "data": len(generated)}
