class PluginsLoader:
    def __init__(self, person, settings):
        self.person = person
        self.loadedModules = {};
        self.settings = settings
        person.text_callback = self.globalResponse

    def loadAllModules(self):
        try:
            from importlib import import_module
            import os

            ignoreDirectories = [
                "__pycache__"
            ]
            # scan this directory for plugins
            obj = os.scandir('./plugins')

            for entry in obj:
                # Should I ignore the directory
                try:
                    ignoreDirectories.index(entry.name)
                    continue
                except ValueError:
                    print()

                # Process Valid directory and import
                if entry.is_dir():
                    print(f"Trying to Load Module: {entry.name}")
                    try:
                        moduleName = f"plugins.{entry.name}.{entry.name}"
                        current_module = import_module(moduleName).PluginBase(self.person, self.settings)
                        registeredSentences = current_module.main()
                        self.addToLoadedModule(moduleName, sentences=registeredSentences, instance=current_module)

                    except Exception as e:
                        print(f"Unable to load Module {entry.name}. Reason: {e}")
        except Exception as e:
            print(e)
        finally:
            print("All Modules Loaded!")

    def addToLoadedModule(self, moduleName, sentences, instance):
        print(f"Loaded Module: {moduleName}")
        self.loadedModules[moduleName] = {'instance': instance, 'registeredSentences': sentences};

    def globalResponse(self, sentence):
        '''
        Check through the plugins registered sentences and see if anything matches
        :param sentence: string
        '''

        for module in self.loadedModules:
            for idx, regSentence in enumerate(self.loadedModules[module]['registeredSentences']):
                if regSentence.lower() == sentence.lower():
                    # We found the sentence
                    self.loadedModules[module]['instance'].respond(sentence.lower(), idx)
                    return True

        return False

