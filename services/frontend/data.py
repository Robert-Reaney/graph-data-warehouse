import neo4j
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from time import sleep
import logging
import networkx as nx

logging.basicConfig(level=logging.INFO)

class NeoData:
    def __init__(self, URI = "neo4j://neo4j_database"):
        self.uri = URI
        self.graph = None
        sleep(5)
        for ii in range(30):
            try:
                with GraphDatabase.driver(self.uri) as driver:
                    driver.verify_connectivity()
                break
            except ServiceUnavailable:
                print('Waiting for neo4j standup...')
                sleep(1)

    def query(self, string):
        with GraphDatabase.driver(self.uri) as driver:
            result = driver.execute_query(string, database_='neo4j', result_transformer_= neo4j.Result.graph)
        return result

    def ubo_query(self, dacis_id):
        # TODO you aren't supposed to inject variables like this but the correct way wasn't working ngb 
        query = f"""
        MATCH (c:Company)-[m:IS_MATCH]->(e:Entity)-[u:HAS_UBO]->(ue:Entity)
        WHERE c.id = '{dacis_id}' AND ue.cosc = true
        RETURN c,m,e,u,ue;"""

        with GraphDatabase.driver(self.uri) as driver:
            result = driver.execute_query(query, database_='neo4j', result_transformer_= neo4j.Result.graph)
        

        nodes = [{'data': {'id': node._properties['id'], 'label': node._properties['name']}, 'classes': ' '.join([x.lower() for x in list(node.labels)])} for node in result.nodes]
        edges = [{'data': {'source': edge.start_node._properties['id'], 'target': edge.end_node._properties['id'], 'label': edge.type}} for edge in result.relationships]

        # logging.info(nodes)
        # logging.info(edges)

        return nodes + edges
    
    def test_ubo(self, dacis_id):
        # TODO you aren't supposed to inject variables like this but the correct way wasn't working ngb 
        query = f"""
        MATCH (c:Company)-[m:IS_MATCH]->(e:Entity)-[u:HAS_UBO]->(ue:Entity)
        WHERE c.id = '{dacis_id}' AND ue.cosc = true
        RETURN c,m,e,u,ue;"""

        with GraphDatabase.driver(self.uri) as driver:
            result = driver.execute_query(query, database_='neo4j', result_transformer_= neo4j.Result.graph)
        
        return self.netx_to_dash(self.cypher_to_netx(result))
        

    def cypher_to_netx(self, cypher_result):
        G = nx.MultiDiGraph()

        for node in cypher_result._nodes.values():
            G.add_node(node._properties['id'], labels=node._labels, properties=node._properties)

        for edge in cypher_result._relationships.values():
            G.add_edge(edge.start_node._properties['id'], edge.end_node._properties['id'], type=edge.type, properties=edge._properties)

        return G
    
    def netx_to_dash(self, netx):
        json = nx.readwrite.json_graph.cytoscape_data(netx)
        nodes = [
            {'data': {'id': node['data']['properties']['id'], 'label': node['data']['properties']['name']}, 'classes': ' '.join([x.lower() for x in node['data']['labels']])} for node in json['elements']['nodes']
        ]
        
        edges = json['elements']['edges']
        for ii, edge in enumerate(edges):
            edges[ii]['data']['label'] = edge['data']['type']
    

        return nodes + edges

        # nodes = [{'data': {'id': node._properties['id'], 'label': node._properties['name']}, 'classes': } for node in result.nodes]
        # edges = [{'data': {'source': edge.start_node._properties['id'], 'target': edge.end_node._properties['id'], 'label': edge.type}} for edge in result.relationships]



# for node in result.nodes:
#     print(list(node.labels))

    # def execute(self, name):
    #     assert hasattr(self, name), f'query={name} not found'
    #     logging.info(f'executing query={name} logic:\n{getattr(self, name)}')
    #     with GraphDatabase.driver(self.uri) as driver:
    #         driver.verify_connectivity()
    #         query = getattr(self, name)
    #         for q in query.split(';'):
    #             if q == '\n':
    #                 continue
    #             driver.execute_query(q, database_='neo4j')