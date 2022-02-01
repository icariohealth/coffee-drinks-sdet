# pylint: disable=redefined-outer-name,missing-module-docstring,missing-function-docstring,unused-variable,implicit-str-concat,import-error

import pytest
import uuid
from expects import equal, expect, be_a, raise_error
from service.coffee_information_service import CoffeeInformationService
from domain.model.coffee_information import CoffeeInformation
from domain.model.coffee_drink import CoffeeDrink
from exception.not_found_exception import NotFoundException
from exception.invalid_uuid_exception import InvalidUUIDException


def describe_get_all_information():
    def test_should_return_coffee_information(
        coffee_information_repository_mock, coffee_information
    ):
        coffee_information_repository_mock.get_coffee_information.return_value = (
            coffee_information
        )
        coffee_information_service = CoffeeInformationService(
            coffee_information_repository_mock
        )

        result = coffee_information_service.get_all_information()

        expect(result).to(be_a(type(coffee_information)))
        expect(result).to(equal(coffee_information))


def describe_get_drink_by_id():
    def test_should_return_coffee_drink(
        coffee_information_repository_mock, coffee_information, coffee_drink
    ):
        coffee_information_repository_mock.get_coffee_information.return_value = (
            coffee_information
        )
        coffee_information_service = CoffeeInformationService(
            coffee_information_repository_mock
        )

        result = coffee_information_service.get_drink_by_id(
            "209f4328-001c-48ff-925a-bc4319443340"
        )

        expect(result).to(be_a(type(coffee_drink)))
        expect(result).to(equal(coffee_drink))

    @pytest.mark.parametrize(
        "invalid_coffee_drink_uuid",
        [
            uuid.uuid1(),
            uuid.uuid3(uuid.NAMESPACE_X500, "foo"),
            uuid.uuid5(uuid.NAMESPACE_X500, "bar"),
        ],
    )
    def test_should_return_invalid_uuid_exception(
        coffee_information_repository_mock,
        coffee_information,
        invalid_coffee_drink_uuid,
    ):
        coffee_information_repository_mock.get_coffee_information.return_value = (
            coffee_information
        )
        coffee_information_service = CoffeeInformationService(
            coffee_information_repository_mock
        )

        expect(
            lambda: coffee_information_service.get_drink_by_id(
                invalid_coffee_drink_uuid
            )
        ).to(raise_error(InvalidUUIDException))

    def test_should_return_not_found_exception(
        coffee_information_repository_mock, coffee_information
    ):
        coffee_information_repository_mock.get_coffee_information.return_value = (
            coffee_information
        )
        coffee_information_service = CoffeeInformationService(
            coffee_information_repository_mock
        )

        non_existent_uuid = uuid.uuid4()
        expect(lambda: coffee_information_service.get_drink_by_id(non_existent_uuid)).to(
            raise_error(NotFoundException)
        )


def describe_get_drink_by_title():
    def test_should_return_coffee_drink(
        coffee_information_repository_mock, coffee_information, coffee_drink
    ):

        coffee_information_repository_mock.get_coffee_information.return_value = (
            coffee_information
        )

        coffee_information_service = CoffeeInformationService(
            coffee_information_repository_mock
        )

        # This test will fail if String argument contains uppercase
        result = coffee_information_service.get_drink_by_title("black")

        expect(result).to(be_a(type(coffee_drink)))

        expect(result).to(equal(coffee_drink))

    def test_should_return_not_found_exception(
        coffee_information_repository_mock, coffee_information
    ):

        coffee_information_repository_mock.get_coffee_information.return_value = (
            coffee_information
        )

        coffee_information_service = CoffeeInformationService(
            coffee_information_repository_mock
        )

        expect(lambda: coffee_information_service.get_drink_by_title("Gatorade")).to(
            raise_error(NotFoundException)
        )


@pytest.fixture
def coffee_information_repository_mock(mocker):
    return mocker.Mock()


@pytest.fixture
def coffee_information():
    return CoffeeInformation(
        [
            CoffeeDrink(
                id="209f4328-001c-48ff-925a-bc4319443340",
                title="Black",
                description="Coffee served as a beverage without cream or milk.",
                ingredients=["Coffee"],
            ),
            CoffeeDrink(
                id="17575fe7-034c-4f5a-97c9-9ee8fc762c9a",
                title="Latte",
                description="A coffee drink of Italian origin made with espresso and steamed milk.",
                ingredients=["Espresso", "Steamed Milk", "Foamed Milk"],
            ),
            CoffeeDrink(
                id="01d8ddd3-f437-4313-991d-7d8bea95aee1",
                title="Cappuccino",
                description=(
                    "An espresso-based coffee drink that originated in Austria with later "
                    "development taking place in Italy, and is prepared with steamed milk foam."
                ),
                ingredients=["Espresso", "Steamed Milk"],
            ),
        ]
    )


@pytest.fixture
def coffee_drink():
    return CoffeeDrink(
        id="209f4328-001c-48ff-925a-bc4319443340",
        title="Black",
        description="Coffee served as a beverage without cream or milk.",
        ingredients=["Coffee"],
    )
