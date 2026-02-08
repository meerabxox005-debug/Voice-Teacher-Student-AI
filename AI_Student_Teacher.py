import os
import pyttsx3
import requests
import threading
import speech_recognition as sr

# ------------------------------
# OpenRouter API setup
# ------------------------------
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

if not API_KEY:
    print("Error: Set OPENROUTER_API_KEY environment variable first!")
    exit(1)

# ------------------------------
# OpenRouter chat function
# ------------------------------
def openrouter_chat(messages, model="openai/gpt-3.5-turbo"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": model,
        "messages": messages
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print("OpenRouter API error:", response.text)
        return None

    return response.json()["choices"][0]["message"]["content"]

# ------------------------------
# Female voice TTS (async)
# ------------------------------
def speak_female_async(text):
    def run():
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")

        # Select female voice
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break

        engine.setProperty("rate", 150)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    threading.Thread(target=run, daemon=True).start()

# ------------------------------
# Student voice input
# ------------------------------
def listen_student():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Student speaking...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Student:", text)
        return text
    except:
        print("Could not understand. Please speak again.")
        return None

# ------------------------------
# Main program
# ------------------------------
def main():
    print("=== 🎙️ Voice-Based Teacher-Student AI ===")
    print("Say 'exit' to quit.\n")

    messages = [
        {"role": "system", "content": "You are a friendly female AI teacher teaching Python."}
    ]

    while True:
        student_input = listen_student()
        if not student_input:
            continue

        if student_input.lower() == "exit":
            print("Exiting...")
            break

        messages.append({"role": "user", "content": student_input})

        teacher_reply = openrouter_chat(messages)

        if teacher_reply:
            print("Teacher:", teacher_reply)
            speak_female_async(teacher_reply)
            messages.append({"role": "assistant", "content": teacher_reply})

if __name__ == "__main__":
    main()



