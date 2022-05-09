from python.pet import Pet
import pytest


@pytest.fixture
def data():
    """data fixture we can use in other parts of the code"""
    return [
        "ID123",
        "max",
        "gender",
        "dog",
        "1",
        "this is the description",
        "filename.jpg",
        "101",
        "shelter-name"
    ]


def test_init_errors():
    """Test all the errors in the init"""

    with pytest.raises(TypeError):
        # this changes the name into a number, which we want to crash when we make it into a pet
        Pet(
            "ID123",
            123,
            "gender",
            "dog",
            "1",
            "this is the description",
            "filename.jpg",
            "101",
            "shelter-name"
        )

    with pytest.raises(TypeError):
        # this checks the gender is a string
        Pet(
            "ID123",
            "max",
            123,
            "cat",
            "1",
            "this is the description",
            "filename.jpg",
            "101",
            "shelter-name"
        )

    with pytest.raises(ValueError):
        # this checks the species is a string
        Pet(
            "ID123",
            "max",
            "gender",
            "Human",
            "1",
            "this is the description",
            "filename.jpg",
            "101",
            "shelter-name"
        )


def test_init(data):
    """check that the pet data is initialized properly"""

    pet = Pet(*data)
    assert pet.image == "filename.jpg"

    pet_image_none = Pet(
        "ID123", "max", "gender", "dog", "1", "this is the description", "", "101"
    )
    assert pet_image_none.image == "ID123.jpg"


def test_string(data):
    """test the string converter dundar"""
    assert str(Pet(*data)) == """< PET name:max age:1 species:dog gender:gender>"""


def test_to_dict(data):
    pet = Pet(*data)

    assert pet.to_dict() == {
        "id": f"{pet.id}",
        "name": f"{pet.name}",
        "gender": f"{pet.gender}",
        "species": f"{pet.species}",
        "age": f"{pet.age}",
        "description": f"{pet.description}",
        "image": f"{pet.image}",
        "shelter_username": f"{pet.shelter_username}"
    }
