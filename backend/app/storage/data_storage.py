# data_storage.py
from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, Date, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
import os
import logging

Base = declarative_base()
logger = logging.getLogger(__name__)


class Indicator(Base):
    __tablename__ = 'indicators'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    # Establish a one-to-many relationship
    data_points = relationship("DataPoint", back_populates="indicator")


class DataPoint(Base):
    __tablename__ = 'data_points'
    indicator_id = Column(Integer, ForeignKey('indicators.id'))
    date = Column(Date)
    value = Column(Float)

    # Link back to the Indicator
    indicator = relationship("Indicator", back_populates="data_points")

    __table_args__ = (
        PrimaryKeyConstraint('indicator_id', 'date'),
    )


if not os.path.exists('./data'):
    os.makedirs('./data')
# Create an engine that stores data in the local directory's
engine = create_engine('sqlite:///./data/economic_data.db')

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a sessionmaker bound to the engine
Session = sessionmaker(bind=engine)


class DataStorage:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def save_data(self, indicator_name, data):
        # Example pseudo-code for saving data to a database
        # Assume `data` is a dictionary with two lists: dates and values
        for date, value in zip(data['date'], data[indicator_name]):
            # Here, you would construct and execute an SQL query to insert or update the data
            # For demonstration, the actual database operations are not implemented
            logger.debug(f"Saving {indicator_name} for {date}: {value}")
            # Placeholder for SQL INSERT or UPDATE command using `self.db_connection`

    # Additional methods for querying or updating data could be added here


def add_indicator(name, description):
    session = Session()
    indicator = Indicator(name=name, description=description)
    session.add(indicator)
    try:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def add_data_point(indicator_name, date, value):
    session = Session()
    indicator = session.query(Indicator).filter_by(name=indicator_name).first()
    if indicator is None:
        logger.error(f"Indicator {indicator_name} not found.")
        return
    data_point = DataPoint(date=date, value=value, indicator=indicator)
    session.add(data_point)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        logger.info(
            f"Data point for {indicator_name} on {date} already exists. Skipping.")
    except Exception as e:
        session.rollback()
        logger.error(
            f"An error occurred while adding data point for {indicator_name} on {date}: {e}")
        raise
    finally:
        session.close()


def get_all_data_for_indicator(indicator_name):
    session = Session()
    indicator = session.query(Indicator).filter_by(name=indicator_name).first()
    if indicator is None:
        logger.error(f"Indicator {indicator_name} not found.")
        return []
    data_points = session.query(DataPoint).filter_by(
        indicator_id=indicator.id).all()
    session.close()
    return data_points


def get_latest_date_for_indicator(indicator_name):
    session = Session()
    indicator = session.query(Indicator).filter_by(name=indicator_name).first()
    if indicator is None:
        logger.error(f"Indicator {indicator_name} not found.")
        return None
    latest_data_point = session.query(DataPoint).filter_by(
        indicator_id=indicator.id).order_by(DataPoint.date.desc()).first()
    session.close()
    return latest_data_point.date if latest_data_point else None
