from os import environ

CFDB_PORT = environ.get("CFDB_PORT", 5431)
CFDB_HOST = environ.get("CFDB_HOST", 'localhost')
CFDB_USER = environ.get("CFDB_USER", 'postgres')
CFDB_PASSWORD = environ.get("CFDB_PASSWORD", 'postgres')
CFDB_NAME = environ.get("CFDB_NAME", 'cfb_rankings')
CONNECTION_STRING = f"dbname={CFDB_NAME} user={CFDB_USER} password={CFDB_PASSWORD} host={CFDB_HOST} port={CFDB_PORT}"
BEARER = environ.get("BEARER")
