class Error():
    def __init__(self, code=0, message=''):
        self.code = code
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
    