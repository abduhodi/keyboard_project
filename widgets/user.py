class User:
    def __init__(self, name: str, email: str, telegramId: str, passwd: str, easy=0, medium=0, hard=0, expert=0) -> None:
        self.name = name
        self.email = email
        self.passwd = passwd
        self.telegramId = telegramId
        self.easy = easy
        self.medium = medium
        self.hard = hard
        self.expert = expert
