import pytest
from main import factorial

def test_factorial_positive():
    assert factorial(5) == 120

def test_factorial_zero():
    assert factorial(0) == 1

def test_factorial_one():
    assert factorial(1) == 1

def test_factorial_negative():
    with pytest.raises(ValueError):
        factorial(-5)

