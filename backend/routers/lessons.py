from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/api/lessons", tags=["课程管理"])

WEEKDAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def _enrich_lesson(lesson, db):
    """给 lesson 附加额外字段"""
    result = schemas.LessonOut.model_validate(lesson).model_dump()
    if lesson.slot:
        result["slot_name"] = lesson.slot.name
    if lesson.term:
        result["term_name"] = lesson.term.name
    result["student_count"] = (
        db.query(models.LessonStudent)
        .filter(models.LessonStudent.lesson_id == lesson.id)
        .count()
    )
    return result


import models


@router.get("")
def list_lessons(
    term_id: Optional[int] = None,
    lesson_date: Optional[date] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    lessons = crud.get_lessons(db, term_id=term_id, lesson_date=lesson_date,
                               start_date=start_date, end_date=end_date, status=status)
    result = [_enrich_lesson(l, db) for l in lessons]
    return {"code": 0, "data": result}


@router.get("/{lesson_id}")
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = crud.get_lesson(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="课程不存在")
    return {"code": 0, "data": _enrich_lesson(lesson, db)}


@router.post("")
def create_lesson(data: schemas.LessonCreate, db: Session = Depends(get_db)):
    lesson = crud.create_lesson(db, data)
    return {"code": 0, "data": schemas.LessonOut.model_validate(lesson).model_dump()}


@router.put("/{lesson_id}")
def update_lesson(lesson_id: int, data: schemas.LessonUpdate, db: Session = Depends(get_db)):
    lesson = crud.get_lesson(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="课程不存在")
    lesson = crud.update_lesson(db, lesson, data)
    return {"code": 0, "data": schemas.LessonOut.model_validate(lesson).model_dump()}


@router.delete("/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = crud.get_lesson(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="课程不存在")
    crud.delete_lesson(db, lesson)
    return {"code": 0, "message": "删除成功"}


@router.get("/{lesson_id}/students")
def get_lesson_students(lesson_id: int, db: Session = Depends(get_db)):
    lesson_students = crud.get_lesson_students(db, lesson_id)
    result = []
    for ls in lesson_students:
        d = schemas.LessonStudentOut.model_validate(ls).model_dump()
        d["student_name"] = ls.student.name if ls.student else ""
        result.append(d)
    return {"code": 0, "data": result}


@router.post("/{lesson_id}/students")
def add_lesson_student(lesson_id: int, data: schemas.LessonStudentAdd, db: Session = Depends(get_db)):
    lesson = crud.get_lesson(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="课程不存在")
    ls = crud.add_lesson_student(db, lesson_id, data)
    return {"code": 0, "data": schemas.LessonStudentOut.model_validate(ls).model_dump()}


@router.delete("/{lesson_id}/students/{student_id}")
def remove_lesson_student(lesson_id: int, student_id: int, db: Session = Depends(get_db)):
    crud.remove_lesson_student(db, lesson_id, student_id)
    return {"code": 0, "message": "移除成功"}


@router.post("/{lesson_id}/attendance")
def take_attendance(lesson_id: int, records: list[schemas.AttendanceItem], db: Session = Depends(get_db)):
    lesson = crud.get_lesson(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="课程不存在")
    lesson = crud.take_attendance(db, lesson, records)
    return {"code": 0, "message": "点名成功", "data": schemas.LessonOut.model_validate(lesson).model_dump()}
