from datetime import time as dt_time

from sqlalchemy import ForeignKey
from database import Model, intpk
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Group(Model):
    __tablename__ = "groups"
    id: Mapped[intpk]
    name: Mapped[str]
    title_name: Mapped[str]


class Teacher(Model):
    __tablename__ = "teachers"
    id: Mapped[intpk]
    name: Mapped[str]
    smile: Mapped[str] = mapped_column(server_default="👨‍🏫")


class Auditory(Model):
    __tablename__ = "auditoryes"
    id: Mapped[intpk]
    name: Mapped[str]


class LesTypes(Model):
    __tablename__ = "lestypes"
    id: Mapped[intpk]
    name: Mapped[str]
    smile: Mapped[str] = mapped_column(server_default="🚪")


class SubGroup(Model):
    __tablename__ = "subgroups"
    id: Mapped[intpk]
    name: Mapped[str]
    smile: Mapped[str | None] = mapped_column(server_default="🐍")


class Lesson(Model):
    __tablename__ = "lessons"
    __allow_unmapped__ = True

    id: Mapped[intpk]
    number_day: Mapped[int]
    order_in_day: Mapped[int]
    group_id: Mapped[int | None] = mapped_column(ForeignKey("groups.id", ondelete="SET NULL"))
    group: "Group" = relationship("Group", lazy="joined")
    subgroup_id: Mapped[int | None] = mapped_column(ForeignKey("subgroups.id", ondelete="SET NULL"))
    subgroup: "SubGroup" = relationship("SubGroup", lazy="joined")
    discipline: Mapped[str]
    type_id: Mapped[int | None] = mapped_column(ForeignKey("lestypes.id", ondelete="SET NULL"))
    type: "LesTypes" = relationship("LesTypes", lazy="joined")

    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teachers.id", ondelete="SET NULL"))
    teacher: "Teacher" = relationship("Teacher", lazy="joined")

    audit_id: Mapped[int | None] = mapped_column(ForeignKey("auditoryes.id", ondelete="SET NULL"))
    audit: "Auditory" = relationship("Auditory", lazy="joined")

    time_start: Mapped[dt_time]
    time_finish: Mapped[dt_time]
