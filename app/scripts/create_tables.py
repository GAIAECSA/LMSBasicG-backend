from app.db.base import Base
from app.db.session import engine

from app.models.role import Role
from app.models.user import User
from app.models.category import Category
from app.models.subcategory import Subcategory
from app.models.course import Course
from app.models.module import Module
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.lesson_block_type import LessonBlockType
from app.models.enrollment import Enrollment

def create_tables():
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas 🚀")

if __name__ == "__main__":
    create_tables()