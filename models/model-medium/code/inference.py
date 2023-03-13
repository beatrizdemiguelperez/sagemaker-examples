import datetime
import json
import time

import whisper


def input_fn(json_request_data, content_type="application/json"):
    input_data = json.loads(json_request_data)
    print("Input data is processed")
    return input_data


def model_fn(model_dir):
    model = whisper.load_model("medium")
    return model


def predict_fn(input_data, model):
    audio_url = input_data["audio_url"]
    audio_length = input_data["audio_length"]

    print(f"got a new file to transcribe, audio_url is {audio_url} ")

    start_time = time.time()
    result = model.transcribe(audio_url)
    end_time = time.time()

    print(result["text"])
    print(
        "--- transcription duration %s seconds ---"
        % (str(datetime.timedelta(seconds=(end_time - start_time))))
    )
    print("--- ratio t/d %s seconds ---" % str((end_time - start_time) / audio_length))

    # print the recognized text
    return {
        "detected_language": result["language"],
        "transcription": result["text"],
        "audio_url": audio_url,
        "audio_length": audio_length,
    }
