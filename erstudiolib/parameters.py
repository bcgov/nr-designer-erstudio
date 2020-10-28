from os import getlogin
from os import getenv

class Parameters():
    def __init__(self):
        self.username = getlogin()
        self.orapass = getenv("ORAPASS")
        self.idirpass = getenv("idirpass")
        self.githubtoken = getenv("gittoken")