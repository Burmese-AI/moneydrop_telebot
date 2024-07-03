from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class QuestionBase(BaseModel):
    text: str
    answer: str
    choice1: str
    choice2: str
    choice3: str


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    questions: list[Question] = []

    class Config:
        orm_mode = True
