from neo4j import GraphDatabase

URI = "neo4j://localhost"

# QUERIES
refresh_db = "MATCH (n) DETACH DELETE n;"

#cb org columns
# 'uuid,name,type,permalink,cb_url,rank,created_at,updated_at,legal_name,roles,domain,homepage_url,country_code,state_code,region,city,
# address,postal_code,status,short_description,category_list,category_groups_list,num_funding_rounds,total_funding_usd,total_funding,
# total_funding_currency_code,founded_on,last_funding_on,closed_on,employee_count,email,phone,facebook_url,linkedin_url,twitter_url,logo_url,
# alias1,alias2,alias3,primary_role,num_exits\n'

# dacis_cb_map cols
# dacis_id,org_uuid,org_match_type,dacis_company_name,dacis_company_alt_name,dacis_formerly_known_as,dacis_parent_name,dacis_homepage_url,
# dacis_telfax,dacis_stock_tickers,cb_name,cb_legal_name,cb_domain,cb_homepage_url,cb_phone,cb_stock_exchange_symbol,cb_stock_symbol

# acq columns
# uuid,name,type,permalink,cb_url,rank,created_at,updated_at,acquiree_uuid,acquiree_name,acquiree_cb_url,acquiree_country_code,
# acquiree_state_code,acquiree_region,acquiree_city,acquirer_uuid,acquirer_name,acquirer_cb_url,acquirer_country_code,acquirer_state_code,
# acquirer_region,acquirer_city,acquisition_type,acquired_on,price_usd,price,price_currency_code

queries = [
    # dacis companies
    """
LOAD CSV WITH HEADERS FROM 'file:///gold_dacis_companies.csv' AS row
MERGE (c:Company {name: row.company_name, id: row.id, cage_codes: row.cageCodes, in_nccs: coalesce(row.in_nccs, False), in_niss: coalesce(row.in_niss, False)})
""",
    # load organizations
    """
LOAD CSV WITH HEADERS FROM 'file:///silver_crunchbase_organizations.csv' AS row
MERGE (o:Organization {uuid: row.uuid, name: row.name, country_code: row.country_code, address: row.address, domain: row.domain})
""",
    # load cb/dacis map to give dacis companies a crunchbase uuid
    """
LOAD CSV WITH HEADERS FROM 'file:///gold_lookup_dacis_companies_to_cb.csv' AS row
MATCH (c:Company {id: row.dacis_id})
SET c.uuid = row.org_uuid
""",
    # load acquisitions
    """
LOAD CSV WITH HEADERS FROM 'file:///bronze_crunchbase_acquisitions.csv' AS row
MATCH (o:Organization {uuid: row.acquirer_uuid})
MATCH (c:Company {uuid: row.acquiree_uuid})
MERGE (o)-[i:INVESTED_IN {uuid: row.uuid}]->(c)
SET i.name = row.name,
    i.type = row.type,
    i.updated_at = row.updated_at,
    i.created_at = row.created_at,
    i.price_usd = row.price_usd,
"""
    # load investor nodes
#     """
# LOAD CSV WITH HEADERS FROM 'file:///bronze_crunchbase_investors.csv' AS row
# WITH row WHERE NOT row.uuid IS NULL
# CREATE (i:Investor {uuid: row.uuid, name: row.name, type: row.type, country_code: row.country_code})
# """,
]

with GraphDatabase.driver(URI) as driver:
    driver.verify_connectivity()
    # driver.execute_query(refresh_db)

    for query in queries:
        driver.execute_query(query)



gold_acquisitions_query =     """
LOAD CSV WITH HEADERS FROM 'file:///gold_crunchbase_acquisitions_fixed.csv' AS row

WITH row WHERE NOT row.investment_uuid IS NULL AND NOT row.investor_uuid IS NULL

MERGE (o:Organization {uuid: row.investor_uuid})
ON CREATE SET o.name = row.investor_name,
    o.country = row.investor_country_code,
    o.in_cosc = row.investor_cosc

WITH row, o

MATCH (c:Company {dacis_id: row.purchased_dacis_id})
MERGE (o)-[i:INVESTED_IN {uuid: row.investment_uuid}]->(c)
SET i.name = row.investment_name,
    i.updated_at = row.updated_at,
    i.price_usd = row.price_usd,
    i.type = row.investment_type
"""