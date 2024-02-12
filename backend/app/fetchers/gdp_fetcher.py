import requests
import logging
from datetime import datetime

from backend.app.storage.data_storage import get_latest_date_for_indicator
from backend.app.fetchers.base_fetcher import BaseFetcher

logger = logging.getLogger(__name__)


# TODO: lowpri - abstract this into a BEA base fetcher
# TODO: current - ensure the GDP fetcher actually works. currently VPN is down so can't pull for data from bls
class GDPFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.api_url = 'https://apps.bea.gov/api/data/'
        self.api_key = '<TODO: enter your bea website>'

    def fetch_data(self):
        # Prepare the request payload
        end_year = datetime.now().year
        latest_year_date = get_latest_date_for_indicator('GDP')
        latest_year = None if latest_year_date is None else latest_year_date.year
        start_year = latest_year if latest_year else end_year - 20
        years = []
        for i in range(start_year, end_year):
            years.append(i)
        years.append(end_year)
        data = {
            "UserID": self.api_key,
            "method": "GetData",
            "datasetname": "NIPA",
            "TableName": "T10101",
            "Frequency": "Q",
            "Year": ','.join([str(year) for year in years]),
            "ResultFormat": "json"
        }

        # Make the API request
        retries = 3
        while retries > 0:
            try:
                response = requests.get(self.api_url, params=data)
            except ConnectionError as e:
                logger.error(
                    f"Failed to fetch GDP data: {e}. Retries left {retries}")
                sleep(5)
                continue
            break
        if retries == 0:
            raise Exception("Failed to fetch GDP data")

        # Check for a successful response
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def process_data(self, data):
        # dump the data into a temporary file for easy debugging
        with open('temp_gdp_data.json', 'w') as f:
            f.write(str(data))
        # Assuming data is the raw JSON response from the fetch_data method
        processed_data = []
        if 'BEAAPI' in data and 'Results' in data['BEAAPI']:
            for item in data['BEAAPI']['Results']['Data']:
                if item['TableName'] != 'T10101' or item['SeriesCode'] != 'A191RL':
                    continue
                time_period = item['TimePeriod']
                year = int(time_period[:4])
                quarter = time_period[4:]

                # Map quarter to the first month of the quarter
                quarter_to_month = {
                    'Q1': 1,
                    'Q2': 4,
                    'Q3': 7,
                    'Q4': 10
                }

                if quarter in quarter_to_month:
                    month = quarter_to_month[quarter]
                    data_date = datetime(year, month, 1).date()
                    data_value = float(item['DataValue'].replace(',', ''))
                    processed_data.append(
                        {'date': data_date, 'value': data_value})
                else:
                    logger.warn(f"Unexpected quarter format: {quarter}")
            print(processed_data)
        else:
            logger.warn("No data found.")
        return processed_data
