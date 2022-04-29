
class Pet:
    def __init__(self, id, name="", gender="", species="", age="", description="", image=""):

        if type(name) != str:
            raise TypeError

        if type(species) != str:
            raise TypeError

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

    def __repr__(self):
        return f"""< PET name:{self.name} age:{self.age} species:{self.species} gender:{self.gender}>"""

    def __str__(self):
        return f"""< PET name:{self.name} age:{self.age} species:{self.species} gender:{self.gender}>"""

    def to_dict(self):
        return {
            "id": f"{self.id}",
            "name": f"{self.name}",
            "gender": f"{self.gender}",
            "species": f"{self.species}",
            "age": f"{self.age}",
            "description": f"{self.description}",
            "image": f"{self.image}"
        }
