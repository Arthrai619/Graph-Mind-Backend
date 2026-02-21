# 🧠 GraphMind: AI Memory Engine
**Version:** 1.0.0  
**Lead Developer:** Arth Rai (Backend & DevOps)

## 📌 Project Overview
GraphMind is a "beyond top-level" hybrid memory system designed for long-term AI context retention. It uses **PostgreSQL** as a secure Identity Vault and **Neo4j** as a Cognitive Memory engine to link user data, interests (like MERN stack and Competitive Programming), and research contexts (like Facial Expression Recognition).

---

## 🛠️ Infrastructure Setup
This project runs on Docker to ensure high availability and persistence.

1. **Prerequisites**: Ensure Docker and Docker Compose are installed.
2. **Environment**: Create a `.env` file in the root directory with the following:
   - `POSTGRES_USER/PASSWORD`
   - `NEO4J_AUTH=neo4j/graphpassword123`
   - `SECRET_KEY` (For JWT)
3. **Boot**: Run `docker-compose up -d`.
   - **PostgreSQL**: Accessible on port `5433`.
   - **Neo4j**: Accessible on port `7687` (Bolt) and `7474` (HTTP).

---

## 📡 API Endpoints (The "Conduits")

### 🔐 Identity Layer (Lead's Work)
- **POST `/register`**: Creates a SQL record and initializes a `User` node in the Graph.
- **POST `/login`**: Validates credentials against the Identity Vault.

### 🧠 Cognitive Layer (AI/Graph Team Integration)
- **POST `/memory`**: 
  - **Input**: `username`, `text`, `mood`.
  - **Action**: Ingests context into Neo4j and links it to the User node.
- **GET `/recall/{username}`**:
  - **Input**: `username`, `limit`.
  - **Action**: Returns a list of past memories for the LLM to use in conversation.

---

## 🤝 Team Interconnection
- **AI Lead**: Connects via the `/recall` endpoint to feed the LLM personal context.
- **Graph Lead**: Manages the `graph_engine.py` to add complex relationships like `WORKS_ON` or `INTERESTED_IN`.
- **DevOps (You)**: Monitors the health of containers and manages database security.
