import whisper

class Transcriber(object):
    def __init__(self, config):
        self._whisper_model = None
        self._config = config

    @property
    def whisper_model(self):
        if self._whisper_model is None:
            self._whisper_model = whisper.load_model(self._config["model_name"])
        return self._whisper_model

    def transcribe(self, audio_url, language="en"):
        result = self.whisper_model.transcribe(audio_url, language=language)
        text = result["text"]
        return text
