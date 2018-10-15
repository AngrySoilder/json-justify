"""
This module is made to create validators in the field
"""
import re
import warnings
from datetime import datetime
EmailRegex = r'[^@]+@[^@]+\.[^@]+'
UrlRegex = (
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$')
url_regex = re.compile(UrlRegex, re.IGNORECASE)
email_reg = re.compile(EmailRegex, re.IGNORECASE)

try:
    from email_validator import validate_email,EmailNotValidError
except ImportError as e:
    warnings.warn("Email Validator is not found"
        "Please install it using"
        "pip3 install email_validator")
    def validate_email(email):
        if not email_reg.match(email):
            raise Invalid("Email is Not Valid")

class Invalid(ValueError):
    """
    This Exception is General Exception used to raise when Data is invalid,
    Not a valid Type etc.

    :param message: Message you want to print in error
    :param args: any
    :param kwargs: any
    :type message: str
    """
    def __init__(self, message, *args, **kwargs):
        super(Invalid, self).__init__(message, *args, **kwargs)


class Validator(object):
    """
    This is core of each validator class

    :param message: Message to be raised when any invalidation occours
    :type message: str
    """

    def __init__(self, message=None):
        """
        This is The basic Validator

        :param message: The message you want to get in template engine
        """
        if message is not None:
            self.message = message

class Data(Validator):

    """
    This is Data field to check that weather data
    is provided or not

    :param message: Message to be raised when any invalidation occours
    :type message: str
    """

    def __call__(self, obj, field):
        """This is called with object and field
        of object

        Args:
            obj (dir): directory of enclosing field
            field : element of object

        Raises:
            Invalid: if data is not provided
        """
        data = field.data
        if isinstance(data, str) or isinstance(data, int) or isinstance(data, float):
            self.data = str(field.data)
            if not self.data.strip():
                raise Invalid("data is not valid")
        if isinstance(data, list) or isinstance(data, dict):
            self.data = field.data
            if not self.data:
                Invalid("data is not valid")
        

class Length(Validator):
    """
    This validator is used to check the minimum and maximum Length of data
    This will work with str, int , float not with array length

    :param min_val: minimum length
    :param max_val: maximum length
    :param message: Message to be raised when any invalidation occours
    :type message: str
    :type min_val: int
    :type max_val: int
    """
    def __init__(self, min_val=-1, max_val=-1, message=None):
        """Overriding Validator Base class
        """
        super(Length,self).__init__(message)
        if min_val == -1 and max_val == -1:
            raise ValueError('At least Provide one of minimum or minimum Value')
        else:
            self.min_val = min_val
            self.max_val = max_val

    def __call__(self, obj, field):
        self.data = field.data
        if (isinstance(self.data, (str, int, float))):
            self.data = str(self.data).strip()
        else:
            raise Invalid("Not a Valid Type")
        if (len(self.data) < self.min_val or 
                self.max_val!=-1 and len(self.data) > self.max_val):
            raise Invalid("Length is not appopriate")


class Email(Validator):

    """
    The Email Validator is used to validate Email which use dependency of python
    email_validator to validate email if not installed on machiene it will used
    standard regex to validate email

    :param message: Message to be raised when any invalidation occours
    :type message: str
    """

    def __call__(self, obj, field):
        """Call when used to validate this field

        Args:
            obj (dir): An object containing Validator
            field (dir): field of object
        """
        self.data = field.data
        try:
            validate_email(self.data)
        except EmailNotValidError:
            raise Invalid(str(self.data) + "is not valid")


class URL(Validator):
    """
    The url validator is used to validate url's But it dones not instanciate
    from Regex class here this is another implementation

    :param message: Message to be raised when any invalidation occours
    :type message: str
    """

    def __call__(self, obj, field):
        """A Class to validate urls

        Args:
            obj (object): A dir congaing Validator
            field (obj): field of object
        """
        self.data = field.data
        if not url_regex.match(self.data):
            raise Invalid("Not a valid url")


class EqualTo(Validator):
    """
    The EqualTo Validator is used to check if data in our field is
    same as other field

    :param field: Other field Pass the whole Field
    :param message: Message to be raised when any invalidation occours
    :type message: str
    :type field: Field class
    """

    def __init__(self, field, message=None):
        super(EqualTo,self).__init__(message)
        self.other = field

    def __call__(self, obj, field):
        if hasattr(self.other, "_data"):
            other_data = self.other.data
        else:
            self.other(obj)
            other_data = self.other.data
        self.data = field.data
        if self.data != other_data:
            raise Invalid("Unequal Data")


class Date(Validator):
    """
    The date field validator is used to validate date field
    under specific range of min_date and max_date

    :param min_date: minimum date
    :param max_date: maximum date
    :param field_format: format of field
    :param message: message
    :type min_date: str of year-month-date
    :type max_date: str of year-month-date
    :type field_format: Field format %Y-%M-%d is default
    :type message: str
    """

    def __init__(self, min_date= datetime.min, max_date= datetime.min,field_format=None, message=None ):
        """
        Overiding Init
        """
        if field_format is None:
            self.field_format = "%Y-%M-%d"
        else:
            self.field_format = field_format
        super(Date, self).__init__(message)
        if min_date == datetime.min and max_date == datetime.min:
            raise ValueError("Provide one of min_date or max_dat")
        else:
            self.min_date = self.givedatetime(self.field_format, min_date)
            self.max_date = self.givedatetime(self.field_format, max_date)

    def __call__(self, obj, field):
        """
        call the validator just with object containing
        field and the field object

        :param obj: object containing field
        :param field: some field object which instantiate Field
                        which is callable and raises Invalid error
                        when validated
        :return:None
        """
        self.data = field.data
        try:
            self.date = datetime.strptime(self.data, self.field_format)
        except ValueError as e:
            raise Invalid(e)

        if (self.date < self.min_date or
                self.max_date != datetime.min and self.date >= self.max_date):
            raise Invalid("date is not bounded")

    @staticmethod
    def givedatetime(dateformat, date):
        if isinstance(date, datetime):
            return date
        try:
            dt = datetime.strptime(date, dateformat)
            return dt
        except ValueError as e:
            raise Invalid("cannot Get currect format of date"
                "in setting value of datetime at")


class Regex(Validator):
    """
    This is used to validate data in format of regex

    :param regex: regex
    :param message: Message to be raised when Error occours
    :type message: str
    :type regex: str
    """

    def __init__(self, reg, message=None):
        """
        This is regex class used to validate some field
        on regex implementation
        it will not raise invalidation when regex matches
        fields data
        
        Args:
            reg (regex): Regex
            message (message, optional): Message you want on Error
        """
        super(Regex,self).__init__(message)
        self.regex = re.compile(reg)

    def __call__(self, obj, field):
        self.data = field.data
        if not self.regex.match(self.data):
            raise Invalid("it does not match The valid Pattern")
            
class Right(Validator):
    """
    This Validator is specific to boolean Field which validates that
    data is True only

    :param message: message to be raise when error occours
    :type message: str
    """
    def __call__(self,obj,field):
        self.data = field.data
        if not isinstance(self.data, bool):
            raise Invalid("this field should contain"
                "only boolean type values")

        if not self.data:
            raise Invalid("field is false")

class Wrong(Validator):
    """
    This Validator is specific to boolean Field which validates that
    data is False only

    :param message: message to be raise when error occours
    :type message: str
    """

    def __call__(self,obj,field):
        self.data = field.data
        if not isinstance(self.data, bool):
            raise Invalid("this field should contain"
                "only boolean type values")

        if self.data:
            raise Invalid("field is false")