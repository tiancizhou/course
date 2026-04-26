from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/api/class-slots", tags=["固定时间段"])


@router.get("")
def list_slots(is_active: Optional[bool] = None, db: Session = Depends(get_db)):
    slots = crud.get_class_slots(db, is_active=is_active)
    result = []
    for s in slots:
        d = schemas.ClassSlotOut.model_validate(s).model_dump()
        # 附带学生列表
        slot_students = crud.get_slot_students(db, s.id)
        students = []
        for ss in slot_students:
            ss_out = schemas.SlotStudentOut.model_validate(ss).model_dump()
            ss_out["student_name"] = ss.student.name if ss.student else ""
            students.append(ss_out)
        d["students"] = students
        result.append(d)
    return {"code": 0, "data": result}


@router.post("")
def create_slot(data: schemas.ClassSlotCreate, db: Session = Depends(get_db)):
    slot = crud.create_class_slot(db, data)
    return {"code": 0, "data": schemas.ClassSlotOut.model_validate(slot).model_dump()}


@router.get("/{slot_id}")
def get_slot(slot_id: int, db: Session = Depends(get_db)):
    slot = crud.get_class_slot(db, slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="时间段不存在")
    return {"code": 0, "data": schemas.ClassSlotOut.model_validate(slot).model_dump()}


@router.put("/{slot_id}")
def update_slot(slot_id: int, data: schemas.ClassSlotUpdate, db: Session = Depends(get_db)):
    slot = crud.get_class_slot(db, slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="时间段不存在")
    slot = crud.update_class_slot(db, slot, data)
    return {"code": 0, "data": schemas.ClassSlotOut.model_validate(slot).model_dump()}


@router.delete("/{slot_id}")
def delete_slot(slot_id: int, db: Session = Depends(get_db)):
    slot = crud.get_class_slot(db, slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="时间段不存在")
    crud.delete_class_slot(db, slot)
    return {"code": 0, "message": "删除成功"}


@router.post("/{slot_id}/students")
def add_slot_student(slot_id: int, data: schemas.SlotStudentAdd, db: Session = Depends(get_db)):
    slot = crud.get_class_slot(db, slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="时间段不存在")
    student = crud.get_student(db, data.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    rel = crud.add_slot_student(db, slot_id, data)
    return {"code": 0, "data": schemas.SlotStudentOut.model_validate(rel).model_dump()}


@router.delete("/{slot_id}/students/{student_id}")
def remove_slot_student(slot_id: int, student_id: int, db: Session = Depends(get_db)):
    crud.remove_slot_student(db, slot_id, student_id)
    return {"code": 0, "message": "移除成功"}
