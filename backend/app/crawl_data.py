import logging
from backend.app.fetchers import (
    CPIFetcher,
    UnemploymentRateFetcher,
    GDPFetcher,
)
from backend.app.storage import (
    DataStorage, add_data_point, Session, Base, engine, Indicator
)

logger = logging.getLogger(__name__)


def fetch_and_store_cpi_data():
    # Initialize the CPI fetcher
    cpi_fetcher = CPIFetcher()
    # Assume this now directly returns processed data
    processed_data = cpi_fetcher.get_data()

    # Ensure the CPI indicator is added to the database
    session = Session()
    cpi_indicator = session.query(Indicator).filter_by(name="CPI").first()
    if not cpi_indicator:
        cpi_indicator = Indicator(
            name="CPI", description="Consumer Price Index")
        session.add(cpi_indicator)
        session.commit()
    session.close()

    # Iterate over processed data and store each data point
    for item in processed_data:
        add_data_point("CPI", item['date'], item['value'])

    logger.info("CPI data fetched and stored successfully.")


def fetch_and_store_unemployment_data():
    # Initialize the Unemployment Rate fetcher
    unemployment_fetcher = UnemploymentRateFetcher()
    # Assume this now directly returns processed data
    processed_data = unemployment_fetcher.get_data()

    # Ensure the Unemployment Rate indicator is added to the database
    session = Session()
    unemployment_indicator = session.query(Indicator).filter_by(
        name="Unemployment Rate").first()
    if not unemployment_indicator:
        unemployment_indicator = Indicator(
            name="Unemployment Rate", description="Unemployment Rate")
        session.add(unemployment_indicator)
        session.commit()
    session.close()

    # Iterate over processed data and store each data point
    for item in processed_data:
        add_data_point("Unemployment Rate", item['date'], item['value'])

    logger.info("Unemployment Rate data fetched and stored successfully.")


def fetch_and_store_gdp_data():
    # Initialize the Unemployment Rate fetcher
    gdp_fetcher = GDPFetcher()
    processed_data = gdp_fetcher.get_data()

    # Ensure the Unemployment Rate indicator is added to the database
    session = Session()
    gdp_indicator = session.query(Indicator).filter_by(
        name="GDP").first()
    if not gdp_indicator:
        gdp_indicator = Indicator(
            name="GDP", description="GDP")
        session.add(gdp_indicator)
        session.commit()
    session.close()

    # Iterate over processed data and store each data point
    for item in processed_data:
        logger.info(item)
        add_data_point("GDP", item['date'], item['value'])

    logger.info("GDP data fetched and stored successfully.")


def start_crawling():
    # Initialize the database (if not already initialized)
    Base.metadata.create_all(engine)
    # TODO: lowpri - run those in parallel
    fetch_and_store_cpi_data()
    fetch_and_store_unemployment_data()
    fetch_and_store_gdp_data()


if __name__ == "__main__":
    start_crawling()
