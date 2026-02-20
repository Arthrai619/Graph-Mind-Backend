from neo4j import GraphDatabase

NEO4J_URI = "bolt://127.0.0.1:7687"
NEO4J_AUTH = ("neo4j", "graphpassword123")

class GraphEngine:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

    def sync_user(self, username: str):
        with self.driver.session() as session:
            session.run("MERGE (u:User {username: $username})", username=username)

    def add_memory(self, username: str, text: str):
        with self.driver.session() as session:
            query = """
            MATCH (u:User {username: $username})
            CREATE (m:Memory {content: $text, timestamp: datetime()})
            MERGE (u)-[:REMEMBERS]->(m)
            """
            session.run(query, username=username, text=text)
    def get_memories(self, username: str, limit: int = 10):
        with self.driver.session() as session:
            # This query starts at the User and finds all connected Memory nodes
            query = """
            MATCH (u:User {username: $username})-[:REMEMBERS]->(m:Memory)
            RETURN m.content AS content, m.timestamp AS time
            ORDER BY m.timestamp DESC
            LIMIT $limit
            """
            result = session.run(query, username=username, limit=limit)
            return [record["content"] for record in result]