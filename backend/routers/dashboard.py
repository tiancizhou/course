from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["首页"])

WEEKDAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


@router.get("")
def get_dashboard(db: Session = Depends(get_db)):
    today = date.today()
    # 本周一和周日
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    # 学生总数（活跃）
    total_students = (
        db.query(models.Student)
        .filter(models.Student.status == "active")
        .count()
    )

    # 今日课程
    today_lessons = (
        db.query(models.Lesson)
        .filter(models.Lesson.lesson_date == today)
        .order_by(models.Lesson.start_time)
        .all()
    )

    # 本周课程
    week_lessons = (
        db.query(models.Lesson)
        .filter(models.Lesson.lesson_date >= monday, models.Lesson.lesson_date <= sunday)
        .order_by(models.Lesson.lesson_date, models.Lesson.start_time)
        .all()
    )

    def lesson_to_item(l):
        item = schemas.DashboardLessonItem(
            id=l.id,
            lesson_date=l.lesson_date,
            weekday=l.weekday,
            start_time=l.start_time,
            end_time=l.end_time,
            slot_name=l.slot.name if l.slot else None,
            lesson_type=l.lesson_type,
            status=l.status,
            student_count=len(l.students),
        )
        return item.model_dump()

    today_items = [lesson_to_item(l) for l in today_lessons]
    week_items = [lesson_to_item(l) for l in week_lessons]

    # 今日待上课
    today_pending = len([l for l in today_lessons if l.status == "scheduled"])

    # 课时不足学生 (<=3)
    low_hour_students = (
        db.query(models.Student)
        .filter(
            models.Student.status == "active",
            models.Student.remaining_hours > 0,
            models.Student.remaining_hours <= 3,
        )
        .all()
    )

    # 欠课时学生 (<=0)
    zero_hour_students = (
        db.query(models.Student)
        .filter(
            models.Student.status == "active",
            models.Student.remaining_hours <= 0,
        )
        .all()
    )

    def student_to_low(s):
        return schemas.DashboardLowHourStudent(
            id=s.id, name=s.name, remaining_hours=s.remaining_hours, phone=s.phone,
        ).model_dump()

    dashboard = schemas.DashboardOut(
        total_students=total_students,
        today_lessons=today_items,
        week_lessons=week_items,
        low_hour_students=[student_to_low(s) for s in low_hour_students],
        zero_hour_students=[student_to_low(s) for s in zero_hour_students],
        today_pending_count=today_pending,
    )

    return {"code": 0, "data": dashboard.model_dump()}
