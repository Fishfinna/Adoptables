class Pet:
    def __init__(
        self,
        id,
        name="",
        gender="",
        species="",
        age="",
        description="",
        image="",
        data="",
        shelter_username="",
    ):
        """Generates the pet object"""

        if type(name) != str:
            raise TypeError

        if species not in ["dog", "cat", "rodent", "bird", "reptile", "other"]:
            raise ValueError

        if type(gender) != str:
            raise TypeError

        self.id = id
        self.name = name
        self.age = age
        self.species = species
        self.gender = gender
        self.description = description
        if image == "":
            self.image = f"{id}.jpg"
        else:
            self.image = image

        self.data = data
        self.shelter_username = shelter_username

    def __str__(self):
        """The string converter dundar"""
        return f"""< PET name:{self.name} age:{self.age} species:{self.species} gender:{self.gender}>"""

    def to_dict(self):
        """Converts the pet to a dict, in JSON format"""
        return {
            "id": f"{self.id}",
            "name": f"{self.name}",
            "gender": f"{self.gender}",
            "species": f"{self.species}",
            "age": f"{self.age}",
            "description": f"{self.description}",
            "image": f"{self.image}",
            "shelter_username": self.shelter_username,
        }
