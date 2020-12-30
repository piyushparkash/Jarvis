from ip2geotools.databases.noncommercial import DbIpCity
from requests import get


class PluginBase:
    def __init__(self, person, settings):
        self.sentences = [
            "where am i"
        ]
        self.person = person
        self.settings = settings

    def main(self):
        return self.sentences

    def respond(self, sentence, index):
        ip = get('https://api.ipify.org').text
        response = DbIpCity.get(ip, api_key='free')

        self.person.speak(f"You are in {response.city}, {response.region}")
