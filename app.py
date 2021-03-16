import csv
import io

from collections import defaultdict

import sqlalchemy

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Candidate, CandidateScore, Base, SessionLocal, engine


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CandidateScoreData(BaseModel):
    score: float


def get_candidate_scores(db: Session):
    cand_scores = (
        db.query(Candidate, CandidateScore)
        .join(CandidateScore)
        .order_by(Candidate.candidate_ref.desc())
        .all()
    )

    outdict = defaultdict(lambda: defaultdict(list))
    for cand, score in cand_scores:
        outdict[cand.candidate_ref][cand.name].append(score.score)

    header = ["candidate_name", "candidate_ref", "score_1", "score_2", "score_3"]
    outlist = [[list(v.keys())[0], k, *list(v.values())[0]] for k, v in outdict.items()]
    out_data = io.StringIO()
    writer = csv.writer(out_data)
    writer.writerow(header)
    writer.writerows(outlist)

    return out_data.getvalue()


def add_score(db: Session, candidate_ref: str, score: float):
    try:
        score_obj = CandidateScore(candidate_ref=candidate_ref, score=score)
        db.add(score_obj)
        db.commit()
        db.refresh(score_obj)
    except sqlalchemy.exc.IntegrityError as err:
        if "NOT NULL constraint failed" in str(err):
            db.rollback()


def add_candidate(db: Session, candidate_ref: str, name: str):
    try:
        candidate_obj = Candidate(candidate_ref=candidate_ref, name=name)
        db.add(candidate_obj)
        db.commit()
        db.refresh(candidate_obj)
    except sqlalchemy.exc.IntegrityError:
        db.rollback()


@app.post("/create-candidates/")
def create_candidates(db: Session = Depends(get_db), candidates: dict = None):
    for row in candidates["data"]:
        add_candidate(db, row["candidate_ref"], row["name"])
        add_score(db, row["candidate_ref"], row["score"])

    return "Added"


@app.get("/get-candidates/")
def read_users(db: Session = Depends(get_db)):
    data = get_candidate_scores(db)
    response = StreamingResponse(iter([data]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response
