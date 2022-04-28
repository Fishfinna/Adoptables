
class Pet:
    def __init__(self, id: int, name="", gender="", species="", age=0):
        if type(age) != int:
            age = int(age)

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

    def __repr__(self):
        return f"""< PET name:{self.name} age:{self.age} species:{self.species} gender:{self.gender}>"""

    def __str__(self):
        return f"""< PET name:{self.name} age:{self.age} species:{self.species} gender:{self.gender}>"""

    def to_dict(self):
        return {"name": {self.name}, "age": {self.age}, "species": {self.species}, "gender": {self.gender}}
