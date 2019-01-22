import pytest
from enum import Enum

class Season(Enum):
    SPRING = 1
    SUMMER = 9
    FALL   = 3
    WINTER = 5
    AUTUMN = 3 # alias

def test_str_name_repr():
    assert str(Season.SPRING) == 'Season.SPRING' # w/ type
    assert Season.SPRING.name == 'SPRING'        # w/o type

    assert repr(Season.SPRING) == '<Season.SPRING: 1>' # w/ value

def test_type__is_enum_class():
    assert type(Season.SPRING) == Season

    assert isinstance(Season.SPRING, Season)
    assert isinstance(Season.SPRING, Enum)

def test_iteration__in_definition_or_order_exclusing_aliases(py2):
    names = [season.name for season in Season]

    if py2: # in value order
        assert names == ['SPRING', 'FALL', 'WINTER', 'SUMMER']
    else:   # in definition order
        assert names == ['SPRING', 'SUMMER', 'FALL', 'WINTER']

def test_hashable():
    try:
        hash(Season.SPRING)
    except TypeError:
        pytest.fail()

    favorites = {Season.SPRING: 'wind', Season.FALL: 'temp.'}
    assert favorites[Season.SPRING] == 'wind'

def test_member_from_value__or_raise_valueerror():
    assert Season(1) == Season.SPRING

    with pytest.raises(ValueError) as excinfo:
        Season(99)
    assert str(excinfo.value) == '99 is not a valid Season'

def test_member_from_name__or_raise_keyerror():
    assert Season['AUTUMN'] == Season.FALL

    with pytest.raises(KeyError) as excinfo:
        Season['UNKNOWN']
    assert str(excinfo.value) == "'UNKNOWN'"

def test_alias__same_identity_value_and_name():
    assert id(Season.FALL) == id(Season.AUTUMN)
    assert Season.FALL == Season.AUTUMN

    assert Season.FALL.value == Season.AUTUMN.value == 3
    assert Season.FALL.name == Season.AUTUMN.name == 'FALL'

def test_custom_value_attrs():
    class Color(Enum):
        RED    = ('RD', (255, 0, 0))
        GREEN  = ('GN', (0, 255, 0))
        BLUE   = ('BL', (0, 0, 255))

        def __new__(cls, code, rgb):
            obj = object.__new__(cls)
            obj._value_ = code

            return obj

        def __init__(self, code, rgb):
            self.code = code
            self.rgb = rgb

    blue = Color('BL')
    assert blue == Color['BLUE'] == Color.BLUE

    assert blue.value == 'BL'
    assert blue.rgb == (0, 0, 255)