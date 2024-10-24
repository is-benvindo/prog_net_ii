from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:senha@localhost/patrocars"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Atualize a importação
from sqlalchemy.orm import declarative_base  # Nova importação

Base = declarative_base()  # Não precisa mudar esta linha

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Adicione a criação das tabelas
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()  # Execute a criação das tabelas