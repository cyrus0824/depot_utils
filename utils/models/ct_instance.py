from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer

Base = declarative_base()

class CTInstance(Base):
    __tablename__ = "ct_instances_verified"
    __table_args__ = {"schema": "de"}

    series_instance_uid = Column(String(200), primary_key=True)
    patient_id = Column(String(200))
    condition_id = Column(String(200))
    started = Column(DateTime())
    uid = Column(String(200))
    series_uid = Column(String(200))
    series_instance_content_url = Column(String(400))
    series_instance_number = Column(Integer)
