from app.db.base import Base
from app.db.session import engine
from app.models.attendance import Attendance
from app.models.block_progress import BlockProgress
from app.models.business import Business
from app.models.business_lms_config import BusinessLmsConfig
from app.models.category import Category
from app.models.certificate import Certificate
from app.models.certificate_template import CertificateTemplate
from app.models.course import Course
from app.models.course_attendance import CourseAttendance
from app.models.enrollment import Enrollment
from app.models.forum_response import ForumResponse
from app.models.homework_response import HomeworkResponse
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.lesson_block_type import LessonBlockType
from app.models.lms_config import LmsConfig
from app.models.mdt_certificate import MdtCertificate
from app.models.module import Module
from app.models.privacy_policy import PrivacyPolicy
from app.models.quizz_response import QuizzResponse
from app.models.role import Role
from app.models.subcategory import Subcategory
from app.models.survey_response import SurveyResponse
from app.models.user import User
from app.models.user_privacy_policy import UserPrivacyPolicy
from app.models.zoom_meeting import ZoomMeeting


def create_tables():
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas 🚀")


if __name__ == "__main__":
    create_tables()
