🍬 Sweet Shop Management System

A full-stack Sweet Shop Management System built with FastAPI (Python) for the backend and React (Vite) for the frontend.

This project demonstrates skills in API development, database management, frontend implementation, testing, and modern workflows.

✨ Features
Backend (FastAPI + SQLModel)

Authentication (JWT-based)

POST /api/auth/register → Register new users

POST /api/auth/login → Login with username & password

Sweets Management

Add, list, search, update, and delete sweets

Purchase & restock sweets (with role-based restrictions: admin vs. user)

Database: SQLite (default), easily swappable with PostgreSQL/MySQL

Testing: pytest + httpx

Frontend (React + Vite)

Register & login forms

Dashboard with all sweets

Search & filter sweets

Purchase button (disabled if out of stock)

Admin controls (add, update, delete, restock)

📂 Project Structure
backend/
  app/                # FastAPI app (models, schemas, auth, crud, main)
  requirements.txt
  tests/              # pytest test suite
frontend/
  index.html
  package.json
  src/                # React components
scripts/
  run_backend.sh      # Helper script to start backend
README.md

🚀 Getting Started
1. Clone the repo
git clone https://github.com/rutujawagh1406/SweetShopManagement.git
cd SweetShopManagement

2. Backend setup
cd backend
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


API Docs: http://localhost:8000/docs

3. Frontend setup
cd frontend
npm install
npm run dev


Frontend: http://localhost:5173

4. Run tests
cd backend
pytest -q

🛠️ Troubleshooting

Dependency issues: Update pip → python -m pip install --upgrade pip

SQLModel errors: Ensure Python 3.10 or newer

JWT/auth issues: Set SECRET_KEY env variable before running backend

Port already in use: Change --port in uvicorn

📸 Screenshots

(add your screenshots here)
Example:

Login page

Dashboard with sweets

API docs

🤝 AI Collaboration

This project was built with assistance from AI tools (ChatGPT).

How AI was used

Bug fixes: Helped resolve relative import issues in main.py and database session handling in database.py.

Project structure: Suggested separating crud.py, schemas.py, and models.py for clarity.

Error handling: Recommended raising proper HTTP exceptions in endpoints.

Documentation: Generated this README and run instructions.

Git collaboration policy

As per the assignment rules, I’ve added AI as a co-author in commits where AI assistance was used.
Example commit message footer:

Co-authored-by: ChatGPT <AI@users.noreply.github.com>
