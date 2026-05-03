# Task Manager API 
 
REST service for project and task management built with FastAPI. 
 
## Features 
- JWT authentication (registration, login) 
- CRUD operations for projects and tasks 
- Workload analysis for team members 
- Algorithm for optimal task assignment 
- Email notifications and deadline tracking 
- 10 automated tests 
 
## Technologies 
- FastAPI, SQLAlchemy, SQLite 
- JWT (python-jose), Pydantic, Pytest 
 
## Quick Start 
 
1. Clone the repository: 
git clone https://github.com/snegyrka/task-manager.git 
cd task-manager 
 
2. Create virtual environment: 
python -m venv venv 
venv\Scripts\activate 
 
3. Install dependencies: 
pip install -r requirements.txt 
 
4. Run server: 
uvicorn app.main:app --reload 
 
5. Open http://localhost:8000/docs 
 
## Tests 
pytest tests/test_main.py -v 
 
## Pylint Score 
7.60/10 
 
## Author 
