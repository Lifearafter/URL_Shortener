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


def insert_user(session, usertype: bool, authkey: str):
    x = find_user(session, authkey)
    user = Users(usertype, authkey)
    if x is None:
        session.add(user)
        session.commit()
        return user
    elif x.auth_key != user.auth_key:
        session.add(user)
        session.commit()
        return user
    else:
        return None


def insert_url(session, new_url: URL):
    stored_match = find_url_given_long(session, new_url.long_url)
    # Not stored yet, insert it
    if stored_match is None:
        session.add(new_url)
        session.commit()
        return new_url
    # long_url doesn't match stored long_url, update it
    elif stored_match.long_url != new_url.long_url:
        session.add(new_url)
        session.commit()
        return new_url
    # a map is already stored in the db
    return None


def find_url_given_long(session, longurl: str) -> URL | None:
    '''Find the stored URL object given the original long URL (stripped of protocol) as a key'''
    return session.query(URL).filter(URL.long_url == longurl).first()


def find_user(session, authkey: str):
    return session.query(Users).filter(Users.auth_key == authkey).first()


def get_last_entry(session):
    return session.query(URL).order_by(None).order_by(URL.short_url.desc()).first()


def get_short_url(session, short_url: str):
    return session.query(URL).get(short_url)


def drop_url(session, short_url: str):
    stored_short_url = get_short_url(session, short_url)
    if stored_short_url is not None:
        session.delete(stored_short_url)
        session.commit()
    else:
        return None
