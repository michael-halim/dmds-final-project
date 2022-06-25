from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
load_dotenv()

class Neo4jConnector:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # read_transaction to read and write_transaction to write.
    # but as we load the database manually i assume we just read

    # for select box
    def get_member_names(self):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_names)
            result.sort()
            return result

    def get_member_names_by_id(self,user_id):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_names_by_id,user_id)
            return result
            
    @staticmethod
    def _find_and_return_names_by_id(tx,user_id):
        # get the suppliers' companyNames only
        query = '''
                MATCH (n)
                WHERE ID(n) = $id
                RETURN n.nama as Name
        '''
        result = tx.run(query,id=user_id)
        return [record["Name"] for record in result]

    @staticmethod
    def _find_and_return_names(tx):
        # get the suppliers' companyNames only
        query = '''
                MATCH (u:USER)
                RETURN u.nama as Name
        '''
        result = tx.run(query)
        return [record["Name"] for record in result]

    def get_member_parent(self, memberName):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_parent, memberName)
            # for i in range(len(result)):
            #     print(result[i]["parentName"])
            return result[0]["parentName"]

    @staticmethod
    def _find_and_return_parent(tx, memberName):
        query = '''
                match (u:USER)-[:CHILD_OF]->(p)
                where u.nama = $nama
                return p.nama as parentName
        '''
        result = tx.run(query, nama=memberName)
        return [record for record in result]

    def get_member_forefathers(self, memberName):
        # forefathers one and all! bear witness!
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_forefathers, memberName)
            return result

    @staticmethod
    def _find_and_return_forefathers(tx, memberName):
        query = '''
                match (u:USER)-[:CHILD_OF]->(f)-[:CHILD_OF]->(gf)-[:CHILD_OF]->(ggf)
                where u.nama = $nama
                return f.nama as Father, gf.nama as Grandfather, ggf.nama as GreatGrandfather
        '''
        result = tx.run(query, nama=memberName)
        lineage = [record for record in result]

        # ugly
        if lineage == []:
            query = '''
                match (u:USER)-[:CHILD_OF]->(f)-[:CHILD_OF]->(gf)
                where u.nama = $nama
                return f.nama as Father, gf.nama as Grandfather
        '''
            result = tx.run(query, nama=memberName)
            lineage = [record for record in result]

        # uglier but it stops here
        if lineage == []:
            query = '''
                match (u:USER)-[:CHILD_OF]->(f)
                where u.nama = $nama
                return f.nama as Father
            '''
            result = tx.run(query, nama=memberName)
            lineage = [record for record in result]
        return lineage

    def get_member_children(self, memberName):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_children, memberName)
            return result

    @staticmethod
    def _find_and_return_children(tx, memberName):
        query = '''
                match (u:USER)-[:LEADERS_OF]->(ou:USER)
                where u.nama = $member
                return ou.nama as names
        '''
        result = tx.run(query, member=memberName)
        return [record for record in result]

    def get_shortest_path(self, memberName):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_shortest_path, memberName)
            return result

    @staticmethod
    def _find_and_return_shortest_path(tx, memberName):
        query = '''
                match(u:USER{nama:$name}), (company:COMPANY),p = shortestPath((u)-[*]-(company))
                return p as shortestPath  
        '''
        result = tx.run(query, name=memberName)
        return [record for record in result]

    def get_shortest_path_by_ID(self, memberID):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_parents, memberID)
            idlist = []
            for record in result:
                nodes = record["shortestPath"].nodes
                for node in nodes:
                    idlist.append(node.id)
            return idlist

    @staticmethod
    def _find_and_return_parents(tx, memberID):
        query = '''
            match(u:USER), (company:COMPANY),p = shortestPath((u)-[*]-(company))
            where id(u) = $id
            return p as shortestPath  
        '''
        result = tx.run(query, id=memberID)
        return [record for record in result]


    def saysomething(self):
        return "im giving up on you :("

    def saysomeotherthing(self):
        return "death beckons at us all"


neo4j_client = Neo4jConnector("bolt://localhost:7687", os.environ.get('USER_NEO4J'), os.environ.get('PASSWORD_NEO4J'))
# result = neo4j_client.get_shortest_path('Jaylen Green')
# print(result)
# # print(shortestPath)
# for record in result:
#     nodes = record["shortestPath"].nodes
#     for node in nodes:
#         print(node.id)

# father = neo4j_client.get_member_parent("Paul Wright")
# print(father)
# royalLineage = neo4j_client.get_member_forefathers("Paul Wright")
# print(royalLineage[0]["Father"])
# neo4j_client.get_company_names()
# #greeter.get_company_competitors("Zaanse Snoepfabriek")
# neo4j_client.close()
