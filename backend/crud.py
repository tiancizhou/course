"""课时流水相关操作"""

from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session

import models
import schemas


# ============ 学生 ============

def get_students(db: Session, status: Optional[str] = None, keyword: Optional[str] = None):
    query = db.query(models.Student)
    if status:
        query = query.filter(models.Student.status == status)
    if keyword:
        query = query.filter(models.Student.name.contains(keyword))
    return query.order_by(models.Student.id.desc()).all()


def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def create_student(db: Session, data: schemas.StudentCreate):
    student = models.Student(**data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(db: Session, student: models.Student, data: schemas.StudentUpdate):
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)
    student.updated_at = datetime.now()
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student: models.Student):
    db.delete(student)
    db.commit()


def recharge_student(db: Session, student: models.Student, data: schemas.RechargeRequest):
    before = student.remaining_hours
    after = before + data.hours
    student.remaining_hours = after
    student.total_hours = student.total_hours + data.hours
    student.updated_at = datetime.now()

    record = models.HourRecord(
        student_id=student.id,
        change_hours=data.hours,
        before_hours=before,
        after_hours=after,
        record_type="purchase",
        remark=data.remark,
    )
    db.add(record)
    db.commit()
    db.refresh(student)
    return student


def get_hour_records(db: Session, student_id: int):
    return (
        db.query(models.HourRecord)
        .filter(models.HourRecord.student_id == student_id)
        .order_by(models.HourRecord.id.desc())
        .all()
    )


# ============ 固定时间段 ============

def get_class_slots(db: Session, is_active: Optional[bool] = None):
    query = db.query(models.ClassSlot)
    if is_active is not None:
        query = query.filter(models.ClassSlot.is_active == is_active)
    return query.order_by(models.ClassSlot.weekday, models.ClassSlot.start_time).all()


def get_class_slot(db: Session, slot_id: int):
    return db.query(models.ClassSlot).filter(models.ClassSlot.id == slot_id).first()


def create_class_slot(db: Session, data: schemas.ClassSlotCreate):
    slot = models.ClassSlot(**data.model_dump())
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot


def update_class_slot(db: Session, slot: models.ClassSlot, data: schemas.ClassSlotUpdate):
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(slot, key, value)
    slot.updated_at = datetime.now()
    db.commit()
    db.refresh(slot)
    return slot


def delete_class_slot(db: Session, slot: models.ClassSlot):
    db.delete(slot)
    db.commit()


def get_slot_students(db: Session, slot_id: int):
    return (
        db.query(models.SlotStudent)
        .filter(models.SlotStudent.slot_id == slot_id)
        .order_by(models.SlotStudent.id.desc())
        .all()
    )


def add_slot_student(db: Session, slot_id: int, data: schemas.SlotStudentAdd):
    # 检查是否已存在生效中的关系
    existing = (
        db.query(models.SlotStudent)
        .filter(
            models.SlotStudent.slot_id == slot_id,
            models.SlotStudent.student_id == data.student_id,
            models.SlotStudent.status == "active",
        )
        .first()
    )
    if existing:
        return existing

    rel = models.SlotStudent(
        slot_id=slot_id,
        student_id=data.student_id,
        start_date=data.start_date,
        status="active",
    )
    db.add(rel)
    db.commit()
    db.refresh(rel)
    return rel


def remove_slot_student(db: Session, slot_id: int, student_id: int):
    rel = (
        db.query(models.SlotStudent)
        .filter(
            models.SlotStudent.slot_id == slot_id,
            models.SlotStudent.student_id == student_id,
            models.SlotStudent.status == "active",
        )
        .first()
    )
    if rel:
        rel.status = "inactive"
        rel.end_date = date.today()
        rel.updated_at = datetime.now()
        db.commit()
    return rel


# ============ 学期 ============

def get_terms(db: Session):
    return db.query(models.Term).order_by(models.Term.id.desc()).all()


def get_term(db: Session, term_id: int):
    return db.query(models.Term).filter(models.Term.id == term_id).first()


def create_term(db: Session, data: schemas.TermCreate):
    term = models.Term(**data.model_dump())
    db.add(term)
    db.commit()
    db.refresh(term)
    return term


def update_term(db: Session, term: models.Term, data: schemas.TermUpdate):
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(term, key, value)
    term.updated_at = datetime.now()
    db.commit()
    db.refresh(term)
    return term


def delete_term(db: Session, term: models.Term):
    db.delete(term)
    db.commit()


# ============ 课程 ============

def get_lessons(
    db: Session,
    term_id: Optional[int] = None,
    lesson_date: Optional[date] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[str] = None,
):
    query = db.query(models.Lesson)
    if term_id:
        query = query.filter(models.Lesson.term_id == term_id)
    if lesson_date:
        query = query.filter(models.Lesson.lesson_date == lesson_date)
    if start_date:
        query = query.filter(models.Lesson.lesson_date >= start_date)
    if end_date:
        query = query.filter(models.Lesson.lesson_date <= end_date)
    if status:
        query = query.filter(models.Lesson.status == status)
    return query.order_by(models.Lesson.lesson_date, models.Lesson.start_time).all()


def get_lesson(db: Session, lesson_id: int):
    return db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()


def create_lesson(db: Session, data: schemas.LessonCreate):
    lesson = models.Lesson(**data.model_dump())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


