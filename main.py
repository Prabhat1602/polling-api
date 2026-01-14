from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Poll, Option, Vote
from schemas import PollCreate, VoteCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real-Time Polling API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Poll
@app.post("/polls")
def create_poll(data: PollCreate, db: Session = Depends(get_db)):
    poll = Poll(question=data.question)
    db.add(poll)
    db.commit()
    db.refresh(poll)

    for opt in data.options:
        db.add(Option(text=opt, poll_id=poll.id))

    db.commit()
    return {"poll_id": poll.id, "message": "Poll created"}

#  Get Poll Details
@app.get("/polls/{poll_id}")
def get_poll(poll_id: int, db: Session = Depends(get_db)):
    poll = db.query(Poll).filter(Poll.id == poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    result = {
        "id": poll.id,
        "question": poll.question,
        "options": []
    }

    for opt in poll.options:
        result["options"].append({
            "option_id": opt.id,
            "text": opt.text,
            "votes": len(opt.votes)
        })

    return result

# Vote
@app.post("/polls/{poll_id}/vote")
def vote(poll_id: int, data: VoteCreate, db: Session = Depends(get_db)):
    option = db.query(Option).filter(
        Option.id == data.option_id,
        Option.poll_id == poll_id
    ).first()

    if not option:
        raise HTTPException(status_code=400, detail="Invalid option")

    vote = Vote(
        user_id=data.user_id,
        poll_id=poll_id,
        option_id=data.option_id
    )

    try:
        db.add(vote)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="User has already voted on this poll"
        )

    return {"message": "Vote recorded"}
