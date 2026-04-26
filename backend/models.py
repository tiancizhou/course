from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Time,
    Boolean, Text, ForeignKey, Numeric,
)
from sqlalchemy.orm import relationship

from database import Base


class Student(Base):
    """学生表"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="学生姓名")
    parent_name = Column(String(50), default="", comment="家长姓名")
    phone = Column(String(20), default="", comment="联系电话")
    total_hours = Column(Numeric(10, 1), default=0, comment="累计购买课时")
    remaining_hours = Column(Numeric(10, 1), default=0, comment="剩余课时")
    status = Column(String(20), default="active", comment="状态: active/suspended/quit")
    remark = Column(Text, default="", comment="备注")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class ClassSlot(Base):
    """固定时间段表"""
    __tablename__ = "class_slots"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="时间段名称")
    weekday = Column(Integer, nullable=False, comment="星期几, 0=周一, 6=周日")
    start_time = Column(Time, nullable=False, comment="开始时间")
    end_time = Column(Time, nullable=False, comment="结束时间")
    location = Column(String(200), default="", comment="上课地点")
    is_active = Column(Boolean, default=True, comment="是否启用")
    remark = Column(Text, default="", comment="备注")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    students = relationship("SlotStudent", back_populates="slot", cascade="all, delete-orphan")


class SlotStudent(Base):
    """时间段-学生关系表"""
    __tablename__ = "slot_students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    slot_id = Column(Integer, ForeignKey("class_slots.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, nullable=False, comment="生效开始日期")
    end_date = Column(Date, nullable=True, comment="生效结束日期, NULL=长期有效")
    status = Column(String(20), default="active", comment="状态: active/inactive")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    slot = relationship("ClassSlot", back_populates="students")
    student = relationship("Student")


class Term(Base):
    """学期表"""
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="学期名称")
    start_date = Column(Date, nullable=False, comment="开始日期")
    end_date = Column(Date, nullable=False, comment="结束日期")
    status = Column(String(20), default="not_started", comment="状态: not_started/active/ended")
    remark = Column(Text, default="", comment="备注")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Lesson(Base):
    """课程表"""
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    term_id = Column(Integer, ForeignKey("terms.id", ondelete="SET NULL"), nullable=True)
    slot_id = Column(Integer, ForeignKey("class_slots.id", ondelete="SET NULL"), nullable=True)
    lesson_date = Column(Date, nullable=False, comment="上课日期")
    weekday = Column(Integer, nullable=False, comment="星期几")
    start_time = Column(Time, nullable=False, comment="开始时间")
    end_time = Column(Time, nullable=False, comment="结束时间")
    lesson_type = Column(String(20), default="regular", comment="类型: regular/makeup/temporary")
    status = Column(String(20), default="scheduled", comment="状态: scheduled/completed/cancelled")
    remark = Column(Text, default="", comment="备注")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    term = relationship("Term")
    slot = relationship("ClassSlot")
    students = relationship("LessonStudent", back_populates="lesson", cascade="all, delete-orphan")


class LessonStudent(Base):
    """课程-学生表（点名记录）"""
    __tablename__ = "lesson_students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    source_type = Column(String(20), default="slot", comment="来源: slot/manual/makeup")
    attendance_status = Column(String(20), default="pending", comment="状态: pending/present/leave/absent/makeup")
    hour_change = Column(Numeric(10, 1), default=0, comment="课时变化")
    remark = Column(Text, default="", comment="备注")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    lesson = relationship("Lesson", back_populates="students")
    student = relationship("Student")


class HourRecord(Base):
    """课时流水表"""
    __tablename__ = "hour_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="SET NULL"), nullable=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True)
    change_hours = Column(Numeric(10, 1), nullable=False, comment="变化课时")
    before_hours = Column(Numeric(10, 1), nullable=False, comment="变化前课时")
    after_hours = Column(Numeric(10, 1), nullable=False, comment="变化后课时")
    record_type = Column(String(30), nullable=False, comment="类型: purchase/present_deduct/makeup_deduct/absent_deduct/manual_adjust/refund")
    remark = Column(Text, default="", comment="备注")
    created_at = Column(DateTime, default=datetime.now)

    student = relationship("Student")
    lesson = relationship("Lesson")
