import asyncio
from datetime import datetime

from sqlalchemy import delete, text, select
from database import async_session_factory
from values import *
from models import SubGroup, Lesson, LesTypes, Group, Auditory, Teacher


def rplc_name(name) -> str:
    """Замена имени группы"""
    return name.lower().strip().replace('-', '')


async def mn():
    """Интеграция"""

    def CrtDct(ks, vls):
        """Костылим и умеем"""
        dct = {}
        vls += [None] * max(0, len(ks) - len(vls))
        for i in range(len(ks)):
            dct[ks[i]] = vls[i]
        return dct

    async with async_session_factory() as sess:
        await sess.execute(delete(Lesson))
        await sess.execute(delete(SubGroup))
        await sess.execute(text(f"""ALTER SEQUENCE {SubGroup.__tablename__}_id_seq RESTART WITH 1;"""))

        sess.add_all([SubGroup(**CrtDct(["name", "smile"], list(els))) for els in subgr])
        await sess.commit()
        with_ids = await sess.execute(select(SubGroup).order_by(SubGroup.name))
        dct_sbg = {gr.name: gr for gr in with_ids.scalars().all()}

    async with async_session_factory() as sess:
        await sess.execute(delete(LesTypes))
        await sess.execute(text(f"""ALTER SEQUENCE {LesTypes.__tablename__}_id_seq RESTART WITH 1;"""))

        sess.add_all([LesTypes(**CrtDct(["name", "smile"], list(els))) for els in lestp])
        await sess.commit()
        with_ids = await sess.execute(select(LesTypes).order_by(LesTypes.name))
        dct_ltp = {gr.name: gr for gr in with_ids.scalars().all()}

    async with async_session_factory() as sess:
        await sess.execute(delete(Group))
        await sess.execute(text(f"""ALTER SEQUENCE {Group.__tablename__}_id_seq RESTART WITH 1;"""))

        sess.add_all([Group(**CrtDct(["name", "title_name"], [rplc_name(els[0]), els[0]])) for els in grps])
        await sess.commit()
        with_ids = await sess.execute(select(Group).order_by(Group.name))
        dct_grp = {gr.title_name: gr for gr in with_ids.scalars().all()}

    async with async_session_factory() as sess:
        await sess.execute(delete(Teacher))
        await sess.execute(text(f"""ALTER SEQUENCE {Teacher.__tablename__}_id_seq RESTART WITH 1;"""))
        sess.add_all([Teacher(**CrtDct(["name", "smile"], list(els))) for els in tch])
        await sess.commit()
        with_ids = await sess.execute(select(Teacher).order_by(Teacher.name))
        dct_tch = {tc.name: tc for tc in with_ids.scalars().all()}

    async with async_session_factory() as sess:
        await sess.execute(delete(Auditory))
        await sess.execute(text(f"""ALTER SEQUENCE {Auditory.__tablename__}_id_seq RESTART WITH 1;"""))
        sess.add_all([Auditory(**CrtDct(["name"], list(els))) for els in audits])
        await sess.commit()
        with_ids = await sess.execute(select(Auditory).order_by(Auditory.name))
        dct_aud = {tc.name: tc for tc in with_ids.scalars().all()}

    def prs_to_ids(elems):
        """Fix to ids"""
        elems[2] = dct_grp.get(elems[2]).id
        elems[3] = dct_sbg.get(elems[3]).id
        elems[5] = dct_ltp.get(elems[5]).id
        elems[6] = dct_tch.get(elems[6]).id
        elems[7] = dct_aud.get(elems[7]).id
        elems[-2] = datetime.strptime(elems[-2], "%H:%M").time()
        elems[-1] = datetime.strptime(elems[-1], "%H:%M").time()
        return elems

    async with async_session_factory() as sess:
        await sess.execute(delete(Lesson))
        await sess.execute(text(f"""ALTER SEQUENCE {Lesson.__tablename__}_id_seq RESTART WITH 1;"""))
        sess.add_all([Lesson(**CrtDct("number_day,order_in_day,group_id,subgroup_id,discipline,type_id,teacher_id,audit_id,time_start,time_finish".split(','),
                                      prs_to_ids(list(els)))) for els in lessons])
        await sess.commit()
        with_ids = await sess.execute(select(Auditory).order_by(Auditory.name))
        dct_aud = {tc.name: tc.id for tc in with_ids.scalars().all()}

if __name__ == '__main__':
    asyncio.run(mn())
