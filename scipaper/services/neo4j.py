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
        # Ensure the paper has a DOI before creating the node
        if not paper.doi:
            return

        # Create or merge the paper node
        tx.run("MERGE (p:Paper {doi: $doi}) "
               "SET p.title = $title",
               doi=paper.doi, title=paper.title)

        if paper.authors:
            for author in paper.authors:
                author_name = author.get('name')
                if author_name:
                    # Create or merge the author node
                    tx.run("MERGE (a:Author {name: $name})", name=author_name)
                    # Create the AUTHORED relationship
                    tx.run("MATCH (p:Paper {doi: $doi}), (a:Author {name: $name}) "
                           "MERGE (a)-[:AUTHORED]->(p)",
                           doi=paper.doi, name=author_name)

# Initialize the Neo4j service
neo4j_service = Neo4jService(settings.neo4j_uri, settings.neo4j_username, settings.neo4j_password)

# You can also add a function to get collaboration suggestions
def get_collaboration_suggestions(topic: str):
    # This is a placeholder for a more complex query
    # For now, we'll just return a list of authors who have written about the topic
    with neo4j_service._driver.session() as session:
        result = session.run("MATCH (a:Author)-[:AUTHORED]->(p:Paper) "
                             "WHERE toLower(p.title) CONTAINS toLower($topic) "
                             "RETURN a.name as author, count(p) as papers "
                             "ORDER BY papers DESC LIMIT 10", topic=topic)
        return [{"author": record["author"], "papers": record["papers"]} for record in result]
