import json
import requests


def test_federation_can_integrate_simple_schema():
    query = {
        'query': """
            query {
                goodbye
            }
        """,
        'variables': {}
    }
    response = requests.post(
        'http://federation:3000/graphql/',
        json=query,
    )
    assert response.status_code == 200
    data = json.loads(response.content)['data']
    assert data['goodbye'] == "See ya!"
