"""
Google Analytics API Data Collection Script
This script fetches data from Google Analytics API for multiple view IDs and saves it to CSV files.
"""

from pathlib import Path
import pandas as pd
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from config import (
    SCOPES,
    DIMENSIONS, METRICS, VIEW_IDS
)
import logging

BASE_DIR = Path.cwd()
CREDENTIALS_FILE = BASE_DIR / 'credentials' / 'client_secrets.json'
OUTPUT_DIR = BASE_DIR / 'output'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(OUTPUT_DIR / 'analytics.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GoogleAnalyticsClient:
    def __init__(self):
        """Initialize the Google Analytics client."""
        try:
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
                CREDENTIALS_FILE, SCOPES
            )
            self.analytics = build('analyticsreporting', 'v4', credentials=self.credentials)
            logger.info("Successfully initialized Google Analytics client")
        except Exception as e:
            logger.error(f"Failed to initialize Google Analytics client: {str(e)}")
            raise

    def get_report(self, view_id, start_date, end_date):
        """
        Fetch report data from Google Analytics for a specific view ID.

        Args:
            view_id (str): The Google Analytics view ID
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format

        Returns:
            dict: API response containing report data
        """
        try:
            response = self.analytics.reports().batchGet(
                body={
                    'reportRequests': [{
                        'viewId': view_id,
                        'dateRanges': {
                            'startDate': start_date,
                            'endDate': end_date
                        },
                        'metrics': [{'expression': i} for i in METRICS],
                        'dimensions': [{'name': j} for j in DIMENSIONS],
                        'orderBys': [{"fieldName": "ga:date", "sortOrder": "ASCENDING"}],
                        'pageSize': 100000
                    }]
                }
            ).execute()

            logger.info(f"Successfully fetched report for view ID {view_id} from {start_date} to {end_date}")
            report = response['reports'][0]

            data_csv = []
            header_row = []

            nextpage = report.get('nextPageToken', None)
            columnHeader = report.get('columnHeader', {})
            metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
            dimensionHeaders = columnHeader.get('dimensions', [])

            for dheader in dimensionHeaders:
                header_row.append(dheader)
            for mheader in metricHeaders:
                header_row.append(mheader['name'])

            rows = report.get('data', {}).get('rows', [])
            for row in rows:
                row_temp = []
                dimensions = row.get('dimensions', [])
                metrics = row.get('metrics', [])
                for d in dimensions:
                    row_temp.append(d)
                for m in metrics[0]['values']:
                    row_temp.append(m)
                data_csv.append(row_temp)

            result_df = pd.DataFrame(data_csv, columns=header_row)

            while nextpage is not None:
                response = self.analytics.reports().batchGet(
                body={
                    'reportRequests': [
                    {
                    'viewId': view_id,
                    'dateRanges': {
                        'startDate': start_date,
                        'endDate': end_date
                    },
                    'metrics': [{'expression':i} for i in METRICS],
                    'dimensions': [{'name':j} for j in DIMENSIONS]
                    ,'orderBys': [{"fieldName": "ga:dateHourMinute","sortOrder": "ASCENDING"}]
                    ,'pageSize': 100000
                    ,'pageToken': nextpage
                    }]
                }
            ).execute()
                report = response['reports'][0]

                data_csv = []

                rows = report.get('data', {}).get('rows', [])
                for row in rows:
                    row_temp = []
                    dimensions = row.get('dimensions', [])
                    metrics = row.get('metrics', [])
                    for d in dimensions:
                        row_temp.append(d)
                    for m in metrics[0]['values']:
                        row_temp.append(m)
                    data_csv.append(row_temp)

                result_df2 = pd.DataFrame(data_csv, columns=header_row)
                result_df = result_df.append(result_df2)

                nextpage = report.get('nextPageToken', None)

            return result_df
        except Exception as e:
            logger.error(f"Failed to fetch report for view ID {view_id}: {str(e)}")
            raise

def process_report_data(report):
    """
    Process the report data into a pandas DataFrame.

    Args:
        report (dict): Report data from Google Analytics API

    Returns:
        pd.DataFrame: Processed data
    """
    try:
        # Get headers
        column_header = report.get('columnHeader', {})
        metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])
        dimension_headers = column_header.get('dimensions', [])

        # Combine headers
        headers = dimension_headers + [m['name'] for m in metric_headers]

        # Process rows
        rows = report.get('data', {}).get('rows', [])
        data = []

        for row in rows:
            row_data = row.get('dimensions', [])
            metrics = row.get('metrics', [])
            row_data.extend(metrics[0]['values'])
            data.append(row_data)

        # Create DataFrame
        df = pd.DataFrame(data, columns=headers)

        df['ga:date'] = pd.to_datetime(df['ga:date'])

        # Convert numeric columns
        numeric_columns = [col for col in df.columns if col.startswith('ga:') and col != 'ga:date']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        logger.info(f"Successfully processed {len(df)} rows of data")
        return df
    except Exception as e:
        logger.error(f"Failed to process report data: {str(e)}")
        raise

def save_data(df, country):
    """
    Save the processed data to a CSV file.

    Args:
        df (pd.DataFrame): Processed data
        country (str): Country code for the file name
    """
    try:
        country_dir = OUTPUT_DIR / country
        country_dir.mkdir(exist_ok=True)

        date = df['ga:date'].iloc[0]
        filename = f"{date.strftime('%Y%m%d')}.csv"
        filepath = country_dir / filename

        df.to_csv(filepath, index=False)
        logger.info(f"Successfully saved data to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save data: {str(e)}")
        raise

def process_country_data(client, view_id, country, start_date, end_date):
    """
    Process data for a specific country/view ID.

    Args:
        client (GoogleAnalyticsClient): GA client instance
        view_id (str): Google Analytics view ID
        country (str): Country name
        start_date (str): Start date
        end_date (str): End date
    """
    try:
        logger.info(f"Processing data for {country} (View ID: {view_id})")

        report = client.get_report(view_id, start_date, end_date)

        df = process_report_data(report)

        save_data(df, country)

        logger.info(f"Successfully completed processing for {country}")
    except Exception as e:
        logger.error(f"Failed to process data for {country}: {str(e)}")
        raise

def main():
    """Main function to run the data collection process for all countries."""
    try:
        client = GoogleAnalyticsClient()

        start_date = date.today().isoformat()
        end_date = start_date

        for view_id, country in VIEW_IDS.items():
            try:
                process_country_data(client, view_id, country, start_date, end_date)
            except Exception as e:
                logger.error(f"Failed to process {country}: {str(e)}")
                continue

        logger.info("Data collection process completed for all countries")
    except Exception as e:
        logger.error(f"Data collection process failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()