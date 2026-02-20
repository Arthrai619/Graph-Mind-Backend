from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database as db
from graph_engine import GraphEngine

app = FastAPI(title="GraphMind AI Memory Engine")
graph = GraphEngine()
db.init_db()

def get_db():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.post("/register")
def register(username: str, password: str, session: Session = Depends(get_db)):
    if session.query(db.User).filter(db.User.username == username).first():
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_pw = db.get_password_hash(password)
    new_user = db.User(username=username, password=hashed_pw)
    session.add(new_user)
    session.commit()
    
    graph.sync_user(username)
    return {"message": "Success: User synced to Knowledge Graph"}

@app.post("/login")
def login(username: str, password: str, session: Session = Depends(get_db)):
    user = session.query(db.User).filter(db.User.username == username).first()
    if not user or not db.verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.post("/memory")
def create_memory(username: str, text: str):
    try:
        graph.add_memory(username, text)
        return {"status": "Memory Ingested into GraphMind"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/recall/{username}")
def recall_memories(username: str, limit: int = 10):
    try:
        # The engine queries the Graph for the user's personal context
        memories = graph.get_memories(username, limit)
        if not memories:
            return {"message": "No memories found for this user", "memories": []}
        
        return {
            "username": username,
            "memory_count": len(memories),
            "context": memories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recall Error: {str(e)}")