from models_base import AuditoryBase, GroupBase, LessonBase, LesTypesBase, SubGroupBase, TeacherBase
from fastapi import APIRouter, HTTPException
from repository import AuditoryRepository, TeacherRepository, LessonRepository, GroupRepository, SubGroupRepository, TypesRepository
from database import async_session_factory

first_router = APIRouter()
auditory_repository = AuditoryRepository(async_session_factory)
teacher_repository = TeacherRepository(async_session_factory)
lesson_repository = LessonRepository(async_session_factory)
group_repository = GroupRepository(async_session_factory)
subgroup_repository = SubGroupRepository(async_session_factory)
types_repository = TypesRepository(async_session_factory)


@first_router.get("/auditories/{auditory_id}", response_model=AuditoryBase)
async def read_auditory(auditory_id: int):
    auditory = await auditory_repository.get_by_id(auditory_id)
    if auditory is None:
        raise HTTPException(status_code=404, detail="Auditory not found")
    return auditory


@first_router.get("/auditories/", response_model=list[AuditoryBase])
async def filter_auditories_by_name(name: str = "", skip: int = 0, limit: int = 10):
    return await auditory_repository.filter_by_name(name, skip, limit)


@first_router.get("/teachers/{teacher_id}", response_model=TeacherBase)
async def read_teacher(teacher_id: int):
    teacher = await teacher_repository.get_by_id(teacher_id)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@first_router.get("/teachers/", response_model=list[TeacherBase])
async def filter_teachers_by_name(name: str = "", skip: int = 0, limit: int = 10):
    return await teacher_repository.filter_by_name(name, skip, limit)


@first_router.get("/lessons/{lesson_id}", response_model=LessonBase)
async def read_teacher(lesson_id: int):
    less = await lesson_repository.get_by_id(lesson_id)
    if less is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return less


@first_router.get("/lessons/", response_model=list[LessonBase])
async def filter_lessons_by_name(name: str = "", skip: int = 0, limit: int = 10,
                                 subgroup_id: int = 0, group_id: int = 0, teacher_id: int = 0, audit_id: int = 0, lestype_id: int = 0):
    less = await lesson_repository.filters_(name, skip, limit, subgroup_id, group_id, teacher_id, audit_id, lestype_id)
    return less


@first_router.get("/groups/{group_id}", response_model=GroupBase)
async def read_group(group_id: int):
    grp = await group_repository.get_by_id(group_id)
    if grp is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return grp


@first_router.get("/groups/", response_model=list[GroupBase])
async def filter_groups_by_name(name: str = "", skip: int = 0, limit: int = 10):
    return await group_repository.filter_by_name(name, skip, limit)


@first_router.get("/subgroups/{subgroup_id}", response_model=SubGroupBase)
async def read_subgroup(group_id: int):
    subgr = await subgroup_repository.get_by_id(group_id)
    if subgr is None:
        raise HTTPException(status_code=404, detail="Subgroup not found")
    return subgr


@first_router.get("/subgroups/", response_model=list[SubGroupBase])
async def filter_subgroups_by_name(name: str = "", skip: int = 0, limit: int = 10):
    return await subgroup_repository.filter_by_name(name, skip, limit)


@first_router.get("/lestypes/{lestype_id}", response_model=SubGroupBase)
async def read_subgroup(group_id: int):
    lestype = await types_repository.get_by_id(group_id)
    if lestype is None:
        raise HTTPException(status_code=404, detail="Lesson Type not found")
    return lestype


@first_router.get("/lestypes/", response_model=list[SubGroupBase])
async def filter_types_by_name(name: str = "", skip: int = 0, limit: int = 10):
    return await types_repository.filter_by_name(name, skip, limit)
