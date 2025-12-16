# Full Stack Site Crawler Assignment

This project demonstrates a **full-stack implementation** of a site crawler login flow.
Users can choose a website, enter credentials, and view available deals from the target platform.

---

## 🧱 Architecture

- **Frontend**: React (Vite)
- **Backend**: Python FastAPI
- **External APIs**: altius.finance (FO1, FO2)

The backend acts as an **adapter layer**, normalizing upstream responses and errors.

---

## 🚀 Running the Backend

### 1. Create virtual environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
    pip install -r requirements.txt

### 3. Run server
    uvicorn main:app --reload --port 8000
    Or
    python3 main.py

## 🚀 Running the Frontend

### 1. Install dependencies

    cd frontend
    npm install

### 2. Run dev server
    npm run dev

## Frontend will be available at:
    http://localhost:5173