# pylint: disable=attribute-defined-outside-init, missing-docstring
"""Contains descriptor Classes which validate their inputs."""

from __future__ import annotations

from typing import Any, Callable

ValidatorFunction = Callable[["ValidatedDescriptor", Any], None]


class ValidatedDescriptor:
    """Class used as an alternative to setter methods that validate inputs.
    The constructor takes a list of functions used to validate the input value.
    A validation function should raise an exception
    if the input value is not valid and do nothing if it is.
    """

    def __init__(self, validation_funcs: list[ValidatorFunction]):

        self.validation_funcs = validation_funcs

    def validate(self, value: Any) -> None:
        """This function passes the input value to each of the validation functions."""

        for func in self.validation_funcs:

            func(self, value)

    def __set_name__(self, owner, name: str):

        self.public_name = name

        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):

        try:

            self.validate(value)

            setattr(obj, self.private_name, value)

        except (TypeError, ValueError) as err:

            print(err)

            raise err


def type_check_factory(type_: type) -> ValidatorFunction:
    def type_check(descriptor: ValidatedDescriptor, value: Any) -> None:

        if not isinstance(value, type_):

            raise TypeError(
                f"{descriptor.public_name} must be of type {type_.__name__} not {type(value).__name__}"
            )

    return type_check


def value_check_factory(
    check_func: Callable[[Any], bool], prop: str
) -> ValidatorFunction:
    def value_check(descriptor: ValidatedDescriptor, value: Any) -> None:

        if not check_func(value):

            raise ValueError(f"{descriptor.public_name} must be {prop}")

    return value_check


is_integer = type_check_factory(int)

is_float = type_check_factory(float)

is_string = type_check_factory(str)

is_bool = type_check_factory(bool)

is_positive = value_check_factory(lambda x: x > 0, "positive")

is_non_negative = value_check_factory(lambda x: x >= 0, "non-negative")
