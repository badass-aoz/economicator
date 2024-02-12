from flask import Flask, jsonify
from backend.app.storage import Session, Indicator, DataPoint
from backend.app.config.log_config import setup_logging
from backend.app.crawl_data import start_crawling
from flask_cors import CORS
import argparse


def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # TODO: midpri - support an argument for crawling data only
    start_crawling()

    @app.route('/api/cpi')
    def get_cpi_data():
        return fetch_all_indicator_data('CPI')

    @app.route("/api/unemployment")
    def get_unemployment_data():
        return fetch_all_indicator_data('Unemployment Rate')

    @app.route("/api/gdp")
    def get_gdp_data():
        return fetch_all_indicator_data('GDP')

    def fetch_all_indicator_data(indicator_name: str):
        session = Session()
        data = session.query(DataPoint).join(
            Indicator).filter(Indicator.name == indicator_name).all()
        session.close()
        # Format data for the frontend
        data = [{'date': dp.date.strftime(
            '%Y-%m-%d'), 'value': dp.value} for dp in data]
        response = jsonify(data)
        response.headers.add('Access-Control-Allow-Origin',
                             '*')
        return response

    @app.route("/hello")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/")
    def index():
        return "<h1>Welcome to ecomnomicator!!</h1>"

    return app


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='Economicator',
        description='The backend that crawls data and set up an API server')
    parser.add_argument('-v', '--verbose',
                        action='store_true')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    if args.verbose:
        setup_logging("DEBUG")
    else:
        setup_logging()

    app = create_app()
    app.run()
else:
    app = create_app()
