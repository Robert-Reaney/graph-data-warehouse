from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import networkx as nx

from schemas import HealthResponse, DacisId
from utils import Neo4jDriver

# Instantiate and intialize API
app = FastAPI()
db = Neo4jDriver(URI="neo4j://neo4j_database")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://gpurhel8.mil.intellibridgelabs.io:3000", "http://10.100.1.26:3000"],  # Allow this origin (you can also use "*" to allow all origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (or specify: ["GET", "POST"])
    allow_headers=["*"],
)

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
    graph = db.jefferson_company_query(company_name)
    return graph

# utilities

@app.get('/health_check', tags=['utilities'])
def health_check() -> HealthResponse:
    return {'message': 'The API is healthy!'}