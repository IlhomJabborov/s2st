import os
import time
import pygame
from gtts import gTTS
import speech_recognition as sr
from googletrans import LANGUAGES, Translator
import subprocess

translator = Translator()
pygame.mixer.init()

language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src=from_language, dest=to_language)

def text_to_voice(text_data, to_language):
    if to_language == "uz":
        to_language = "uz-UZ-MadinaNeural"
    elif to_language == "ru":
        to_language = "ru-RU-SvetlanaNeural"
    elif to_language == "en":
        to_language = "en-US-JennyNeural"

    output_file = "output_uzbek.mp3"

    command = [
        "edge-tts",
        "--text", text_data,
        "--voice", to_language,
        "--write-media", output_file
    ]
    
    subprocess.run(command, check=True)

    audio = pygame.mixer.Sound(output_file)
    audio.play()
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)

    os.remove(output_file)

def main_process(from_language, to_language):
    is_translate_on = True

    while is_translate_on:
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)

        try:
            print("Processing...")
            spoken_text = rec.recognize_google(audio, language=from_language)

            print("Translating...")
            translated_text = translator_function(spoken_text, from_language, to_language)

            print(f"Original: {spoken_text}")
            print(f"Translated: {translated_text.text}")

            text_to_voice(translated_text.text, to_language)

        except Exception as e:
            print(f"Error: {e}")


from_language = "en"  
to_language = "ru"    


print("Press Ctrl+C to stop the program.")
try:
    main_process(from_language, to_language)
except KeyboardInterrupt:
    print("Translation process stopped.")
