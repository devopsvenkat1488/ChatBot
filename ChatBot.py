import openai
import pyttsx3
import speech_recognition as sr
from datetime import datetime
from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import messagebox

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OpenAI API key not found. Make sure to set it in the .env file.")

# Updated function to use the new OpenAI API interface
def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the model you want (GPT-3.5 or GPT-4)
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error with OpenAI API: {e}"

# Voice output using pyttsx3
engine = pyttsx3.init(driverName='sapi5')  # Use SAPI5 explicitly for Windows

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error with speech synthesis: {e}")

# Voice recognition using SpeechRecognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand.")
            speak("Sorry, I could not understand.")
        except sr.RequestError as e:
            print(f"Error with the recognition service: {e}")
            speak("There was an error with the recognition service.")
        return ""

# Greeting based on the time of day
def greet_user():
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning!"
    elif hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"

# Function to send the message when button is clicked
def send_message():
    user_input = user_input_box.get()
    if user_input:
        chat_display.insert(tk.END, f"You: {user_input}\n")
        response = chat_with_gpt(user_input)
        chat_display.insert(tk.END, f"Chatbot: {response}\n")
        speak(response)
        user_input_box.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a message.")

# Function to use speech-to-text
def speech_input():
    user_input = recognize_speech()
    if user_input:
        chat_display.insert(tk.END, f"You: {user_input}\n")
        response = chat_with_gpt(user_input)
        chat_display.insert(tk.END, f"Chatbot: {response}\n")
        speak(response)

# Initialize the UI window
root = tk.Tk()
root.title("Chatbot Assistant")

# Create the UI components
chat_display = tk.Text(root, height=20, width=60, wrap=tk.WORD)
chat_display.grid(row=0, column=0, padx=10, pady=10)

user_input_box = tk.Entry(root, width=50)
user_input_box.grid(row=1, column=0, padx=10, pady=10)

send_button = tk.Button(root, text="Send", width=15, command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

microphone_button = tk.Button(root, text="Speak", width=15, command=speech_input)
microphone_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Run the UI window
root.mainloop()
