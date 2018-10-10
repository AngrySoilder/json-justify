
# Testing functionality without app
# With that only functionality will be checked

import pytest
from json_justify import JsonManager
from json_justify.fields import String, Number, Boolean, Array, Keyname, Field
from json_justify.validators import Invalid, Length, Right

class dummyclas:
    pass

class dummy_field(JsonManager):
    name = Field("name")

class string_js(JsonManager):
    name = String(field_name="name")

class string_val_js(JsonManager):
    name = String(field_name="name",validators=[Length(min_val=5)])

class number_js(JsonManager):
    age = Number(field_name="age")

class number_call_js(JsonManager):
    age = Number(field_name="ahge")

class number_val_js(JsonManager):
    age = Number(field_name="age", validators=[Length(min_val=2,max_val=2)])

class boolean_js(JsonManager):
    student = Boolean(field_name="student")

class boolean_val_js(JsonManager):
    student = Boolean(field_name="student",validators=[Right()])

class array_js(JsonManager):
    students = Array(field_name="students")

class array_len_js(JsonManager):
    students = Array(field_name="students", min_len=2, max_len=2)

class array_len_false_js(JsonManager):
    students = Array(field_name="students", min_len=3, max_len=6)

class array_model_js(JsonManager):
    students = Array(field_name="students", js_model= string_js)

class array_seq_validators(JsonManager):
    students = Array(field_name="students", seq_validators=[Length(min_val=5,max_val=5),Length(min_val=5,max_val=5)])

class array_mismatch_js(JsonManager):
    students = Array(field_name="studendts")

class array_with_validators_js(JsonManager):
    students = Array(field_name="students", validators=[Length(min_val=5,max_val=5)])



s = Keyname("akash")
sp = Keyname("akash",'js')

string_data = {
    "name" : "Akash"
}

number_data = {
    "age" : 20
}

number_false_data = {
    "age" : 200
}

number_str_data = {
    "age" : "string"
}

boolean_data = {
    "student" : True
}

boolean_false_data = {
    "student" : "call"
}

array_data = {
    "students" : ['akash','adars']
}

array_false_data = {
    "students" : True
}

array_js_model_data ={
    "students" : [{
        "name" : "Akash"
    }]
}

array_js_false_model_data = {
    "students" : [{
        "name" : True
    }]
}

def test_dummy_field():
    js = dummy_field(data=string_data)
    assert js.is_valid() == True
    assert str(js['name']) == '<Field>'
    with pytest.raises(Invalid) as error:
        del js['name'].data
    assert "Cannot Delete data attribute" in str(error.value)

def test_string_js():
    js = string_js(data=string_data)
    assert js.is_valid() == True
    assert js._mapped_data == {"name" : "Akash"}
    js = string_val_js(data=string_data)
    assert js.is_valid()

def test_number_js():
    js = number_js(data=number_data)
    assert js.is_valid() == True
    assert js._mapped_data == {"age" : 20}
    js = number_val_js(data=number_data)
    assert js.is_valid() == True
    js = number_val_js(data=number_false_data)
    assert js.is_valid() == False
    js = number_js(data=number_str_data)
    assert js.is_valid() == False

def test_boolean_js():
    js = boolean_js(data=boolean_data)
    assert js.is_valid() == True
    assert js._mapped_data == {"student" : True}
    js = boolean_val_js(data=boolean_data)
    assert js.is_valid()
    js = boolean_val_js(data=boolean_false_data)
    assert js.is_valid() == False

def test_array_js():
    js = array_js(data=array_data)
    assert js.is_valid() == True
    assert js._mapped_data == { "students" : ['akash','adars'] }

    js_len = array_len_js(data=array_data)
    assert js_len.is_valid() == True

    js_model_c = array_model_js(data=array_js_model_data)
    assert js_model_c.is_valid() == True

    js_model_fal_c = array_model_js(data = array_js_false_model_data)
    assert js_model_fal_c.is_valid() == False

    with pytest.raises(ValueError) as error:
        class Array_Seq_Js(JsonManager):
            students = Array(field_name="students", validators=[Length(min_val=5)],
                             seq_validators=[Length(min_val=5), Length(min_val=5)])
    assert "you can use only one at a time from validators" in str(error.value)
    js = array_seq_validators(data=array_data)
    assert js.is_valid()

    a = Array("arr")
    with pytest.raises(ValueError) as error:
        a({})
    assert "field object to filed should be instance of JsonManager" in str(error.value)

    with pytest.raises(Invalid) as error:
        class array_dummy_js(dummyclas):
            students = Array(field_name="students", seq_validators=Length(min_val=2))
    assert "param seq_validators: should be a list type" in str(error.value)

    with pytest.raises(Invalid) as error:
        class array_dummy_jsonmanager_js(dummyclas):
            students = Array(field_name="students", js_model=dummyclas)
    assert "Please provide a class that subclasses JsonManager" in str(error.value)
    js = array_mismatch_js(data=array_data)
    assert not js.is_valid()

    js = array_js(data=array_false_data)
    assert not js.is_valid()

    js = array_len_false_js(data=array_data)
    assert not js.is_valid()

    js = array_with_validators_js(data=array_data)
    assert js.is_valid()



def test_s():
    assert str(s) == 'akash'
    assert repr(s) == 'akash'
    assert str(sp) =='jsakash'

    with pytest.raises(TypeError) as error:
        key = Keyname(True)
    assert "key of json should be of string Type" in str(error.value)

def test_validator():
    with pytest.raises(Invalid) as error:
        Field("some",validators="handson")
    assert  "validators: should be None or list type" in str(error.value)
    fi = Field("some")
    fi.register_error("one","message")
    assert fi.error_messages == {"one":"message"}
    js = number_call_js(data=number_data)
    assert js.is_valid() == False
