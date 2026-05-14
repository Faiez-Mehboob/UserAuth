from sqlalchemy import create_engine, Column, Integer, String, BLOB
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import BYTEA
import os

curr_dir=os.path.dirname(os.path.abspath(__file__))

db_url= os.path.join(curr_dir,'UserAuth.db')
try:
    engine = create_engine(f'sqlite:///{db_url}')
except Exception as e:
    print(f"Error Connecting to DB: {e}\n")

Base = declarative_base()

class User(Base):
    __tablename__= "users"
    
    id = Column(Integer, primary_key=True)
    username= Column(String)
    passwd= Column(BLOB)
        
Base.metadata.create_all(engine)