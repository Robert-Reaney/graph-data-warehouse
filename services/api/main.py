from fastapi import FastAPI
import networkx as nx

from schemas import HealthResponse, DacisId
from utils import Neo4jDriver

# Instantiate and intialize API
app = FastAPI()
db = Neo4jDriver(URI="neo4j://neo4j_database")

# active

@app.get('/companies/{company_name}')
def get_company(company_name: str):
    """
    Retrieve a company-centric graph by their name.

    - **company_name**: Name of the company to fetch.
    """
    return db.get_company_by_name(company_name)

# deprecated

@app.get('/search/company/{company_name}', tags=["deprecated"])
def search_company(company_name: str):
    return db.get_company_by_name(company_name)

# utilities

@app.get('/health_check', tags=['utilities'])
def health_check() -> HealthResponse:
    return {'message': 'The API is healthy!'}