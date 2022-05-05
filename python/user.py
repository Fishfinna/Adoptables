from cryptography.fernet import Fernet


class User():
    def __init__(self, username, password):
        """Initalizes the User class"""
        if type(username) != str or type(password) != str:
            raise ValueError

        self.username = username
        self.key = Fernet.generate_key()
        self.password = Fernet(self.key).encrypt(password.encode())

        # Return account information
        self.account = {"username": self.username, "password": self.password}

    def check_password(self, username, password):
        """
        This will return true if the password and username
        entered into the system are in the database
        """
        if type(password) != str:
            raise ValueError

        if username == self.username:
            # this decodes the password and checks it
            decoded_password = Fernet(self.key).decrypt(self.password).decode()
            if password == decoded_password:
                return True
