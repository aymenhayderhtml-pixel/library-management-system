import os
import sys

# Add the project root to path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import db_session, UserModel
def make_admin(username: str):
    """Promote a user to admin by username."""
    user = db_session.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        print(f"User '{username}' not found.")
        return False
    user.role = "admin"
    db_session.commit()
    print(f"User '{username}' promoted to admin.")
    return True
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m app.utils.make_admin <username>")
        sys.exit(1)
    username = sys.argv[1]
    success = make_admin(username)
    sys.exit(0 if success else 1)