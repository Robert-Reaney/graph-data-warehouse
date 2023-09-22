from scripts.helpers.queries import ImportHelper
import logging

logging.basicConfig(level=logging.INFO)

queries = ImportHelper()

queries.execute('constraints')
queries.execute('indicies')
queries.execute('dacis_companies')

queries.execute('sayari_entities')
queries.execute('sayari_ubos')

queries.execute('dacis_company_to_dod_budget')