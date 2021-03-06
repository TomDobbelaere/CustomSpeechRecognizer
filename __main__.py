import speech_recognition as sr
import subprocess
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api = os.getenv("API")
apikey = os.getenv("API_KEY")

r = sr.Recognizer()
m = sr.Microphone()

try:
    print("A moment of silence, please...")
    with m as source:
        r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source:
            audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(value).encode("utf-8"))
            else:  # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(value))

            try:
                req = requests.get(url=api, params={"k": apikey, "q": value})
                data = req.json()
                print(data)

                if "text" in data:
                    proc = subprocess.Popen(
                        [
                            "espeak",
                            "-v",
                            str(data["voice"]),
                            "-s",
                            str(data["speed"]),
                            "-p",
                            str(data["pitch"]),
                            str(data["text"]),
                        ]
                    )
                    proc.communicate()
            except Exception as e:
                print(e)
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print(
                "Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(
                    e
                )
            )
except KeyboardInterrupt:
    pass
