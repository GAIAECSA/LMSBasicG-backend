from sqlalchemy.orm import Session
from app.models.quizz_response import QuizzResponse

def create(db: Session, quizz_response: QuizzResponse):
    db.add(quizz_response)
    db.commit()
    db.refresh(quizz_response)
    return quizz_response

def update(db: Session, quizz_response: QuizzResponse):
    db.merge(quizz_response)
    db.commit()
    db.refresh(quizz_response)
    return quizz_response

def delete(db: Session, quizz_response: QuizzResponse):
    quizz_response.deleted = True
    db.merge(quizz_response)
    db.commit()
    return quizz_response

def get_by_id(db: Session, quizz_response_id: int):
    return db.query(QuizzResponse).filter(QuizzResponse.id == quizz_response_id, QuizzResponse.deleted == False).first()

def get_all_by_enrollment(db: Session, enrollment_id: int):
    return db.query(QuizzResponse).filter(QuizzResponse.deleted == False, QuizzResponse.enrollment_id == enrollment_id).all()
