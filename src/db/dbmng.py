import sys
import os

if __package__:
    path_one = "c:\\Zaid\\Fun Projects -- Code\\URL_Shortener\\src\\db"
    path = os.path.dirname(path_one)
    if path not in sys.path:
        sys.path.append(path)
    if path_one not in sys.path:
        sys.path.append(path_one)
    from .base import Base, Session, engine
    from .url import URL
    from .users import Users
else:
    from base import Base, Session, engine
    from url import URL
    from users import Users


class DBMng:
    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    @classmethod
    def test_db(cls, engine, Session):
        Base.metadata.create_all(engine)
        cls.session = Session()

    def insert_user(self, usertype: bool, authkey: str):
        x = self.find_user(authkey)
        user = Users(usertype, authkey)
        if x != user:
            self.session.add(user)
            self.session.commit()
        else:
            return None

    def insert_url(self, short_url: str, long_url: str, time: str):
        x = self.find_short_url(long_url)
        url = URL(short_url, long_url, time)
        if x != url:
            self.session.add(url)
            self.session.commit()
        else:
            return None

    def find_short_url(self, longurl: str):
        x = self.session.query(URL).filter(URL.long_url == longurl).first()
        return x

    def find_user(self, authkey: str):
        x = self.session.query(Users).filter(Users.auth_key == authkey).first()
        return x

    def get_last_entry(self):
        x = (
            self.session.query(URL)
            .order_by(None)
            .order_by(URL.short_url.desc())
            .first()
        )
        return x

    def get_short_url(self, short_url: str):
        x = self.session.query(URL).get(short_url)
        return x

    def drop_url(self, short_url: str):
        x = self.get_short_url(short_url)
        if x is not None:
            self.session.delete(x)
            self.session.commit()
        else:
            return None


if __name__ == "__main__":
    main = DBMng()
    # main.insert_url("1", "https://www.google.com", "2020-01-01")
    #  x = main.get_short_url("1")
# x = main.get_last_entry()
# main.drop_url("1")
