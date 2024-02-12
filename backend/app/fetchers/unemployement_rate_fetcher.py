import logging
from datetime import datetime

from backend.app.fetchers.bls_fetcher import BLSFetcher

logger = logging.getLogger(__name__)


class UnemploymentRateFetcher(BLSFetcher):
    def __init__(self):
        super().__init__()
        self.series_id = 'LNS14000000'  # Unemployment Rate series ID

    def fetch_data(self):
        return self._fetch_data_for_indicator('Unemployment Rate')
