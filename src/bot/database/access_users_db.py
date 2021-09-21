import datetime
from typing import Union, List

from sqlalchemy import select

import bot.database.db_models as db


def get_all_users(session=db.open_session()) -> Union[List[db.Users], None]:
    """ Get all users from db """

    return [entry[0] for entry in session.execute(select(db.Users)).all()]


def get_user_by_id(user_id: int, session=db.open_session()):

    statement = select(db.Users).where(db.Users.user_id == user_id)
    entry = session.execute(statement).first()
    return entry[0] if entry else None


def add_user(user_id: int, username: str,
             sent_messages=0, join_date=datetime.datetime.now(), is_verified=False, session=db.open_session()):
    user = db.Users(user_id=user_id, username=username,
                    sent_messages=sent_messages, join_date=join_date, is_verified=is_verified)
    session.add(user)
    session.commit()
    session.close()
