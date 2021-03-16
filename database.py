from sqlalchemy import create_engine, Column, ForeignKey, Float, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./candidates.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Candidate(Base):
    __tablename__ = "candidates"

    candidate_ref = Column(String(8), primary_key=True, index=True)
    name = Column(String, nullable=False)

    scores = relationship("CandidateScore", back_populates="candidate")


class CandidateScore(Base):
    __tablename__ = "score"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True)
    candidate_ref = Column(String(8), ForeignKey("candidates.candidate_ref"))
    score = Column(Float, nullable=False)

    candidate = relationship("Candidate", back_populates="scores")


Base.metadata.create_all(bind=engine)
