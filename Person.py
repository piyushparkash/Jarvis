import speech_recognition as sr
from google.cloud import texttospeech
import pyaudio


class Person:
    def __init__(self, app, settings, credJson):
        self.app = app
        self.settings = settings
        self.credJson = credJson
        self.text_callback = None

    def listen_text(self):
        r = sr.Recognizer();
        audio = None
        with sr.Microphone() as source:
            print("Say Something!");
            try:
                audio = r.listen(source);
            except sr.WaitTimeoutError:
                print("Didn't hear anything!")
                return;

        # recognize speech using Google Speech Recognition
        try:
            rec_text = r.recognize_google_cloud(audio_data=audio, credentials_json=self.credJson, language="en_IN")
            print("Heard:" + rec_text)
            if rec_text.startswith(self.settings['name']):
                rec_text = rec_text.replace(self.settings['name'], '')
                rec_text = rec_text.strip()
                self.app.setText(rec_text)

                if self.text_callback is not None:
                    self.text_callback(rec_text)
                else:
                    self.speak("I don't know, how to respond to that!")

            return rec_text
        except sr.UnknownValueError as e:
            print(e)
            return False
        except sr.RequestError as e:
            print(e)
            return False

    def keepListening(self):
        while 1:
            self.listen_text()

    def speak(self, text):
        language_code = "-".join(self.settings['voice'].split("-")[:2])
        text_input = texttospeech.SynthesisInput(text=text)
        voice_params = texttospeech.VoiceSelectionParams(
            language_code=language_code, name=self.settings['voice']
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        client = texttospeech.TextToSpeechClient()
        response = client.synthesize_speech(
            input=text_input, voice=voice_params, audio_config=audio_config
        )

        self.play(response, audio_config)

    def play(self, tone_out, config):
        bytestream = tone_out.audio_content
        pya = pyaudio.PyAudio()
        stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=24000, output=True)
        stream.write(bytestream)
        stream.stop_stream()
        stream.close()

        pya.terminate()
