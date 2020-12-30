class PluginBase:
    def __init__(self, person, settings):
        self.sentences = [
            "What is your name"
        ]
        self.person = person
        self.settings = settings;

    def main(self):
        return self.sentences

    def respond(self, sentence):
        self.person.speak(f"My name is {self.settings['name']}")