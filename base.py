from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


master_engine = create_engine('postgresql://postgres:3497279088@192.168.0.104:5432/football')
master_session = sessionmaker(bind=master_engine)

slave_engine = create_engine('postgresql://postgres:3497279088@192.168.0.110:5432/football')
slave_session = sessionmaker(bind=slave_engine)

Base = declarative_base()
