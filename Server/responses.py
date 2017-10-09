class Responses:
    response = any

    # constructor
    def __init__(self):
        self.response = {}

    # getters
    def getResponse(self):
        return self.response

    # setters
    def setResponse(self, slug, response):
        self.response[slug] = response
