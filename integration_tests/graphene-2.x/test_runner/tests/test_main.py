import json
import pytest
import requests

SERVICE_A = "service_a"
SERVICE_B = "service_b"
SERVICE_C = "service_c"
SERVICE_D = "service_d"


@pytest.fixture
def federation_gateway_url():
    url = f"http://federation:3002/graphql/"
    return url


def fetch_sdl(service_name: str):
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
    response = requests.post(f'http://{service_name}:5002/graphql/', json=query)
    assert response.status_code == 200
    return response.json()['data']['_service']['sdl']


def test_integrate_simple_schema(federation_gateway_url):
    query = {
        'query': """
            query {
                goodbye
            }
        """,
        'variables': {}
    }
    response = requests.post(federation_gateway_url, json=query)
    assert response.status_code == 200
    data = json.loads(response.content)['data']
    assert data['goodbye'] == 'See ya!'
    print("qwerty")


def test_external_types(federation_gateway_url):
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
                        primaryEmail
                    }
                }
                articles {
                    id
                    text
                    author {
                        id
                        primaryEmail
                    }
                }
            }
        """,
        'variables': {}
    }
    response = requests.post(
        federation_gateway_url,
        json=query,
    )
    assert response.status_code == 200
    data = json.loads(response.content)['data']
    posts = data['posts']
    articles = data['articles']

    assert 4 == len(posts)
    assert [{'id': 1, 'name': 'file_1'}] == posts[0]['files']
    assert {'id': 1, 'body': 'funny_text_1', 'color': 3} == posts[0]['text']
    assert [{'id': 2, 'name': 'file_2'}, {'id': 3, 'name': 'file_3'}] == posts[1]['files']
    assert {'id': 2, 'body': 'funny_text_2', 'color': 4} == posts[1]['text']
    assert posts[2]['files'] is None
    assert {'id': 3, 'body': 'funny_text_3', 'color': 5} == posts[2]['text']
    assert {'id': 1001, 'primaryEmail': 'frank@frank.com', } == posts[3]['author']

    assert articles == [
        {'id': 1, 'text': 'some text', 'author': {'id': 5, 'primaryEmail': 'name_5@gmail.com'}}]



def test_key_decorator_applied_by_exact_match_only():
    sdl = fetch_sdl(SERVICE_B)
    assert 'type FileNode @key(fields: "id")' in sdl
    assert 'type FileNodeAnother @key(fields: "id")' not in sdl


def test_avoid_duplication_of_key_decorator():
    sdl = fetch_sdl(SERVICE_A)
    assert 'extend type FileNode  @key(fields: \"id\") {' in sdl


def test_multiple_key_decorators_apply_multiple_key_annotations():
    sdl = fetch_sdl(SERVICE_B)
    assert 'type User @key(fields: "primaryEmail") @key(fields: "id")' in sdl


def test_mutation_is_accessible_in_federation(federation_gateway_url):
    # this mutation is created in service_b
    mutation = """
    mutation {
        funnyMutation {
            result
        }
    }"""

    response = requests.post(
        federation_gateway_url, json={'query': mutation}
    )
    assert response.status_code == 200
    assert 'errors' not in response.json()
    assert response.json()['data']['funnyMutation']['result'] == 'Funny'


def test_provides(federation_gateway_url):
    """
    articles -> w/o provide (get age value from service b)
    articlesWithAuthorAgeProvide -> w/ provide (get age value from service c)

    :return:
    """
    query = {
        'query': """
                query {
                    articles {
                        id
                        text
                        author {
                            age
                        }
                    }
                    articlesWithAuthorAgeProvide {
                        id
                        text
                        author {
                            age
                        }
                    }
                }
            """,
        'variables': {}
    }
    response = requests.post(
        federation_gateway_url,
        json=query,
    )
    assert response.status_code == 200
    data = json.loads(response.content)['data']
    articles = data['articles']
    articles_with_age_provide = data['articlesWithAuthorAgeProvide']

    assert articles == [
        {'id': 1, 'text': 'some text', 'author': {'age': 17}}]

    assert articles_with_age_provide == [
        {'id': 1, 'text': 'some text', 'author': {'age': 18}}]


def test_requires(federation_gateway_url):
    query = {
        'query': """
            query {
                articles {
                    id
                    text
                    author {
                        uppercaseEmail
                    }
                }
            }
        """,
        'variables': {}
    }
    response = requests.post(
        federation_gateway_url,
        json=query,
    )
    assert response.status_code == 200
    data = json.loads(response.content)['data']
    articles = data['articles']

    assert articles == [
        {'id': 1, 'text': 'some text', 'author': {'uppercaseEmail': 'NAME_5@GMAIL.COM'}}]