import requests
import logging
from datetime import datetime

from backend.app.storage.data_storage import get_latest_date_for_indicator
from backend.app.fetchers.base_fetcher import BaseFetcher

logger = logging.getLogger(__name__)


class BLSFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.api_key = 'TODO: <enter yours>'
        self.series_id = None
        self.api_url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'

    def _fetch_data_for_indicator(self, indicator: str, start_year=None):
        # Prepare the request payload
        end_year = datetime.now().year
        if start_year is None:
            latest_year_date = get_latest_date_for_indicator(indicator)
            # use 1900 as BLS can safely handle early years
            start_year = 1900 if latest_year_date is None else latest_year_date.year
        data = {
            "seriesid": [self.series_id],
            "startyear": str(start_year),
            "endyear": str(end_year),
            "registrationkey": self.api_key,
        }

        # Make the API request
        response = requests.post(self.api_url, json=data)

        # Check for a successful response
        if response.status_code == 200:
            raw_data = response.json()
            # There are two cases for special handling:
            # 1. If no data is returned, it can be data for all the years we crawl aren't available
            if len(raw_data['Results']['series'][0]['data']) == 0:
                msg = raw_data['message'][-1]
                if 'No Data Available for Series' in msg:
                    latest_year = int(msg[-4:])
                    return self._fetch_data_for_indicator(indicator, latest_year)
                else:
                    logger.error(
                        f"No data is available for {indicator}: {msg}")
                    return None
            # 2. If we hit the system-allowed limit of 20 years, we need to keep crawling
            for msg in raw_data['message']:
                if 'system-allowed limit' in msg:
                    latest_year = int(
                        raw_data['Results']['series'][0]['data'][0]['year'])
                    more_data = self._fetch_data_for_indicator(
                        indicator, latest_year)
                    raw_data['Results']['series'][0]['data'].extend(
                        more_data['Results']['series'][0]['data'])
                break
            return raw_data
        else:
            response.raise_for_status()

    def process_data(self, data):
        # Assuming data is the raw JSON response from the fetch_data method
        processed_data = []
        if 'Results' in data:
            for item in data['Results']['series'][0]['data']:
                # Convert periodName to a datetime object for simplicity; adjust as necessarymonth_str = item['period'][1:]  # This removes the 'M' but keeps '01', '02', etc.
                # This removes the 'M' but keeps '01', '02', etc.
                month_str = item['period'][1:]
                date_str = f"{item['year']}-{month_str}-01"

                # date_str = f"{item['year']}-{item['period'][2:]}-01"  # Assumes period is in the format 'M01', 'M02', etc.
                data_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                data_value = float(item['value'])
                processed_data.append({'date': data_date, 'value': data_value})
        else:
            logger.warn("No data found in {self.__class__.__name__}.")
        return processed_data
