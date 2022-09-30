from ast import Del
import sys
import os

if __package__:
    parentdir = os.path.dirname(__file__)
    rootdir = os.path.dirname(parentdir)
    if rootdir not in sys.path:
        sys.path.append(rootdir)
    if parentdir not in sys.path:
        sys.path.append(parentdir)
    from .url import URL
    from .users import Users
    from .delStack import DelStack


def insert_user(session, usertype: bool, authkey: str):
    x = find_user(session, authkey)
    user = Users(usertype, authkey)
    if x is None:
        session.add(user)
        session.commit()
        return user
    # elif x.auth_key != user.auth_key:
    #     session.add(user)
    #     session.commit()
    #     return user
    else:
        return None


def insert_url(session, short_url: str, long_url: str, time: str):
    x = find_short_url(session, long_url)
    url = URL(short_url, long_url, time)
    if x is None:
        session.add(url)
        session.commit()
        return url
    # elif x.long_url != url.long_url:
    #     session.add(url)
    #     session.commit()
    #     return url
    else:
        return None


def find_short_url(session, longurl: str):
    x = session.query(URL).filter(URL.long_url == longurl).first()
    return x


def find_user(session, authkey: str):
    x = session.query(Users).filter(Users.auth_key == authkey).first()
    return x


def get_last_entry(session):
    x = session.query(URL).order_by(None).order_by(URL.short_url.desc()).first()
    return x


def get_short_url(session, short_url: str):
    x = session.query(URL).get(short_url)
    return x


def drop_url(session, long_url: str):
    droppedObject = find_short_url(session, long_url)
    if droppedObject is not None:
        session.delete(droppedObject)
        session.commit()
        return droppedObject
    else:
        return None


def popDelStack(session):
    topElement = session.query(DelStack).first()
    if topElement is not None:
        session.delete(topElement)
        session.commit()
        return topElement
    else:
        return None


def pushDelStack(session, shortUrl):

    rowDelStack = DelStack(shortUrl)

    session.add(rowDelStack)
    session.commit()
    return shortUrl
