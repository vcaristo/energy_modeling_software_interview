from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

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