from typing import Optional
from sqlalchemy.future import select
from sqlalchemy import func
from models import Auditory, Teacher, Lesson, Group, SubGroup, LesTypes
from sqlalchemy.ext.asyncio import AsyncSession


class AuditoryRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_by_id(self, auditory_id: int) -> Optional[Auditory]:
        async with self.db() as session:
            result = await session.execute(select(Auditory).filter(Auditory.id == auditory_id))
            return result.scalars().first()

    async def filter_by_name(self, name: str, skip: int = 0, limit: int = 10) -> list[Auditory]:
        async with self.db() as session:
            result = await session.execute(select(Auditory).filter(func.lower(Auditory.name).like(f"%{name.lower()}%")).offset(skip).limit(limit))
            return result.scalars().all()


class TeacherRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, teacher_id: int) -> Optional[Teacher]:
        async with self.db() as session:
            result = await session.execute(select(Teacher).filter(Teacher.id == teacher_id))
            return result.scalars().first()

    async def filter_by_name(self, name: str, skip: int = 0, limit: int = 10) -> list[Teacher]:
        async with self.db() as session:
            result = await session.execute(select(Teacher).filter(func.lower(Teacher.name).like(f"%{name.lower()}%")).offset(skip).limit(limit))
            return result.scalars().all()


class LessonRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, lesson_id: int) -> Optional[Lesson]:
        async with self.db() as session:
            result = await session.execute(select(Lesson).filter(Lesson.id == lesson_id))
            return result.scalars().first()

    async def filters_(self, name: str, skip: int = 0, limit: int = 10,
                      subgroup_id: int = 0, group_id: int = 0, teacher_id: int = 0, audit_id: int = 0, lestype_id: int = 0) -> list[Lesson]:
        async with self.db() as session:
            query = select(Lesson).filter(func.lower(Lesson.discipline).like(f"%{name.lower()}%")).offset(skip).limit(limit)

            if subgroup_id:
                query = query.filter(Lesson.subgroup_id == subgroup_id)
            if group_id:
                query = query.filter(Lesson.group_id == group_id)
            if teacher_id:
                query = query.filter(Lesson.teacher_id == teacher_id)
            if audit_id:
                query = query.filter(Lesson.audit_id == audit_id)
            if lestype_id:
                query = query.filter(Lesson.type_id == lestype_id)
            result = await session.execute(query)
            lessons = result.scalars().all()
            return lessons


class GroupRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, group_id: int) -> Optional[Group]:
        async with self.db() as session:
            result = await session.execute(select(Group).filter(Group.id == group_id))
            return result.scalars().first()

    async def filter_by_name(self, name: str, skip: int = 0, limit: int = 10) -> list[Group]:
        async with self.db() as session:
            result = await session.execute(select(Group).filter(func.lower(Group.name).like(f"%{name.lower()}%")).offset(skip).limit(limit))
            return result.scalars().all()


class SubGroupRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, subgroup_id: int) -> Optional[SubGroup]:
        async with self.db() as session:
            result = await session.execute(select(SubGroup).filter(SubGroup.id == subgroup_id))
            return result.scalars().first()

    async def filter_by_name(self, name: str, skip: int = 0, limit: int = 10) -> list[SubGroup]:
        async with self.db() as session:
            result = await session.execute(select(SubGroup).filter(func.lower(SubGroup.name).like(f"%{name.lower()}%")).offset(skip).limit(limit))
            return result.scalars().all()


class TypesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, lestype_id: int) -> Optional[LesTypes]:
        async with self.db() as session:
            result = await session.execute(select(LesTypes).filter(LesTypes.id == lestype_id))
            return result.scalars().first()

    async def filter_by_name(self, name: str, skip: int = 0, limit: int = 10) -> list[LesTypes]:
        async with self.db() as session:
            result = await session.execute(select(LesTypes).filter(func.lower(LesTypes.name).like(f"%{name.lower()}%")).offset(skip).limit(limit))
            return result.scalars().all()
