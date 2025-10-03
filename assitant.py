import pyttsx3
# from vosk import Model, KaldiRecognizer
# import pyaudio
from perplexipy import PerplexityClient
# 
# Initialize TTS engine (Text to speach engine)
tts_engine = pyttsx3.init()
# voice: String ID of the voice
tts_engine.setProperty('rate', 150)  # Speed percent
# tts_engine.setProperty('voice')
# Get available voices
voices = tts_engine.getProperty('voices')
# for i, voice in enumerate(voices):
#     print(f"Voice {i}: ID={voice.id}, Name={voice.name}, Lang={voice.languages}")

tts_engine.setProperty('voice', voices[1].id)


import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("Preplexity_API_KEY")
# Initialize Perplexity
perplexity = PerplexityClient(key=api_key)  # api-key

# # Initialize speech recognition (Vosk)
# model = Model("path_to_vosk_model")
# rec = KaldiRecognizer(model, 16000)
# mic = pyaudio.PyAudio()
# stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
# stream.start_stream()

# def listen_query():
#     print("Say something...")
#     while True:
#         data = stream.read(4096)
#         if rec.AcceptWaveform(data):
#             result = rec.Result()
#             text = eval(result)['text']
#             if text:
#                 return text

def listen_query():
    user_question = input("say something")
    if user_question:
        return user_question
    
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()
    tts_engine.stop()


chat_history = []

while True:
    # Listen for user's  query
    query = listen_query()
    print("You asked:", query)

    if query.lower() in ["exit", "quit", "bye", "stop"]:
        speak("Goodbye! Have a nice day.")
        break
    
    chat_history.append("User: " + query)

    # Combine chat history into a single prompt string
    prompt = "\n".join(chat_history) + "\nAssistant:"

    # Query perplexity with the full conversation so far
    try:
        answer = perplexity.query(prompt)
    except Exception as e:
        answer = "Sorry, I couldn't process that."
        print("Error:", e)

    print("Answer:", answer)

    chat_history.append("Assistant: " + answer)
    
    # Step 3: Speak out the answer
    speak(answer)

# Remember to handle exceptions, cleanup streams, and close Perplexity session when done!
