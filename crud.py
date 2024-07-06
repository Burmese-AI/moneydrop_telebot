from sqlalchemy.orm import Session

import models, schemas


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_category_by_name(db: Session, category_name: str):
    return (
        db.query(models.Category).filter(models.Category.name == category_name).first()
    )


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).offset(skip).limit(limit).all()


def create_question(db: Session, question: schemas.QuestionCreate, category_id: int):
    db_question = models.Question(**question.model_dump(), category_id=category_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
