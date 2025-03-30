from sqlalchemy import Column, Integer, String, Date, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String)

    def __repr__(self):
        return f"<Project(id={self.id}, title={self.title})>"
    

class Measure(Base):
    __tablename__ = 'measure'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'))
    measure_type = Column(String)
    install_date = Column(Date)

    def __repr__(self):
        return f"<Measure(id={self.id}, type={self.measure_type})>"


# Set up SQLite DB session - OS independent

# db is two levels up from models.py
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
db_path = os.path.join(BASE_DIR, 'db', 'application_example.db')
engine = create_engine(f'sqlite:///{db_path}')

# single db session for the web app -- may want to move for concurrency features
Session = sessionmaker(bind=engine)  
session = Session()