import pytest
from json_justify.jason import JsonManager
from json_justify.validators import (Validator, Data, Length, Email, URL,
                                      Invalid,EqualTo, Date, Regex,Wrong, Right)
from json_justify.fields import String, Boolean, Array
from datetime import datetime

data = {
    "name" : "   "
}

data_false = {
    "name" : " fyes  "
}

data_dct = {
    "name" : []
}

data_for_len = {
    "name" : "akash"
}

data_for_url = {
    "name" : "https://www.google.com"
}

data_for_url_false = {
    "name" : "www.google.com"
}

class Dt(JsonManager):
    name = String("name",validators=[Data()])

class Dt_Len(JsonManager):
    name = String("name",validators=[Length(min_val=5,max_val=5)])

def test_validator():
    val = Validator("Validator message")
    assert val.message == "Validator message"

def test_data():
    js = Dt(data=data)
    assert js.is_valid() == False
    js = Dt(data=data_false)
    assert js.is_valid()

    js = Dt(data=data_dct)
    assert not js.is_valid()

def test_length():
    js = Dt_Len(data=data_for_len)
    assert js.is_valid()

    with pytest.raises(ValueError):
        Length()

def test_url():
    class ur(JsonManager):
        name = String("name", validators=[URL()])

    js = ur(data=data_for_url)
    assert js.is_valid()
    js = ur(data=data_for_url_false)
    assert not js.is_valid()

def test_equal_to():
    equal_data = {
        "name" : "akash",
        "ident" : "akash"
    }
    equal_data_false = {
        "name" : "akash",
        "ident" : "adarsh"
    }
    class eq_js(JsonManager):
        name = String("name")
        ident = String("ident", validators=[EqualTo(name)])

    js = eq_js(data=equal_data)
    assert js.is_valid()
    js = eq_js(data=equal_data_false)
    assert not js.is_valid()

def test_right():
    right_data_false = {
        "Male" : "coller"
    }
    right_data = {
        "Male": True
    }
    right_data_wrong = {
        "Male": False
    }
    class right_js(JsonManager):
        Male =  Boolean("Male", validators=[Right()])

    class wrong_js(JsonManager):
        Male = Boolean("Male", validators=[Wrong()])

    js = right_js(data=right_data)
    assert js.is_valid()
    js = right_js(data=right_data_false)
    assert not js.is_valid()
    js = right_js(data=right_data_wrong)
    assert not js.is_valid()
    js = wrong_js(data=right_data_wrong)
    assert js.is_valid()
    js = wrong_js(data=right_data)
    assert not js.is_valid()

def test_email():
    email_data = {
        "email" : "chaudharia041@gmail.com"
    }
    email_data_false = {
        "email" : "dacofedd.cm"
    }
    class ema(JsonManager):
        email = String("email", validators=[Email()])

    js = ema(data=email_data)
    assert js.is_valid()
    js = ema(data=email_data_false)
    assert not js.is_valid()

def test_regex():
    reg_data = {
        "name" : "akash"
    }
    reg_data_false = {
        "name" : "adarsh"
    }
    class reg(JsonManager):
        name = String("name", validators=[Regex("akash")])

    js = reg(data=reg_data)
    assert js.is_valid()
    js = reg(data=reg_data_false)
    assert not js.is_valid()

def test_date():
    data_date = {
        "date" : "2018-9-30"
    }
    data_date_false = {
        "date" : "30-09-2018"
    }

    data_unbound_date = {
        "date" : "2018-9-27"
    }
    class dt(JsonManager):
        date = String("date", validators=[Date(min_date="2018-9-29")])

    class jsdt(JsonManager):
        date = String("date", validators=[Date(field_format="%Y-%M-%d", min_date='2018-9-29')])

    js = dt(data=data_date)
    assert js.is_valid()

    with pytest.raises(ValueError):
        Date()

    js = dt(data=data_date_false)
    assert not js.is_valid()

    js =dt(data=data_unbound_date)

    assert not js.is_valid()

    with pytest.raises(Invalid):
        Date(field_format = '%Y-%d-%M', min_date='12-12-2012')

def testing_with_array():
    array_dat = {
        "truth" : [True, True]
    }
    array_dat_bool = {
        "truth" : ["akash"]
    }


    class arr_js(JsonManager):
        truth = Array("truth", validators=[Right()])

    class arr_wr(JsonManager):
        truth = Array("truth", validators=[Wrong()])

    js = arr_js(data=array_dat)
    assert js.is_valid()
    js = arr_js(data=array_dat_bool)
    assert not js.is_valid()
    js = arr_wr(data=array_dat_bool)
    assert not js.is_valid()

def test_array_check_second():
    array_data = {
        "students": [{"key" : "value"},{}]
    }

    class array_js(JsonManager):
        students = Array(field_name="students",validators=[Data()])

    class array_js_val(JsonManager):
        students = Array(field_name="students",validators=[Length(min_val=1)])

    js = array_js(data=array_data)
    assert len(js) == 1
    assert js.is_valid()
    js = array_js_val(data=array_data)
    assert not js.is_valid()
