from typing import Optional
from app.database import db_session, UserModel
def save_user(user: dict) -> dict:
    # user dict must contain username, password_hash, role
    db_user = UserModel(**user)
    db_session.add(db_user)
    db_session.commit()
    return user_to_dict(db_user)
def get_user_by_username(username: str) -> Optional[dict]:
    u = db_session.query(UserModel).filter_by(username=username).first()
    return user_to_dict(u) if u else None
def user_to_dict(u: UserModel) -> dict:
    return {
        "id": u.id,
        "username": u.username,
        "password_hash": u.password_hash,
        "role": u.role,
    }