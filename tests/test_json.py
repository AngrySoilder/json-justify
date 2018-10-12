import pytest
from json_justify.jason import InvalidMachiene, InvalidContainer
from json_justify.jason import JsonManager, keymapper, addupdict, render_factory
from json_justify.fields import String,Number,Boolean,Array
from json_justify.validators import Invalid

data = {
    "name" : "john doe",
    "age" : 120,
    "male" : False,
    "friends" : ["Jelly","Kelly"]
}

json_chain_data = {
    "chain" : {
    "name" : "john doe",
    "age" : 120,
    "male" : False,
    "friends" : ["Jelly","Kelly"]
}
}

missing_data = {
    "name" : "john doe",
    "age" : 120,
    "friends" : ["Jelly","Kelly"]
}

extra_data = {
    "name" : "john doe",
    "age" : 120,
    "male" : False,
    "extra" : "data",
    "friends" : ["Jelly","Kelly"]
}

def non_return():
    return ('ad','add','daf')

def some():
    return ("chaudhari",)

def cal():
    return ("chaudhari",)

class DummyClass(JsonManager):
    name = String("name")
    age = Number("age")
    male = Boolean("male")
    friends = Array("friends")

class Render(JsonManager):
    name = String("name")
    age = Number("age")
    male = Boolean("male")
    friends = Array("friends")
    render_machienes = (some,)


class Render_false(JsonManager):
    name = String("name")
    age = Number("age")
    male = Boolean("male")
    friends = Array("friends")
    render_machienes = (some)

class chain(JsonManager):
    chain = DummyClass

def test_errors():
    with pytest.raises(InvalidContainer):
        raise InvalidContainer("checkup container")
    with pytest.raises(InvalidMachiene):
        raise InvalidMachiene("checkup machiene")

def test_manager():
    js = DummyClass(data=data)
    assert js.is_valid()

    with pytest.raises(TypeError):
        js['name'] = "akash"
    js["name"] = String('akash') # Setting a field
    assert str(js) == "<DummyClass of JsonManager>"
    assert js.integral_types('akash')
    assert not js.integral_types({'dict': 'f'})

    js = DummyClass(data='akash')
    js.setup_json()
    assert js._mapped_data == {}

def test_renders():
    js = Render(data=data)
    assert js.is_valid()
    assert js()
    js.regester_error('invalid_field','chai')
    with pytest.raises(InvalidContainer):
        js.add_render_machiene('adsd')
    assert js._error_data == {'invalid_field':'chai'}
    assert 'auth_token' in js.render_json()
    assert 'some' in js.render_json()
    js.regester_attris(cal)
    assert len(js._attris_funcs) == 1
    assert js._set_data() == None

    with pytest.raises(ValueError):
        js.child = 'da'
    with pytest.raises(InvalidMachiene):
        js.regester_attris("aka")
    with pytest.raises(ValueError):
        js = Render_false(data=data)

def test_chain():
    js = chain(data=json_chain_data)
    assert js.is_valid()

def test_missing():
    js = DummyClass(data=missing_data)
    assert not js.is_valid()

    js = DummyClass(data=extra_data)
    assert not js.is_valid()

def test_keymaper():
    with pytest.raises(ValueError):
        keymapper([non_return])

def test_addupdict():
    with pytest.raises(ValueError):
        addupdict(['dfa'])

def test_render_factory():
    with pytest.raises(ValueError):
        render_factory(some,(some,))

    js = DummyClass(data=data)
    render_factory(js,(some,))
    assert some in js._render_funcs