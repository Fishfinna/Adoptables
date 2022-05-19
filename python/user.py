import bcrypt


class User:
    def __init__(
        self,
        username="",
        password="",
        shelter_name="unkown",
        email="",
        street="",
        city="",
        province="",
        postal="",
        phone="",
    ):
        """Initalizes the User class"""
        if type(username) != str:
            raise ValueError

        self.username = username
        self.password = password
        self.shelter_name = shelter_name
        self.email = email
        self.street = street
        self.city = city
        self.province = province
        self.postal = postal
        self.phone = phone

        if type(password) != bytes:
            file = open("static/key.key", "rb")
            key = file.read()
            encode = password.encode("utf-8")
            self.encoded_password = bcrypt.hashpw(encode, key)
            file.close()
        else:
            self.encoded_password = password

    def check_password(self, username, password):
        """
        This will return true if the password and username
        entered into the system are in the database
        """
        if type(password) != str:
            raise ValueError

        if username == self.username:
            # this encodes the password and checks it
            file = open("static/key.key", "rb")
            key = file.read()
            encode = password.encode("utf-8")
            hashed_password = bcrypt.hashpw(encode, key)
            file.close()
            if hashed_password == self.encoded_password:
                return True
        return False

    def get_account(self):
        """Return account information"""
        return {
            "username": self.username,
            "password": self.encoded_password,
            "shelter_name": self.shelter_name,
            "email": self.email,
            "street": self.street,
            "city": self.city,
            "province": self.province,
            "postal": self.postal,
            "phone": self.phone,
        }
