import json


class Messages:
    username = ""
    sender = ""
    receiver = ""
    text = ""
    IMEI = ""

    # constructor
    def __init__(self, username, sender, receiver, text, IMEI):
        self.username = username
        self.sender = sender
        self.receiver = receiver
        self.text = text
        self.IMEI = IMEI

    # getters
    def getSender(self):
        return self.sender

    def getReceiver(self):
        return self.receiver

    def getUsername(self):
        return self.username

    def getText(self):
        return self.text

    def getIMEI(self):
        return self.IMEI

    # setters
    def setSender(self, sender):
        self.sender = sender

    def setReceiver(self, receiver):
        self.receiver = receiver

    def setUsername(self, username):
        self.username = username

    def setText(self, text):
        self.text = text

    def setIMEI(self, IMEI):
        self.IMEI = IMEI

    # method for creating json with message information
    def createJson(self):
        return {"sender": self.getSender(), "text": self.getText(), "MessageUsername": self.getUsername(),
                "receiver": self.getReceiver(), "IMEI": self.getIMEI()}
