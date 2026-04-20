from app.db.base import Base
from app.db.session import engine

from app.models.role import Role
from app.models.user import User

def create_tables():
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas 🚀")

if __name__ == "__main__":
    create_tables()