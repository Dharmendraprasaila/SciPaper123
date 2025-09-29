from neo4j import GraphDatabase
from scipaper.config import settings
from scipaper.schemas import Paper

class Neo4jService:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def add_paper_and_authors(self, paper: Paper):
        with self._driver.session() as session:
            session.execute_write(self._create_paper_and_authors, paper)

    @staticmethod
    def _create_paper_and_authors(tx, paper: Paper):
        if not paper.doi:
            return

        tx.run("MERGE (p:Paper {doi: $doi}) SET p.title = $title",
               doi=paper.doi, title=paper.title)

        if paper.authors:
            for author in paper.authors:
                author_name = author.get('name')
                if author_name:
                    tx.run("MERGE (a:Author {name: $name})", name=author_name)
                    tx.run("MATCH (p:Paper {doi: $doi}), (a:Author {name: $name}) "
                           "MERGE (a)-[:AUTHORED]->(p)",
                           doi=paper.doi, name=author_name)

    def get_collaboration_suggestions(self, topic: str):
        with self._driver.session() as session:
            result = session.run("MATCH (a:Author)-[:AUTHORED]->(p:Paper) "
                                 "WHERE toLower(p.title) CONTAINS toLower($topic) "
                                 "RETURN a.name as author, count(p) as papers "
                                 "ORDER BY papers DESC LIMIT 10", topic=topic)
            return [{"author": record["author"], "papers": record["papers"]} for record in result]

# --- Singleton Pattern for Neo4j Service ---
neo4j_service_instance = None

def get_neo4j_service():
    global neo4j_service_instance
    if neo4j_service_instance is None:
        neo4j_service_instance = Neo4jService(
            settings.neo4j_uri, 
            settings.neo4j_username, 
            settings.neo4j_password
        )
    return neo4j_service_instance
