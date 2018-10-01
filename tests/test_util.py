import pytest
from json_justify.utils import PlaceHolder, ErrorResponse, Level

dct = {'akash': 'student'}
resp = ErrorResponse()
resp_param = ErrorResponse(response=dct)


def test_response():
    resp.add('name', 'akash')
    assert resp.response == {'name': 'akash'}
    assert resp_param.response == {'akash': 'student'}
    assert 'name' in resp
    assert resp.resp() == '{"name": "akash"}'


def test_placeholder():
    place = PlaceHolder()
    assert str(place) == "<Placeholder>"
    assert bool(place) == False


def test_level():
    level = Level(1)
    assert level.level == 1

    with pytest.raises(Exception) as error:
        del level.level

    assert "cannot delete level" in str(error.value)

    with pytest.raises(AssertionError) as error:
        level.level = 'a'

    assert "Please use level value as integer" in str(error.value)

    level.level = 0

    assert level.level == 0
