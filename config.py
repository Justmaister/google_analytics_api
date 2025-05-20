SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

# View IDs and country mapping
VIEW_IDS = {
    'ga:172857801': 'Spain',
    'ga:185615721': 'Germany',
    'ga:172849730': 'Italy',
    'ga:174328120': 'Portugal'
}

# Analytics dimensions and metrics
DIMENSIONS = [
    'ga:date',
    'ga:source',
    'ga:medium'
]

METRICS = [
    'ga:sessions',
    'ga:newusers',
    'ga:pageviews',
    'ga:uniquePageviews',
    'ga:timeOnPage',
    'ga:bouncerate',
    'ga:avgSessionDuration',
    'ga:pageviewsPerSession'
]