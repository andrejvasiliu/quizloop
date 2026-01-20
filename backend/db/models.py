from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .db import Base
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


class User(Base):
    """User model representing a user in the system.

    Attributes:
        id: Primary key.
        username: Unique username of the user.
        email: Unique email of the user.
        password_hash: Hashed password.
        created_at: Timestamp of user creation (UTC).
        quizzes: Quizzes created by the user.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    quizzes = relationship("Quiz", back_populates="creator", cascade="all, delete")

    def set_password(self, password: str) -> None:
        self.password_hash = ph.hash(password)

    def check_password(self, password: str) -> bool:
        try:
            return ph.verify(self.password_hash, password)
        except VerifyMismatchError:
            return False

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username!r}, email={self.email!r})>"


class Quiz(Base):
    """Quiz model representing a quiz created by a user.

    Attributes:
        id: Primary key.
        title: Title of the quiz.
        description: Description of the quiz.
        created_at: Timestamp of quiz creation.
        user_id: Foreign key to the user who created the quiz.
        questions: List of questions in the quiz.
    """

    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="quizzes")

    questions = relationship(
        "Question", back_populates="quiz", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Quiz(id={self.id}, title={self.title!r}, user_id={self.user_id})>"


class Question(Base):
    """Question model representing a question in a quiz.

    Attributes:
        id: Primary key.
        text: Text of the question.
        quiz_id: Foreign key to the quiz this question belongs to.
        answers: List of answers for the question.
    """

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)

    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)

    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship(
        "Answer", back_populates="question", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Question(id={self.id}, text={self.text!r}, quiz_id={self.quiz_id})>"


class Answer(Base):
    """Answer model representing an answer to a question.

    Attributes:
        id: Primary key.
        text: Text of the answer.
        is_correct: Indicates if the answer is correct.
        question_id: Foreign key to the question this answer belongs to.
    """

    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)

    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    question = relationship("Question", back_populates="answers")

    def __repr__(self):
        return (
            f"<Answer(id={self.id}, text={self.text!r}, is_correct={self.is_correct})>"
        )
