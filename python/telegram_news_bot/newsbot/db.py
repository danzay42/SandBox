import os
from sqlalchemy import create_engine

host = os.getenv("PGHOST", "db")
port = os.getenv("PGPORT", 5432)
dbname = os.getenv("POSTGRES_DB", "postgres")
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "")
url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"


engine = create_engine(url)


