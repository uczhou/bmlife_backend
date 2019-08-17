from db_utils.base import Base
from sqlalchemy import Column, Integer, Text


class CrimeSpot(Base):
    __tablename__ = 'crimespot'

    gid = Column(Integer, autoincrement=True, primary_key=True)

    address_1 = Column(Text, nullable=True)
    case_number = Column(Text, nullable=True)
    city = Column(Text, nullable=True)
    clearance_type = Column(Text, nullable=True)
    created_at = Column(Text, nullable=True)
    day_of_week = Column(Text, nullable=True)
    hour_of_day = Column(Text, nullable=True)
    incident_datetime = Column(Text, nullable=True)
    incident_description = Column(Text, nullable=True)
    incident_id = Column(Text, nullable=True)
    incident_type_primary = Column(Text, nullable=True)
    latitude = Column(Text, nullable=True)
    longitude = Column(Text, nullable=True)
    parent_incident_type = Column(Text, nullable=True)
    state = Column(Text, nullable=True)
    updated_at = Column(Text, nullable=True)
    zip = Column(Text, nullable=True)
