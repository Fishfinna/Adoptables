from .pet import Pet
import json


class App:
    def __init__(self):
        with open("data/pets.json") as file:
            data = json.load(file)

            self.pets = [Pet(*i.values()) for i in data]

    def get_by_id(self, id):
        if [i for i in self.pets if i.id == id] != []:
            return [i for i in self.pets if i.id == id][0]

    def get_pets(self):
        return self.pets

    def delete_by_id(self, id):
        self.pets = [i for i in self.pets if i.id != id]
        self.save()

    def put_pet(self, **kwargs):
        original = self.get_by_id(kwargs["id"])
        new = original.update(**kwargs)
        self.delete_pet(original)
        self.post_pet(new)
        self.save()

    def post_pet(self, instance):
        if type(instance) not in [dict, Pet]:
            raise ValueError

        if type(instance) != Pet:
            instance = Pet(instance)

        self.pets.append(instance)
        self.save()

    def save(self):
        with open("data/pets.json", "w") as file:
            json.dump([pet.to_dict() for pet in self.pets], file)
