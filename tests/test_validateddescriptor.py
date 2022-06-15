# pylint: disable=redefined-outer-name, missing-docstring

from typing import TypeVar
import pytest

from validateddescriptor import ValidatedDescriptor, value_check_factory

is_not_empty = value_check_factory(lambda x: x != "", "non-empty")


@pytest.fixture
def non_empty_str_desc():

    return ValidatedDescriptor.factory(str, [is_not_empty])


class TestClass:

    name = ValidatedDescriptor.factory(str, [is_not_empty])

    age = ValidatedDescriptor.factory(float)

    def __init__(self, name: str, age: float):

        self.name = name

        self.age = age


@pytest.fixture
def test_instance():

    return TestClass("John", 30.0)


def test_init():

    str_desc = ValidatedDescriptor.factory(str)

    assert str_desc.validation_funcs == []

    assert str_desc.type_ == str


def test_init_invalid():

    with pytest.raises(TypeError):

        ValidatedDescriptor.factory(TypeVar("a"))


def test_init_with_validation_funcs(non_empty_str_desc):

    assert non_empty_str_desc.validation_funcs

    non_empty_str_desc = "John"


def test_init_of_test_class(test_instance):

    assert test_instance.name == "John"
    assert test_instance.age == 30.0


def test_init_of_test_class_invalid():

    with pytest.raises(TypeError):

        TestClass("John", "30.0")  # type: ignore


def test_set_attr(test_instance):

    test_instance.age = 15.0

    assert test_instance.age == 15.0


def test_set_attr_invalid_type(test_instance):

    with pytest.raises(TypeError):

        test_instance.age = "30.0"


def test_set_attr_invalid_value(test_instance):

    with pytest.raises(ValueError):

        test_instance.name = ""
