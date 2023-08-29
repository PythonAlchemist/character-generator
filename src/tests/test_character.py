import pytest
from char_gen.entity.character import Character


props = {
    "name": "John Doe",
    "description": "Test Chatracter",
    "age": 30,
}


@pytest.fixture
def new_character():
    return Character(props=props)


def test_character(new_character):
    assert new_character.name == props["name"]
    assert new_character.description == props["description"]
    assert new_character.age == props["age"]
    assert new_character.is_dead == False
