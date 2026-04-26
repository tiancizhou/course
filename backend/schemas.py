from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field


# ============ 通用 ============

class ResponseBase(BaseModel):
    code: int = 0
    message: str = "success"


# ============ 学生 ============

class StudentCreate(BaseModel):
    name: str
    parent_name: str = ""
    phone: str = ""
    remark: str = ""


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    parent_name: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class StudentOut(BaseModel):
    id: int
    name: str
    parent_name: str
    phone: str
    total_hours: Decimal
    remaining_hours: Decimal
    status: str
    remark: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RechargeRequest(BaseModel):
    hours: Decimal = Field(..., gt=0, description="充值课时数")
    remark: str = ""


class HourRecordOut(BaseModel):
    id: int
    student_id: Optional[int] = None
    lesson_id: Optional[int] = None
    change_hours: Decimal
    before_hours: Decimal
    after_hours: Decimal
    record_type: str
    remark: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ============ 固定时间段 ============

class ClassSlotCreate(BaseModel):
    name: str
    weekday: int = Field(..., ge=0, le=6)
    start_time: time
    end_time: time
    location: str = ""
    remark: str = ""


class ClassSlotUpdate(BaseModel):
    name: Optional[str] = None
    weekday: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None
    remark: Optional[str] = None


class ClassSlotOut(BaseModel):
    id: int
    name: str
    weekday: int
    start_time: time
    end_time: time
    location: str
    is_active: bool
    remark: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SlotStudentAdd(BaseModel):
    student_id: int
    start_date: date


class SlotStudentOut(BaseModel):
    id: int
    slot_id: int
    student_id: int
    start_date: date
    end_date: Optional[date] = None
    status: str
    student_name: Optional[str] = None

    model_config = {"from_attributes": True}


# ============ 学期 ============

class TermCreate(BaseModel):
    name: str
    start_date: date
    end_date: date
    remark: str = ""


class TermUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class TermOut(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    status: str
    remark: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ============ 课程 ============

class LessonCreate(BaseModel):
    term_id: Optional[int] = None
    slot_id: Optional[int] = None
    lesson_date: date
    weekday: int
    start_time: time
    end_time: time
    lesson_type: str = "regular"
    remark: str = ""


class LessonUpdate(BaseModel):
    lesson_date: Optional[date] = None
    weekday: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class LessonOut(BaseModel):
    id: int
    term_id: Optional[int] = None
    slot_id: Optional[int] = None
    lesson_date: date
    weekday: int
    start_time: time
    end_time: time
    lesson_type: str
    status: str
    remark: str
    created_at: datetime
    updated_at: datetime
    slot_name: Optional[str] = None
    term_name: Optional[str] = None
    student_count: int = 0

    model_config = {"from_attributes": True}


class LessonStudentAdd(BaseModel):
    student_id: int
    source_type: str = "manual"


class LessonStudentOut(BaseModel):
    id: int
    lesson_id: int
    student_id: int
    source_type: str
    attendance_status: str
    hour_change: Decimal
    remark: str
    student_name: Optional[str] = None

    model_config = {"from_attributes": True}


# ============ 点名 ============

class AttendanceItem(BaseModel):
    student_id: int
    attendance_status: str = Field(..., description="present/leave/absent/makeup")
    deduct_hours: Decimal = Field(default=1, description="扣课时数")


class AttendanceRequest(BaseModel):
    records: List[AttendanceItem]


# ============ Dashboard ============

class DashboardLessonItem(BaseModel):
    id: int
    lesson_date: date
    weekday: int
    start_time: time
    end_time: time
    slot_name: Optional[str] = None
    lesson_type: str
    status: str
    student_count: int = 0


class DashboardLowHourStudent(BaseModel):
    id: int
    name: str
    remaining_hours: Decimal
    phone: str


class DashboardOut(BaseModel):
    total_students: int = 0
    today_lessons: List[DashboardLessonItem] = []
    week_lessons: List[DashboardLessonItem] = []
    low_hour_students: List[DashboardLowHourStudent] = []
    zero_hour_students: List[DashboardLowHourStudent] = []
    today_pending_count: int = 0
