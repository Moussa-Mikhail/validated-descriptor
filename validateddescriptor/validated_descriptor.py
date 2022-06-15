# pylint: disable=attribute-defined-outside-init, missing-docstring
"""Contains descriptor Classes which validate their inputs."""

from __future__ import annotations

from types import UnionType

from typing import Any, Callable, Generic, TypeVar

# acceptable types
IsInstanceable = type | UnionType | tuple[type | UnionType | tuple[Any, ...], ...]

T = TypeVar("T")

ValidatorFunction = Callable[["ValidatedDescriptor[T]", Any], None]


class ValidatedDescriptor(Generic[T]):
    """Class used as an alternative to setter methods that validate inputs to attributes.
    The constructor takes a list of functions used to validate the input value
    and a type for the attribute.
    A validation function should raise an exception
    if the input value is not valid and do nothing if it is.
    """

    def __init__(
        self,
        type_: IsInstanceable,
        validation_funcs: list[ValidatorFunction] | None = None,
    ):

        self.validation_funcs = validation_funcs or []

        try:

            isinstance(None, type_)

        except TypeError as err:

            raise TypeError(
                f"{type_} must be a type, a tuple of types, or a union"
            ) from err

        self.type_ = type_

        self.type_name = str(type_)

    def validate(self, value: Any) -> None:
        """This function passes the input value to the type check
        and then each of the validation functions.
        """

        self.type_check(value)

        for func in self.validation_funcs:

            func(self, value)

    def type_check(self, value: Any) -> None:

        if not isinstance(value, self.type_):

            raise TypeError(
                f"{self.public_name} must be of type {self.type_name} not {type(value).__name__}"
            )

    def __set_name__(self, owner, name: str):

        self.public_name = name

        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None) -> T:
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):

        try:

            self.validate(value)

            setattr(obj, self.private_name, value)

        except (TypeError, ValueError) as err:

            print(err)

            raise err

    @classmethod
    def factory(cls, type_, validation_funcs: list[ValidatorFunction] | None = None):
        """Factory function for creating ValidatedDescriptors.
        The type of the returned descriptor can be inferred by mypy.
        """

        return ValidatedDescriptor[type_](type_, validation_funcs)  # type: ignore[valid-type]


def value_check_factory(
    check_func: Callable[[Any], bool], prop: str
) -> ValidatorFunction:
    def value_check(descriptor: ValidatedDescriptor, value: Any) -> None:

        if not check_func(value):

            raise ValueError(f"{descriptor.public_name} must be {prop}")

    return value_check
