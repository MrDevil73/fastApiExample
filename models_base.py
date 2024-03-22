from pydantic import BaseModel
from models import dt_time


class GroupBase(BaseModel):
    id: int
    title_name: str


class TeacherBase(BaseModel):
    id: int
    name: str
    smile: str


class AuditoryBase(BaseModel):
    id: int
    name: str


class LesTypesBase(BaseModel):
    id: int
    name: str
    smile: str


class SubGroupBase(BaseModel):
    id: int
    name: str
    smile: str


class LessonBase(BaseModel):
    id: int
    number_day: int
    order_in_day: int
    group: GroupBase
    subgroup: SubGroupBase
    discipline: str
    type: LesTypesBase
    teacher: TeacherBase
    audit: AuditoryBase
    time_start: dt_time
    time_finish: dt_time
