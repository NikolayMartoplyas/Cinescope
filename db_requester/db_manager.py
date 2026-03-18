from db_requester.db_helpers import DBHelperUser
from db_requester.db_helpers import DBHelperMovies

class DBHelper:

    def __init__(self, db_session):
        self.user = DBHelperUser(db_session)
        self.movie = DBHelperMovies(db_session)