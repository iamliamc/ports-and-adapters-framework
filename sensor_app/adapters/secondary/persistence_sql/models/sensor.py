from sqlalchemy import Column, Integer, String, Float
from sensor_app.adapters.secondary.persistence_sql.models.base import Base


class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
