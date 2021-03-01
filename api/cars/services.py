import json
import requests


NHTSA_API_BASE_URL = 'https://vpic.nhtsa.dot.gov/api/vehicles/'


def get_models_for_make(make):
    """Queries external API and returns set of models names.
    """
    url = f'getmodelsformake/{make.lower()}'
    r = requests.get(NHTSA_API_BASE_URL + url, params={'format': 'json'})
    json_data = json.loads(r.text)
    results = json_data['Results']
    models = set([item['Model_Name'].lower() for item in results])
    return models
