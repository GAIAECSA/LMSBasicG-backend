from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.mdt_certificate import MdtCertificate
from app.models.user import User


def get_mdt_certificates_report_data(db: Session, course_id: int, certificate_type: str):
    """
    Obtiene los certificados de un curso y tipo específico, cruzándolos 
    con la tabla de usuarios mediante el número de identificación.
    """
    return (
        db.query(
            User.firstname.label("student_firstname"),
            User.lastname.label("student_lastname"),
            MdtCertificate.id_number.label("certificate_id_number"),
            MdtCertificate.certificate_type.label("certificate_type"),
            MdtCertificate.visited_at.label("visited_at"),
        )
        .select_from(MdtCertificate)
        .outerjoin(
            User,
            and_(
                MdtCertificate.id_number == User.idnumber,
                User.deleted.is_(False)
            )
        )
        .filter(
            MdtCertificate.course_id == course_id,
            MdtCertificate.certificate_type == certificate_type,
            MdtCertificate.deleted.is_(False),
        )
        .order_by(User.lastname.asc(), User.firstname.asc())
        .all()
    )