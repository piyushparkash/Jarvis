from datetime import datetime


class PluginBase:
    def __init__(self, person, settings):
        self.sentences = [
            "what is the time",
            "What is the date"
        ]
        self.person = person
        self.settings = settings

    def main(self):
        return self.sentences

    def respond(self, sentence, index):
        now = datetime.now()  # current date and time
        if index == 0:
            self.person.speak(now.strftime("%H:%M:%S"))
        elif index == 1:
            self.person.speak(now.strftime("%m/%d/%Y"))
