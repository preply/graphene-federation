import json
import requests


def test_integrate_simple_schema():
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


def test_external_types():
    query = {
        'query': """
            query {
                posts {
                    title
                    text
                    files {
                       id
                       name
                    }
                }
            }
        """,
        'variables': {}
    }
    response = requests.post(
        'http://federation:3000/graphql/',
        json=query,
    )
    assert response.status_code == 200
    posts = json.loads(response.content)['data']['posts']
    assert 3 == len(posts)
    assert [{"id": 1, "name": "file_1"}] == posts[0]['files']
    assert [{"id": 2, "name": "file_2"}, {"id": 3, "name": "file_3"}] == posts[1]['files']
    assert posts[2]['files'] is None
