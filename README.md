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

## Google Analytics Reporting API V4 Setup

### 1 - Crear un Proyecto en la Consola de Google Cloud. 
- Logearse en la [Google Cloud Console](https://console.cloud.google.com/home/dashboard?project=nth-cumulus-283513&folder=&organizationId=). 
- Crear el Proyecto 
- Navigate To APIs & Services in the navigation menu & enable the following APIs. 
- Google Analytics Reporting API (for fetching the data from GA)

### 2 - Crear un Service account 

- Open the [Service accounts page](https://console.developers.google.com/iam-admin/serviceaccounts). If prompted, select a project.
- Click add Create Service Account, enter a name and description for the service account. You can use the default service account ID, or choose a different, unique one. When done click Create.
- The Service account permissions (optional) section that follows is not required. Click Continue.
- On the Grant users access to this service account screen, scroll down to the Create key section. Click add Create key.
- In the side panel that appears, select the format for your key: JSON is recommended.
- Click Create. Your new public/private key pair is generated and downloaded to your machine; it serves as the only copy of this key. For information on how to store it securely, see [Managing service account keys](https://cloud.google.com/iam/docs/understanding-service-accounts#managing_service_account_keys).
- Click Close on the Private key saved to your computer dialog, then click Done to return to the table of your service accounts.


### 3- Add service account to the Google Analytics account
The newly created service account will have an email address that looks similar to:
quickstart@PROJECT-ID.iam.gserviceaccount.com

Use this email address to [add a user](https://support.google.com/analytics/answer/1009702) to the Google analytics view you want to access via the API. For this tutorial only [Read & Analyze](https://support.google.com/analytics/answer/9305587?visit_id=638979458311258426-1384302019&rd=1#zippy=%2Cin-this-article) permissions are needed.