from sqlalchemy import Column, BigInteger, FLOAT, INTEGER
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

Base = declarative_base()


class Atmospheric(Base):
    __tablename__ = 'atmospheric'
    __table_args__ = {'schema': 'data'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP(timezone=True))
    temperature = Column(FLOAT)
    humidity = Column(FLOAT)
    pressure = Column(FLOAT)


class Config(Base):
    __tablename__ = 'config'
    __table_args__ = {'schema': 'public'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    value = Column(JSONB)


# region schema
class ConfigSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Config


class AtmosphericSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Atmospheric

# endregion
