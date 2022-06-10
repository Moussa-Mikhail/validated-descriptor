# pylint: disable=attribute-defined-outside-init, missing-docstring
"""Contains descriptor Classes which validate their inputs."""

from __future__ import annotations

from numbers import Real
from typing import Any, Callable, Iterable, Type

ValidatorFunction = Callable[["ValidatedDescriptor", Any], None]


class ValidatedDescriptor:
    """Class used as an alternative to setter methods that validate inputs.
    The constructor takes an iterable of functions used to validate the input value.
    A validation function should raise an exception
    if the input value is not valid and do nothing if it is.
    """

    validation_funcs: set[ValidatorFunction]

    def __init__(self, validation_funcs: Iterable[ValidatorFunction]):

        self.validation_funcs = set(validation_funcs)

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


def type_check_factory(type_: Type):
    def type_check(descriptor: ValidatedDescriptor, value: Any) -> None:

        if not isinstance(value, type_):

            raise TypeError(
                f"{descriptor.public_name} must be a {type_} not {type(value)}"
            )

    return type_check


is_integer = type_check_factory(int)

is_real = type_check_factory(Real)

is_string = type_check_factory(str)

is_bool = type_check_factory(bool)


def is_positive(descriptor: ValidatedDescriptor, value: Any) -> None:

    is_real(descriptor, value)

    if value <= 0:
        raise ValueError(f"{descriptor.public_name} must be positive")


def is_non_negative(descriptor: ValidatedDescriptor, value: Any) -> None:

    is_real(descriptor, value)

    if value < 0:
        raise ValueError(f"{descriptor.public_name} must be non-negative")


def is_non_empty(descriptor: ValidatedDescriptor, value: Any) -> None:
    """Meant to be used along with a container validation function"""

    if not value:
        raise ValueError(f"{descriptor.public_name} must not be empty")
