import os



class Config:
    library_path = "C:/Users/Jim/Desktop/php_pm/library"

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)