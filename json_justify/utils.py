from json import dumps

class ErrorResponse(object):

    """
    This class will be used to create error response but it will be
    used in later implementation of module
    """
    def __init__(self, response = None):
        self.response = dict()
        if response is not None and isinstance(response, dict):
            self.response = response

    def __contains__(self, key):
        return key in self.response

    def add(self, key, value):
        self.response[key] = value

    def resp(self):
        return dumps(self.response)


class PlaceHolder(object):

    """
    This is placeholder which is used when no data is set
    """

    def __str__(self):
        return "<Placeholder>"

    __repr__ = __str__

    def __nonzero__(self):
        return False

    def __bool__(self):
        return self.__nonzero__()

class Level(object):

    """This class will be used to
    set Level of runtime
    :Example:
    level = Level(Level.DEBUG)

    :param level: int
    """
    DEBUG = 0
    PRODUCTION = 1

    def __init__(self,level):
        """setting level here
        
        Args:
            level (int): Integer to set level
        """
        self.level = level

    @property
    def level(self):
        """
        This is used to set level to work with
        default levels are as follow
        DEGUG
        PRODUCTION

        :return: Int
        """
        return self._value

    @level.setter
    def level(self,value):
        """This is used to set value
        
        Args:
            value (int): Integer
        """
        assert isinstance(value, int), "Please use level value as integer"
        self._value = value

    @level.deleter
    def level(self):
        raise Exception("cannot delete level")
