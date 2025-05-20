import os
import string
import random
from typing import Union

from gtts import gTTS
from pydub import AudioSegment

DATA_PATH = os.getenv("UPLOAD_PATH")
MISSING = object()
bitrate = 128   # in kbps

def generate_random_ascii(length: int = 20, letters: bool = True, numbers: bool = True, punctuation: bool = False) -> str:
    characters = ''
    if letters:
        characters += string.ascii_letters
    if numbers:
        characters += string.digits
    if punctuation:
        characters += string.punctuation
    return ''.join(random.choices(characters, k=length))

def generate_random_ascii_path(file_name: Union[str, object] = MISSING) -> str:
    if file_name == MISSING:
        file_name = generate_random_ascii()
    return os.path.join(DATA_PATH, file_name)

def generate_mp3_tts(text_to_speech: str = "Test FLOSScast", lang: str = "de") -> str:
    tts = gTTS(text=text_to_speech, lang=lang, lang_check=True, timeout=60)
    path = generate_random_ascii_path(generate_random_ascii()) + ".mp3"
    tts.save(path)
    return path

def calculate_mp3_duration(size: int) -> int:
    '''
    Formula for roughly calculating the correlating mp3 file size for a duration.
    Size in kilobyte = (Bitrate in kilobit per second * Duration in seconds)  / 8
    '''
    return int((size * 8) / bitrate)

def generate_mp3_size(kilobyte: int = 2048, path: Union[str, object] = MISSING) -> str:
    if path == MISSING:
        path = generate_random_ascii_path(generate_random_ascii())
    length = calculate_mp3_duration(kilobyte)
    silent_audio = AudioSegment.silent(duration=length * 1000)  # *1000 because it is in ms
    path += ".mp3"
    silent_audio.export(path, format="mp3", bitrate=f"{bitrate}k")
    return path

def generate_mp3_duration(duration: int = 60, path: Union[str, object] = MISSING) -> str:
    if path == MISSING:
        path = generate_random_ascii_path(generate_random_ascii())
    silent_audio = AudioSegment.silent(duration=duration * 1000)
    path += ".mp3"
    silent_audio.export(path, format="mp3", bitrate=f"{bitrate}k")
    return path