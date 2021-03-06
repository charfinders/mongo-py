
import pytest

from unidata import tokenize, parse


@pytest.fixture
def line_for_A():
    return '0041;LATIN CAPITAL LETTER A;Lu;0;L;;;;;N;;;;0061;'


@pytest.fixture
def line_with_old_name():
    return '002E;FULL STOP;Po;0;CS;;;;;N;PERIOD;;;;'


@pytest.fixture
def three_lines():
    return ['003B;SEMICOLON;Po;0;ON;;;;;N;;;;;',
            '003C;LESS-THAN SIGN;Sm;0;ON;;;;;Y;;;;;',
            '003D;EQUALS SIGN;Sm;0;ON;;;;;N;;;;;']


def test_tokenize():
    name = 'LESS-THAN SIGN'
    assert ['LESS', 'THAN', 'SIGN'] == tokenize(name)


def test_simple_parse(line_for_A):
    char, name = parse(line_for_A)
    assert char == 'A'
    assert name == 'LATIN CAPITAL LETTER A'


def test_parse_with_old_name(line_with_old_name):
    char, name = parse(line_with_old_name)
    assert char == '.'
    assert name == 'FULL STOP | PERIOD'


def test_parse_with_reduntant_old_name():
    line = ('00BD;VULGAR FRACTION ONE HALF;No;0;ON;<fraction'
            '> 0031 2044 0032;;;1/2;N;FRACTION ONE HALF;;;;')
    char, name = parse(line)
    assert name == 'VULGAR FRACTION ONE HALF'
