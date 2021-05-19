from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patient"
    __table_args__ = {"schema": "de"}

    managingorganization_id = Column(String(50))
    patient_id = Column(String(200), primary_key=True)
    gender = Column(String(50))
    identifier = Column(String(50))
    private_identifier = Column(String())
