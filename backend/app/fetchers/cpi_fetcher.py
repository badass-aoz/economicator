import logging
from datetime import datetime

from backend.app.fetchers.bls_fetcher import BLSFetcher

logger = logging.getLogger(__name__)


class CPIFetcher(BLSFetcher):
    def __init__(self, series_id='CUUR0000SA0'):
        super().__init__()
        self.series_id = series_id  # CPI-U series ID

    def fetch_data(self):
        return self._fetch_data_for_indicator('CPI')
