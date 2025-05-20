SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

VIEW_IDS = {
    'ga:ga_spain_id': 'Spain',
    'ga:ga_german_id': 'Germany',
    'ga:ga_italy_id': 'Italy',
    'ga:ga_portugal_id': 'Portugal'
}

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