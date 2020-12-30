import os
import json
import _thread
from PyQt5.QtWidgets import (QDialog, QLabel, QHBoxLayout, QGridLayout, QApplication)
import sys
from PluginsLoader import PluginsLoader
from Person import Person

# Load the settings.json
settingsJson = json.load(open('settings.json'))
credJson = open(settingsJson['credJson']).read()
os.environ['PROJECT_ID'] = json.loads(credJson)['project_id']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(settingsJson['credJson'])
voice_name = settingsJson['voice']
name = settingsJson['name']

app = QApplication(sys.argv)


class MainApplication(QDialog):
    styleLabel = QLabel("Text you said!")

    def __init__(self, parent=None):
        super(MainApplication, self).__init__(parent)
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.styleLabel)
        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        self.setLayout(mainLayout)

    def setText(self, text):
        self.styleLabel.setText(text)


gallery = MainApplication()
gallery.show()
person = Person(gallery, settingsJson, credJson)

# Need to load the plugins
pluginLoader = PluginsLoader(person=person, settings=settingsJson)
pluginLoader.loadAllModules()

_thread.start_new_thread(person.keepListening, ())

sys.exit(app.exec_())
