from cryptography.fernet import Fernet


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
            self.encoded_password = Fernet(key).encrypt(self.password.encode())
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
            # this decodes the password and checks it
            file = open("static/key.key", "rb")
            key = file.read()
            decoded_password = Fernet(key).decrypt(self.encoded_password).decode()
            file.close()
            if password == decoded_password:
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

#Create A Search Form
class SearchForm(FlaskForm):
    searched = StringField("Searched"), validate) = [DataRequired]
    submit = SubmitField("Submit")