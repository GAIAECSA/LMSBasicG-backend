from sqlalchemy.orm import Session
from app.models.certificate import Certificate

def create(db: Session, certificate: Certificate):
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    return certificate

def update(db: Session, certificate: Certificate):
    db.merge(certificate)
    db.commit()
    db.refresh(certificate)
    return certificate

def delete(db: Session, certificate: Certificate):
    certificate.deleted = True
    db.merge(certificate)
    db.commit()
    return certificate

def get_by_id(db: Session, certificate_id: int):
    return db.query(Certificate).filter(Certificate.id == certificate_id, Certificate.deleted == False).first()

def get_all(db: Session):
    return db.query(Certificate).filter(Certificate.deleted == False).all()

def get_by_course(db: Session, course_id: int):
    return db.query(Certificate).filter(Certificate.course_id == course_id, Certificate.deleted == False).first()