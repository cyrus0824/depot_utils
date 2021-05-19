from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()

class XRayInstance(Base):
    __tablename__ = "xray_instances_verified"
    __table_args__ = {"schema": "de"}

    series_instance_uid = Column(String(200), primary_key=True)
    patient_id = Column(String(200))
    identifier = Column(String(50))
    condition_id = Column(String(200))
    imagingstudy_id = Column(String(200))
    started = Column(DateTime())
    uid = Column(String(200))
    series_uid = Column(String(200))
    series_instance_content_url = Column(String(400))
    series_modality_cd = Column(String(50))
    status = Column(String(50))
    organization = Column(String(200))
