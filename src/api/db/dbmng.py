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
else:
    from url import URL
    from users import Users


def insert_user(session, usertype: bool, authkey: str):
    x = find_user(session, authkey)
    user = Users(usertype, authkey)
    if x != user:
        session.add(user)
        session.commit()
    else:
        return None


def insert_url(session, short_url: str, long_url: str, time: str):
    x = find_short_url(session, long_url)
    url = URL(short_url, long_url, time)
    if x != url:
        session.add(url)
        session.commit()
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


def drop_url(session, short_url: str):
    x = get_short_url(session, short_url)
    if x is not None:
        session.delete(x)
        session.commit()
    else:
        return None


if __name__ == "__main__":
    insert_url("1", "https://www.google.com", "2020-01-01")
    x = get_short_url("1")
# x = main.get_last_entry()
# main.drop_url("1")
