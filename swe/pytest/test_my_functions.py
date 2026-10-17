
from swe.pytest.my_functions import add, divide
import pytest

##### Parameterize Test Cases #####

ADD_CASES = [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
]

@pytest.mark.parametrize("a, b, expected", ADD_CASES)
def test_add1(a, b, expected):
    assert a + b == expected

###

CASES = [
    {"a": 1, "b": 2, "expected": 3},
    {"a": 0, "b": 0, "expected": 0},
]

@pytest.mark.parametrize("case", CASES)
def test_add2(case):
    assert case["a"] + case["b"] == case["expected"]




##### Basic Implementation #####



def test_add_numbers(): # Convention of naming test_<func_name>()

    assert add(2,3) == 5 , "2+3 = 5"

    assert add(100,1000) == 1100, "100 + 1000 = 1100"

def test_add_strings():

    result = add("Hello", "World")
    assert result 
    assert result == "HelloWorld"



def test_divide_by_zero():

    with pytest.raises(ValueError): # testing if error is raised
        divide(2,0)

def test_divide_result_type():
    assert type(divide(3,2)) == float
    assert type(divide(3,3)) == float





   
