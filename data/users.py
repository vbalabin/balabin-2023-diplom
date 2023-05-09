class User:
    def __init__(self, login: str, password: str = 'secret_sauce') -> None:
        self.login = login
        self.password = password


standard_user = User('standard_user')
