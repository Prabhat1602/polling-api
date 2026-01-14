# Real-Time Polling System API

This project is a simple REST API for creating polls and casting votes in real time.  
It is built to demonstrate clean API design, relational database modeling, and safe handling of duplicate votes.

---

## Tech Stack

- **Language:** Python  
- **Framework:** FastAPI  
- **Database:** SQLite  
- **ORM:** SQLAlchemy  

---

## How to Run the App

### 1. Clone the Repository
```bash
git clone <your-github-repo-url>
cd polling-api



2. Create a Virtual Environment (Optional but Recommended)
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Mac / Linux

source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Start the Server
uvicorn main:app --reload

5. Access the API

API Base URL:

http://127.0.0.1:8000


Interactive Swagger Documentation:

http://127.0.0.1:8000/docs


The SQLite database file (polls.db) is created automatically on first run.

API Endpoints
Create a Poll

POST /polls

{
  "question": "What is your favorite tech?",
  "options": ["Go", "Node.js", "Python"]
}

Get Poll Details

GET /polls/{poll_id}

Returns the poll question, options, and current vote counts.

Cast a Vote

POST /polls/{poll_id}/vote

{
  "user_id": "user123",
  "option_id": 1
}

One Vote Per User Logic

To ensure that a user can vote only once per poll, the following approach is used:

Database-Level Enforcement

Votes are stored in a votes table

A unique constraint is applied on the combination of:

user_id

poll_id

UniqueConstraint("user_id", "poll_id", name="unique_user_poll")

Why This Works

The database guarantees that the same user cannot insert two votes for the same poll

Prevents race conditions

Efficient and scalable

No in-memory tracking required

If a user tries to vote again on the same poll, the database throws an error, which is safely handled and returned as a clear API response.