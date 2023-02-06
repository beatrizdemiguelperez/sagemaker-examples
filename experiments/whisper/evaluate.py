import argparse
import os

from transcriber import Transcriber


def main(i_path, o_path):
    model = Transcriber({"model_name": "base"})
    print("%% Model loaded...")
    print(os.getcwd())
    print(os.listdir(i_path))
    for file in os.listdir(i_path):
        suffix = ".mp3"
        if file.endswith(suffix):
            i_file = os.path.join(i_path, file)
            print(f"%% transcribing {i_file}...")
            transcribe_output = model.transcribe(i_file)
            print("%% Saving results...")
            if not os.path.isdir(o_path):
                os.mkdir(o_path)
            transcription_path = os.path.join(
                o_path, f"{file}.txt"
            )
            f= open(transcription_path,"w+")
            f.write(transcribe_output)
            f.close()

"""
Take a directory and transcribe mp3 files
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="Path of folder with input mp3files", type=str, required=True)
    parser.add_argument("-o", "--output_path", help="Path to output folder", type=str, required=True)

    args = parser.parse_args()
    main(args.input_path, args.output_path)
    
    print("%% Done")
