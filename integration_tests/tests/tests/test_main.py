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
    response = requests.post('http://federation:3000/graphql/', json=query)
    assert response.status_code == 200
    data = json.loads(response.content)['data']
    assert data['goodbye'] == 'See ya!'


def test_external_types():
    query = {
        'query': """
            query {
                posts {
                    title
                    text {
                       id
                       body
                       color
                    }
                    files {
                       id
                       name
                    }
                    author {
                        id
                        email
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

    assert 4 == len(posts)
    assert [{'id': 1, 'name': 'file_1'}] == posts[0]['files']
    assert {'id': 1, 'body': 'funny_text_1', 'color': 3} == posts[0]['text']
    assert [{'id': 2, 'name': 'file_2'}, {'id': 3, 'name': 'file_3'}] == posts[1]['files']
    assert {'id': 2, 'body': 'funny_text_2', 'color': 4} == posts[1]['text']
    assert posts[2]['files'] is None
    assert {'id': 3, 'body': 'funny_text_3', 'color': 5} == posts[2]['text']
    assert {'id': 1001, 'email': 'frank@frank.com', } == posts[3]['author']


def fetch_sdl():
    query = {
        'query': """
            query {
                _service {
                    sdl
                }
            }
        """,
        'variables': {}
    }
    response = requests.post('http://service_b:5000/graphql', json=query)
    assert response.status_code == 200
    return response.json()['data']['_service']['sdl']


def test_key_decorator_applied_by_exact_match_only():
    sdl = fetch_sdl()
    assert 'type FileNode  @key(fields: "id")' in sdl
    assert 'type FileNodeAnother  @key(fields: "id")' not in sdl


def test_mutation_is_accessible_in_federation():
    # this mutation is created in service_b
    mutation = """
    mutation {
        funnyMutation {
            result
        }
    }"""

    response = requests.post(
        'http://federation:3000/graphql/', json={'query': mutation}
    )
    assert response.status_code == 200
    assert 'errors' not in response.json()
    assert response.json()['data']['funnyMutation']['result'] == 'Funny'


def test_multiple_key_decorators_apply_multiple_key_annotations():
    sdl = fetch_sdl()
    assert 'type User  @key(fields: "id") @key(fields: "email")' in sdl
