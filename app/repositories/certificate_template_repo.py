from sqlalchemy.orm import Session
from app.models.certificate_template import CertificateTemplate

def create(db: Session, certificate_template: CertificateTemplate):
    db.add(certificate_template)
    db.commit()
    db.refresh(certificate_template)
    return certificate_template

def update(db: Session, certificate_template: CertificateTemplate):
    db.merge(certificate_template)
    db.commit()
    db.refresh(certificate_template)
    return certificate_template

def delete(db: Session, certificate_template: CertificateTemplate):
    certificate_template.deleted = True
    db.merge(certificate_template)
    db.commit()
    return certificate_template

def get_by_id(db: Session, certificate_template_id: int):
    return db.query(CertificateTemplate).filter(CertificateTemplate.id == certificate_template_id, CertificateTemplate.deleted == False).first()

def get_all(db: Session):
    return db.query(CertificateTemplate).filter(CertificateTemplate.deleted == False).all()

def get_by_course(db: Session, course_id: int):
    return db.query(CertificateTemplate).filter(CertificateTemplate.course_id == course_id, CertificateTemplate.deleted == False).first()