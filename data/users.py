class User:
    def __init__(self, login: str, password: str = 'secret_sauce') -> None:
        self.login = login
        self.password = password

    def __repr__(self) -> str:
        return f'[login="{self.login}"]'


standard_user = User('standard_user')
locked_out_user = User('locked_out_user')
problem_user = User('problem_user')
performance_glitch_user = User('performance_glitch_user')
