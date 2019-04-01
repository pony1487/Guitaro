import sys
import pytest

sys.path.insert(0, '../')

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_topics_route(client):
    expected_output = b'{"directories":["fingerIndependence","strumming","picking"]}\n'
    rv = client.get('/topics')
    print(rv.data)
    assert expected_output in rv.data


def test_plans_route(client):
    expected_output = b'{"directories":["intermediate","beginner"]}\n'
    rv = client.get('/plans')
    print(rv.data)
    assert expected_output in rv.data


def test_bad_route(client):
    expected_output = b'<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <title>Page not found</title>\n    <div id="main">\n    \t<div class="fof">\n        \t\t<h1>Error 404</h1>\n    \t</div>\n</div>\n</head>\n<body>\n\n</body>\n</html>'

    rv = client.get('/route-that-doesnt-exist')
    print(rv.data)
    assert expected_output in rv.data


def test_get_lesson_notation(client):
    route = "notation/topics/picking/A_minor_pentatonic_ascending-95.wav"
    rv = client.get(route)
    print(rv.data)

    expected_output = b'{"bpm":"95","lesson_fret_list":[5,8,5,7,5,7],"lesson_string_list":["E","E","A","A","D","D"],"padded_duration_list":["half","half","half","half","half","half"],"total_beats":12}\n'

    assert expected_output in rv.data
