from contextvars import ContextVar
from datetime import datetime, timedelta
from auth.crud import Crud
import uuid
import bcrypt
user_session: ContextVar[None] = ContextVar('user_session', default=None)

def current_user():
    return user_session.get()

def validate_token(token):
    try:
        crud = Crud()
        client_id = crud.get_user_by_token(token=token)
        if (len(client_id) == 0):
            return False
        user_session.set(client_id[0][0])
        return  True
    except Exception as e:
        return False


def create_access_token():
    return str(uuid.uuid4())

def generate_password(password):
    salt = bcrypt.gensalt()
    hashcoded = bcrypt.hashpw(password.encode(), salt)
    return hashcoded