def update_lesson(db: Session, lesson: models.Lesson, data: schemas.LessonUpdate):
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(lesson, key, value)
    lesson.updated_at = datetime.now()
    db.commit()
    db.refresh(lesson)
    return lesson


def delete_lesson(db: Session, lesson: models.Lesson):
    db.delete(lesson)
    db.commit()


def get_lesson_students(db: Session, lesson_id: int):
    return (
        db.query(models.LessonStudent)
        .filter(models.LessonStudent.lesson_id == lesson_id)
        .all()
    )


def add_lesson_student(db: Session, lesson_id: int, data: schemas.LessonStudentAdd):
    existing = (
        db.query(models.LessonStudent)
        .filter(
            models.LessonStudent.lesson_id == lesson_id,
            models.LessonStudent.student_id == data.student_id,
        )
        .first()
    )
    if existing:
        return existing

    ls = models.LessonStudent(
        lesson_id=lesson_id,
        student_id=data.student_id,
        source_type=data.source_type,
    )
    db.add(ls)
    db.commit()
    db.refresh(ls)
    return ls


def remove_lesson_student(db: Session, lesson_id: int, student_id: int):
    ls = (
        db.query(models.LessonStudent)
        .filter(
            models.LessonStudent.lesson_id == lesson_id,
            models.LessonStudent.student_id == student_id,
        )
        .first()
    )
    if ls:
        db.delete(ls)
        db.commit()
    return ls


# ============ 生成课程 ============

def generate_lessons(db: Session, term: models.Term):
    """根据学期日期和固定时间段自动生成课程"""
    slots = db.query(models.ClassSlot).filter(models.ClassSlot.is_active == True).all()

    generated = []
    current = term.start_date
    while current <= term.end_date:
        weekday = current.weekday()  # 0=周一
        for slot in slots:
            if slot.weekday == weekday:
                # 检查是否已存在
                exists = (
                    db.query(models.Lesson)
                    .filter(
                        models.Lesson.term_id == term.id,
                        models.Lesson.slot_id == slot.id,
                        models.Lesson.lesson_date == current,
                    )
                    .first()
                )
                if exists:
                    continue

                lesson = models.Lesson(
                    term_id=term.id,
                    slot_id=slot.id,
                    lesson_date=current,
                    weekday=weekday,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    lesson_type="regular",
                    status="scheduled",
                )
                db.add(lesson)
                db.flush()  # 获取 lesson.id

                # 根据 slot_students 生成 lesson_students
                slot_stu_rels = (
                    db.query(models.SlotStudent)
                    .filter(
                        models.SlotStudent.slot_id == slot.id,
                        models.SlotStudent.status == "active",
                        models.SlotStudent.start_date <= current,
                    )
                    .all()
                )
                for rel in slot_stu_rels:
                    # 如果 end_date 有值且已过期，跳过
                    if rel.end_date and rel.end_date < current:
                        continue
                    ls = models.LessonStudent(
                        lesson_id=lesson.id,
                        student_id=rel.student_id,
                        source_type="slot",
                    )
                    db.add(ls)

                generated.append(lesson)

        current += timedelta(days=1)

    term.status = "active"
    term.updated_at = datetime.now()
    db.commit()
    return generated


# ============ 点名 ============

def take_attendance(db: Session, lesson: models.Lesson, records: List[schemas.AttendanceItem]):
    """点名并扣课时，支持重复提交（先回滚再重新扣）"""
    # 1. 回滚已有的课时变化
    existing_records = (
        db.query(models.LessonStudent)
        .filter(models.LessonStudent.lesson_id == lesson.id)
        .all()
    )
    existing_map = {r.student_id: r for r in existing_records}

    # 回滚旧的 hour_records 和学生剩余课时
    old_hour_records = (
        db.query(models.HourRecord)
        .filter(models.HourRecord.lesson_id == lesson.id)
        .all()
    )
    for hr in old_hour_records:
        student = db.query(models.Student).filter(models.Student.id == hr.student_id).first()
        if student:
            student.remaining_hours = student.remaining_hours - hr.change_hours  # change_hours 是负数，减负=加回
        db.delete(hr)

    # 2. 应用新的点名结果
    for item in records:
        ls = existing_map.get(item.student_id)
        if not ls:
            ls = models.LessonStudent(
                lesson_id=lesson.id,
                student_id=item.student_id,
                source_type="manual",
            )
            db.add(ls)
            db.flush()

        ls.attendance_status = item.attendance_status
        deduct = item.deduct_hours
        ls.hour_change = -deduct

        if deduct > 0:
            student = db.query(models.Student).filter(models.Student.id == item.student_id).first()
            if student:
                before = student.remaining_hours
                after = before - deduct
                student.remaining_hours = after
                student.updated_at = datetime.now()

                # 确定流水类型
                record_type = "manual_adjust"
                if item.attendance_status == "present":
                    record_type = "present_deduct"
                elif item.attendance_status == "absent":
                    record_type = "absent_deduct"
                elif item.attendance_status == "makeup":
                    record_type = "makeup_deduct"

                hr = models.HourRecord(
                    student_id=student.id,
                    lesson_id=lesson.id,
                    change_hours=-deduct,
                    before_hours=before,
                    after_hours=after,
                    record_type=record_type,
                )
                db.add(hr)

    lesson.status = "completed"
    lesson.updated_at = datetime.now()
    db.commit()
    db.refresh(lesson)
    return lesson
