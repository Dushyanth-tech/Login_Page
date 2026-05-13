from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine,Column,Integer,String

URL="postgresql+psycopg2://postgres:root@localhost:5432/sample"

engine=create_engine(URL)
base=declarative_base()
SessionLocal=sessionmaker(bind=engine)

class User(base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    email=Column(String)
    password=Column(String)



