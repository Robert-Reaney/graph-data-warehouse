from neo4j import GraphDatabase
import logging

class ImportHelper:
    def __init__(self, URI = "neo4j://localhost"):
        self.uri = URI
        with GraphDatabase.driver(self.uri) as driver:
            driver.verify_connectivity()

    def execute(self, name):
        assert hasattr(self, name), f'query={name} not found'
        logging.info(f'executing query={name} logic:\n{getattr(self, name)}')
        with GraphDatabase.driver(self.uri) as driver:
            driver.verify_connectivity()
            query = getattr(self, name)
            for q in query.split(';'):
                if q == '\n':
                    continue
                driver.execute_query(q, database_='neo4j')

    refresh_db = "MATCH (n) DETACH DELETE n;"

    # contraints
    constraints = """
    CREATE CONSTRAINT FOR (c:Company) REQUIRE c.id IS UNIQUE;
    CREATE CONSTRAINT FOR (e:Entity) REQUIRE e.id IS UNIQUE;
    CREATE CONSTRAINT FOR (b:Budget) REQUIRE b.id IS UNIQUE;
    """

    indicies = """
    CREATE INDEX company_name FOR (c:Company) ON (c.name);
    """

    # dacis companies
    dacis_companies = """
    LOAD CSV WITH HEADERS FROM 'file:///gold_dacis_companies.csv' AS row
    CREATE (c:Company {name: row.company_name, id: row.dacis_id, cage_codes: row.cageCodes, in_nccs: coalesce(row.in_nccs, False), in_niss: coalesce(row.in_niss, False)})
    """

    # sayari entitiy
    sayari_entities = """
    LOAD CSV WITH HEADERS FROM 'file:///select_dacis_entities.csv' AS row
    WITH row, split(replace(replace(row.countries, '["', ''), '"]', ''), '","') AS countriesList

    MERGE (e:Entity {id: row.entity_id})

    SET e.name = row.label,
        e.countries = countriesList

    WITH row, e

    MATCH (c:Company {id: row.dacis_id})
    MERGE (c)-[s:IS_MATCH]->(e)
    """

    # sayari ubo
    sayari_ubos = """
    LOAD CSV WITH HEADERS FROM 'file:///select_ubos.csv' AS row
    WITH row, split(replace(replace(row.target_countries, '["', ''), '"]', ''), '","') AS countriesList

    MERGE (e:Entity {id: row.target_id})
    SET e.name = row.target_label,
        e.countries = countriesList,
        e.cosc = ANY(country IN countriesList WHERE country IN ['AFG', 'ARM', 'AZE', 'BLR', 'MMR', 'KHM', 'CAF', 'CHN', 'COG', 'CUB', 'CYP', 'ERI', 'GEO', 'HTI', 'IRN', 'IRQ', 'KAZ', 'LAO', 'LBN', 'LBY', 'MDA', 'MNG', 'PRK', 'PAK', 'RUS', 'SAU', 'SOM', 'SSD', 'SDN', 'SYR', 'TJK', 'TKM', 'UKR', 'UZB', 'VEN', 'VNM', 'YEM', 'ZWE'])
    
    WITH row, e

    MATCH (z:Entity {id: row.entity_id})
    CREATE (z)-[:HAS_UBO]->(e)
    """

    # sayari ubo edges

    # sayari dacis-entity edges
    
    # dacis dod budget

    # company to dod_budget
    dacis_company_to_dod_budget = """
    LOAD CSV WITH HEADERS FROM 'file:///silver_dacis_edges_companies_to_dod_budget.csv' AS row
    
    MERGE (b:Budget {id: row.dod_budget_id})
    ON CREATE SET b.title = row.budget_title,
        b.fiscal_year = row.fiscal_year,
        b.type = row.budget_type,
        b.lineno = row.budget_line_number

    WITH row, b
        
    MATCH (c:Company {id: row.company_id})
    MERGE (c)-[f:FUNDED_BY]->(b)
    SET f.fiscal_year = row.fiscal_year,
        f.type = row.budget_type
    """


    ### ACQUISITIONS STUFF ####
    # load cb/dacis map to give dacis companies a crunchbase uuid
    dacis_to_cb = """
    LOAD CSV WITH HEADERS FROM 'file:///gold_lookup_dacis_companies_to_cb.csv' AS row
    MATCH (c:Company {id: row.dacis_id})
    SET c.uuid = row.org_uuid
    """

    # load investor organizations and acquisition edges
    acquisitions = """
    LOAD CSV WITH HEADERS FROM 'file:///gold_crunchbase_acquisitions.csv' AS row

    MERGE (o:Organization {uuid: row.investor_uuid})
    ON CREATE SET o.name = row.investor_name,
        o.address = row.investor_address,
        o.country = row.investor_country_code,
        o.in_cosc = row.investor_cosc

    WITH row, o

    MATCH (c:Company {dacis_id: row.purchased_dacis_id})
    MERGE (o)-[i:INVESTED_IN {uuid: row.investment_uuid}]->(c)
    SET i.name = row.investment_name,
        i.updated_at = row.updated_at,
        i.created_at = row.created_at,
        i.price_usd = row.price_usd,
        i.type = row.investment_type
    """