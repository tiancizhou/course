from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/api/students", tags=["学生管理"])


@router.get("")
def list_students(
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
):
    students = crud.get_students(db, status=status, keyword=keyword)
    return {"code": 0, "data": [schemas.StudentOut.model_validate(s).model_dump() for s in students]}


@router.post("")
def create_student(data: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = crud.create_student(db, data)
    return {"code": 0, "data": schemas.StudentOut.model_validate(student).model_dump()}


@router.get("/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    return {"code": 0, "data": schemas.StudentOut.model_validate(student).model_dump()}


@router.put("/{student_id}")
def update_student(student_id: int, data: schemas.StudentUpdate, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    student = crud.update_student(db, student, data)
    return {"code": 0, "data": schemas.StudentOut.model_validate(student).model_dump()}


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    crud.delete_student(db, student)
    return {"code": 0, "message": "删除成功"}


@router.post("/{student_id}/recharge")
def recharge_student(student_id: int, data: schemas.RechargeRequest, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    student = crud.recharge_student(db, student, data)
    return {"code": 0, "data": schemas.StudentOut.model_validate(student).model_dump()}


@router.get("/{student_id}/hour-records")
def get_hour_records(student_id: int, db: Session = Depends(get_db)):
    records = crud.get_hour_records(db, student_id)
    return {"code": 0, "data": [schemas.HourRecordOut.model_validate(r).model_dump() for r in records]}
