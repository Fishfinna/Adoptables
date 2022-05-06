from cryptography.fernet import Fernet


class User():
    def __init__(self, username, password):
        """Initalizes the User class"""
        if type(username) != str or type(password) != str:
            raise ValueError

        self.username = username

        file = open('static/key.key', 'rb')
        key = file.read()
        self.password = Fernet(key).encrypt(password.encode())
        file.close()

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
            file = open('static/key.key', 'rb')
            key = file.read()
            decoded_password = Fernet(key).decrypt(
                self.password).decode()
            file.close()
            if password == decoded_password:
                return True
        return False
