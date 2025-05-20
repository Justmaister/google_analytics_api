# Google Analytics Custom Reports API

This project provides a custom solution for retrieving Google Analytics data using the Google Analytics Reporting API v4. It was developed to reduce dependency on third-party applications and associated costs while maintaining full control over data retrieval and processing.

## Overview

The project consists of several components that work together to fetch, process, and store Google Analytics data:

- Custom report generation for multiple GA account ID
- Data processing and wrangling
- Automated data collection

## Features

- **Multi GA accounts Support**: Fetch data for multiple countries simultaneously
- **Custom Metrics**: Configure and retrieve specific metrics and dimensions
- **Data Processing**: Built-in data cleaning and type conversion
- **Automated Collection**: Schedule and automate data collection
- **Cost-Effective**: Eliminates need for paid third-party solutions

## Configuration

The `config.py` file contains the following configurations:

- `SCOPES`: Google Analytics API scopes
- `DIMENSIONS`: GA dimensions to fetch
- `METRICS`: GA metrics to fetch
- `VIEW_IDS`: Mapping of view IDs to countries

- Place your Google Analytics service account credentials in the `credentials` folder
