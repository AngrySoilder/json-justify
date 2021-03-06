"""
fields is used to import various fields for json
example
"""

from json_justify.utils import PlaceHolder
from inspect import isclass
from json_justify.validators import Invalid
import json_justify.jason


class Field(object):
    """
    This Field Class is Core of all the Fields and should be instanciated
    For Creating New Fields
    This should only be used with JsonManager Field
    Following Things should be done in order to Create Field
    -- Instanciate Field
    -- Should implement _validate() function to which data of field will be provided
    Also one can change whole functionality by instanciating Field object as well

    :param field_name: Name of the field same as JsonManager Class Field
    :param validators: list of validators
    :type field_name: str
    :type validators: list of callable take one param data
    """

    def __init__(self, field_name, validators=None):

        self.field_name = Keyname(field_name)
        self.error_messages = dict()
        if validators is not None and not isinstance(validators, list):
            raise Invalid("validators: should be None or list type")
        self.validators = validators

    def __str__(self):
        """This is added to give a string Representation
        of Field in different places
        """
        return '<{0}>'.format(self.__class__.__name__)

    __repr__ = __str__

    @property
    def data(self):
        """
        :returns: data associated with particular field
        :raises: Invalid Exception on delete of these property
        """
        return self._data

    @data.setter
    def data(self, value):
        self._data = value if value is not None else PlaceHolder()

    @data.deleter
    def data(self):
        raise Invalid("Cannot Delete data attribute")

    def register_error(self, key,value):
        """This Function is used to register error
        of the fields which is usually done by the
        validaors to register errors
        
        :param key: key of error for json
        :param value: custom error message inside json

        :returns: None but registors error
        """
        self.error_messages[key] = value

    def __call__(self, field_object):
        """
        This is called to validate
        :param field_object:
        :return:
        """
        self.field_object = field_object
        if str(self.field_name) in self.field_object:
            self.data = self.field_object._mapped_data[str(self.field_name)]
            self._validate()
        else:
            raise Invalid(str(self.field_name) + "is not present in object" + self.__class__.__name__)

    def _validate(self, *args, **kwargs):
        """
        This function is used to validate field
        it should be overided by the instanciated class
        :return:
        """
        pass


class String(Field):
    """This is simple String Field of json Which should be used with json manager class 
    
    This field is automacally called inside JsonManager Class and validated if Invalid
    data is raised it will automatically catched by JsonManager Class

    :param field_name: Name of the field same as JsonManager Class Field
    :param validators: list of validators
    :type field_name: str
    :type validators: list of callable take one param data
    """

    def _validate(self):
        """
        The validator is used to
        :return:
        """
        if isinstance(self.data, str):
            if self.validators is not None:
                for check in self.validators:
                    check(self.field_object, self)
            else:
                return True
        else:
            raise Invalid("These are Invalid Field")


class Number(Field):
    """This is Number Field and Should be Used inside JsonManager Class to create numbers
    
    This field will raise Invalid and automatically catched by JsonManager if Data to 
    key is not int of float
    
    :param field_name: Name of the field same as JsonManager Class Field
    :param validators: list of validators
    :type field_name: str
    :type validators: list of callable take one param data
    """
    def _validate(self):
        """
        This is used to validate the data 
        """
        if isinstance(self.data, int) or isinstance(self.data, float):
            if self.validators is not None:
                for check in self.validators:
                    check(self.field_object, self)
            else:
                return True
        else:
            raise Invalid('This booleanfield is Invalid')


class Boolean(Field):
    """This is Boolean Field and Should be Used inside JsonManager Class to create numbers
    
    This field will raise Invalid and automatically catched by JsonManager if Data to 
    key is not Boolean
    
    :param field_name: Name of the field same as JsonManager Class Field
    :param validators: list of validators
    :type field_name: str
    :type validators: list of callable take one param data
    """

    def _validate(self):
        """
        The validate option
        :return:
        """
        if isinstance(self.data, bool):
            if self.validators:
                for check in self.validators:
                    check(self.field_object, self)
            else:
                return True
        else:
            raise Invalid("Data should be boolean type")


class Array(Field):
    """This is simple Array Field and should be used with JsonManager Class to create simple
    Arrays and also objects inside array

    Only one of three paremeters from js_model, validators, seq_validators can be choosed
    at a time
    Two Dimentional or N-Dimentional Array May be Implemented inside later Version of This

    :param field_name: Name of the field same as JsonManager Class Field
    :param validators: list of validators
    :type field_name: str
    :type validators: list of callable take one param data
    :param js_model: a JsonManager Class that should be used to create array of key json
    :param seq_validators: A sequence of validators to validate each sequence of validator
    if choosed length of array is seq_validator
    """
    def __init__(self, field_name, min_len=-1, max_len=-1,
                 js_model=None, validators=None, seq_validators=None):
        """This is addition of functionality of function
        in init function
        
        Args:
            field_name (TYPE): Description
            validators (None, optional): Description
        """
        super(Array, self).__init__(field_name, validators)

        _t_ckeck = [cls for cls in (validators, seq_validators, js_model) if cls is not None]
        _t_ckeck = len(_t_ckeck)
        if _t_ckeck > 1:
            raise ValueError("you can use only one at a time from validators, "
                             "seq_validators and js_model")

        if seq_validators is not None and not isinstance(seq_validators, list):
            raise Invalid("param seq_validators: should be a list type")

        self.seq_validators = seq_validators

        if js_model is not None and isclass(js_model) and not issubclass(js_model, json_justify.jason.JsonManager):
            raise Invalid("Please provide a class that subclasses JsonManager")

        self.js_model = js_model

        if self.seq_validators is not None:
            self.min_len = self.max_len = len(self.seq_validators)
        else:
            self.min_len = min_len
            self.max_len = max_len

    def __call__(self, field_object):
        """A overiding and providing a new implementation for the
        array field
        
        Args:
            field_object (Field): A field controlled array
        """
        if not isinstance(field_object, json_justify.jason.JsonManager):
            raise ValueError("field object to filed should be instance of JsonManager")

        self.field_object = field_object
        if str(self.field_name) in self.field_object:
            dat = self.field_object._mapped_data[str(self.field_name)]
            if not isinstance(dat, list):
                raise Invalid("Array should Be list")
            if (len(dat) < self.min_len or 
                    self.js_model is None and
                    self.max_len != -1 and len(dat) > self.max_len):
                raise Invalid("Invalid Length of Array Found")
            for index, data in enumerate(dat):
                self.data = data
                self._validate(index)
        else:
            raise Invalid("Array is invalid")

    def _validate(self, index):
        
        if self.validators is not None:
            for check in self.validators:
                check(self.field_object, self)

        elif self.seq_validators is not None:
            check = self.seq_validators[index]
            check(self.field_object, self)

        elif self.js_model is not None:
            js = self.js_model
            js = js(data=self.data, _child_hook=True)
            js.is_valid()
        else:
            return True


class Keyname(object):

    """This is keymame of different JsonManager linked Field
    This is used privately inside module
    :param key: keyname
    :param prefix: prefix for keyname
    """
    
    def __init__(self, key, prefix=None):
        if prefix is not None and isinstance(prefix, str) and bool(prefix.strip()):
            self._prefix = prefix.strip()
        else:
            self._prefix = ''

        if isinstance(key, str) and bool(key.strip()):
            self._key = key.strip()
        else:
            raise TypeError("key of json should be of string Type")

    def __str__(self):
        return str(self._prefix + self._key)

    def __repr__(self):
        return str(self._prefix + self._key)