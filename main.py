import random
import webbrowser
import pyjokes
import inspirational_quotes
from datetime import datetime
from dotenv import load_dotenv
import allweather
import gemini
import os
import threading

load_dotenv()

# Text-to-speech setup using gTTS (works on all platforms)
TTS_AVAILABLE = True


def speak(text):
    """Speak the given text using gTTS."""
    if not TTS_AVAILABLE:
        return
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='en')
        tts.save("temp_speech.mp3")
        # Use xdg-open for Linux, afplay for macOS
        os.system("xdg-open temp_speech.mp3 >/dev/null 2>&1 &")
    except Exception:
        pass  # Silently fail if audio not available


def listen():
    """Listen for voice input - uses whisper if available, else speech_recognition."""
    try:
        import sounddevice as sd

        print("\n🎤 Recording... (5 seconds max)")

        # Record audio
        duration = 5
        sample_rate = 16000
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()

        # Save as WAV
        import wave
        with wave.open("temp_audio.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())

        # Fallback to speech_recognition (Google API)
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.AudioFile("temp_audio.wav") as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            os.remove("temp_audio.wav")
            return text.lower() if text else None
        except Exception:
            pass

        os.remove("temp_audio.wav")
        print("Couldn't understand audio")

    except ImportError:
        print("Install sounddevice: pip install sounddevice")
    except Exception as e:
        print(f"Voice error: {e}")
    return None


# Greeting based on time
current_hour = datetime.now().hour
if current_hour <= 12:
    greeting = "Good Morning!"
elif current_hour < 18:
    greeting = "Good Afternoon!"
else:
    greeting = "Good Evening!"

print(greeting)

user_name = input("Your name > ")
print(f"Nice to meet you, {user_name}!")
speak(f"Nice to meet you, {user_name}")

# Save greeting to memory
with open("memory.txt", "a") as f:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    f.write(f"[{timestamp}] bot: {greeting}\n")
    f.write(f"[{timestamp}] bot: Nice to meet you, {user_name}!\n")

# Response pools
sad_replies = ["I'm with you", "It's okay, breathe", "Talk to me", "Got you"]
greetings = ["Hello!", "Hi!", "Yoooo!", "Hey there!"]


def save_to_memory(role, message):
    """Save message to memory with timestamp."""
    with open("memory.txt", "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"[{timestamp}] {role}: {message}\n")


def get_ai_response(query):
    """Get response from Gemini AI."""
    try:
        reply = gemini.generate_response(query)
        return reply
    except Exception as e:
        return f"AI Error: {e}"


def weather_menu(data):
    """Weather submenu."""
    while True:
        print("\n--- Weather Menu ---")
        print("1 --> What clothes to wear")
        print("2 --> Safe to drive")
        print("3 --> Mask required (AQI)")
        print("4 --> UV Index")
        print("5 --> 5-Day Forecast")
        print("6 --> Humidity advice")
        print("7 --> Current weather")
        print("8 --> Wind speed")
        print("9 --> Feels like temperature")
        print("10 --> Visibility")
        print("11 --> Weather alert")
        print("12 --> Back")

        try:
            choice = int(input("\nEnter choice (1-12): "))
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        if choice == 1:
            print(allweather.clothes(data))
        elif choice == 2:
            print(allweather.drive(data))
        elif choice == 3:
            print(allweather.aqi(data))
        elif choice == 4:
            print(allweather.uvi(data))
        elif choice == 5:
            allweather.forecast(data)
        elif choice == 6:
            print(allweather.humid(data))
        elif choice == 7:
            print(f"Weather: {data['weather'][0]['main']} - {data['weather'][0]['description']}")
        elif choice == 8:
            print(f"Wind Speed: {data['wind']['speed']} m/s")
        elif choice == 9:
            print(f"Feels like: {data['main']['feels_like']}°C")
        elif choice == 10:
            print(f"Visibility: {data['visibility']} meters")
        elif choice == 11:
            print(allweather.alert(data))
        elif choice == 12:
            break
        else:
            print("Invalid choice. Try 1-12.")


def rock_paper_scissors():
    """Rock Paper Scissors game."""
    choices = ["rock", "paper", "scissors"]
    user_score = 0
    bot_score = 0

    print("\n--- Rock Paper Scissors ---")
    print("Enter 'rock', 'paper', or 'scissors'. Type 'exit' to quit.")

    while True:
        user_choice = input("\nYour choice: ").lower().strip()
        if user_choice == "exit":
            break
        if user_choice not in choices:
            print("Invalid choice!")
            continue

        bot_choice = random.choice(choices)
        print(f"Bot chose: {bot_choice}")

        if user_choice == bot_choice:
            result = "Tie!"
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "paper" and bot_choice == "rock") or \
             (user_choice == "scissors" and bot_choice == "paper"):
            result = "You win!"
            user_score += 1
        else:
            result = "Bot wins!"
            bot_score += 1

        print(f"{result} | Score - You: {user_score}, Bot: {bot_score}")

    return f"Final Score - You: {user_score}, Bot: {bot_score}"


def guess_number():
    """Guess the number game."""
    secret = random.randint(1, 100)
    tries = 0

    print("\n--- Guess the Number (1-100) ---")
    print("I'm thinking of a number between 1 and 100.")

    while True:
        try:
            guess = int(input("Your guess: "))
        except ValueError:
            print("Enter a valid number!")
            continue

        tries += 1

        if guess == secret:
            return f"Correct! The number was {secret}. You got it in {tries} tries!"
        elif guess > secret:
            print("Lower!")
        else:
            print("Higher!")


def unit_converter():
    """Unit conversion utility."""
    print("\n--- Unit Converter ---")
    print("1 --> Temperature (C/F/K)")
    print("2 --> Length (m/ft/km/miles)")
    print("3 --> Weight (kg/lbs)")
    print("4 --> Back")

    try:
        choice = int(input("Choose type: "))
    except ValueError:
        return "Invalid input"

    if choice == 1:
        temp = float(input("Temperature: "))
        unit = input("Unit (C/F/K): ").upper()
        if unit == "C":
            return f"{temp}°C = {temp*9/5+32:.1f}°F = {temp+273.15:.1f}K"
        elif unit == "F":
            return f"{temp}°F = {(temp-32)*5/9:.1f}°C = {(temp-32)*5/9+273.15:.1f}K"
        elif unit == "K":
            return f"{temp}K = {temp-273.15:.1f}°C = {(temp-273.15)*9/5+32:.1f}°F"
    elif choice == 2:
        val = float(input("Length: "))
        unit = input("Unit (m/ft/km/miles): ").lower()
        if unit == "m":
            return f"{val}m = {val*3.281:.1f}ft = {val/1000:.3f}km = {val/1609:.3f}miles"
        elif unit == "ft":
            return f"{val}ft = {val/3.281:.1f}m = {val/3281:.3f}km = {val/5280:.3f}miles"
        elif unit == "km":
            return f"{val}km = {val*1000:.0f}m = {val*3281:.0f}ft = {val*0.621:.2f}miles"
        elif unit == "miles":
            return f"{val}miles = {val*1609:.0f}m = {val*1.609:.2f}km = {val*5280:.0f}ft"
    elif choice == 3:
        val = float(input("Weight: "))
        unit = input("Unit (kg/lbs): ").lower()
        if unit == "kg":
            return f"{val}kg = {val*2.205:.1f}lbs"
        elif unit == "lbs":
            return f"{val}lbs = {val/2.205:.1f}kg"

    return "Invalid conversion"


# Main chat loop
print("\nSay 'listen' to use voice input, or just type your message!")
print("Say 'bye' or 'exit' to quit.\n")

while True:
    user_input = input("\n> ").lower().strip()

    # Voice input mode
    if user_input == "listen":
        voice_input = listen()
        if voice_input:
            user_input = voice_input
        else:
            continue

    if not user_input:
        continue

    # Save user message
    save_to_memory("user", user_input)

    reply = None

    # Core commands
    if user_input in ["hello", "hi"]:
        reply = f"{random.choice(greetings)}, {user_name}!"

    elif "sad" in user_input:
        reply = random.choice(sad_replies)

    elif "happy" in user_input:
        reply = "Keep shining!"

    elif "date" in user_input:
        reply = datetime.now().strftime("%d %B %Y")

    elif "time" in user_input:
        reply = datetime.now().strftime("%H:%M %p")

    elif "day" in user_input:
        reply = datetime.now().strftime("%A")

    elif "open google" in user_input:
        webbrowser.open("https://google.com")
        reply = "Opening Google..."

    elif "open youtube" in user_input:
        webbrowser.open("https://youtube.com")
        reply = "Opening YouTube..."

    elif "open music" in user_input:
        webbrowser.open("https://music.youtube.com/")
        reply = "Opening YouTube Music..."

    elif "joke" in user_input or "jokes" in user_input:
        reply = pyjokes.get_joke()

    elif "quote" in user_input:
        quote_data = inspirational_quotes.quote()
        reply = f'"{quote_data["quote"]}" - {quote_data["author"]}'

    elif "rock paper" in user_input:
        reply = rock_paper_scissors()

    elif "guess number" in user_input:
        reply = guess_number()

    elif "weather" in user_input:
        city = input("Enter city name: ").lower().strip()
        try:
            data = allweather.fetch(city)
            print(f"\n--- Weather in {data['name']} ---")
            print(f"{data['weather'][0]['main']} - {data['weather'][0]['description']}")
            print(f"Temperature: {data['main']['temp']}°C (Feels like {data['main']['feels_like']}°C)")
            print(f"Humidity: {data['main']['humidity']}%")
            weather_menu(data)
            reply = None
        except Exception as e:
            reply = f"Error: {e}"

    elif "convert" in user_input or "converter" in user_input:
        reply = unit_converter()

    elif "calculate" in user_input:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            op = input("Enter operator (+, -, *, /, %): ")

            if op == "+":
                result = num1 + num2
            elif op == "-":
                result = num1 - num2
            elif op == "*":
                result = num1 * num2
            elif op == "/":
                if num2 == 0:
                    reply = "Cannot divide by zero!"
                else:
                    result = num1 / num2
            elif op == "%":
                result = num1 % num2
            else:
                reply = "Invalid operator!"

            if reply is None:
                reply = f"The result of {num1} {op} {num2} = {result}"
        except ValueError:
            reply = "Invalid number!"

    elif "bye" in user_input or "exit" in user_input:
        reply = "Talk later! Goodbye!"
        save_to_memory("bot", reply)
        print(reply)
        speak(reply)
        break

    elif "help" in user_input or "commands" in user_input:
        help_text = """
Available Commands:
------------------
• hello / hi         - Greet the bot
• sad / happy        - Emotional responses
• date / time / day  - Show current date/time/day
• weather            - Get weather info
• joke / jokes       - Tell a programming joke
• quotes / quote     - Show inspirational quote
• calculate          - Basic calculator (+, -, *, /, %)
• convert            - Unit converter (temp, length, weight)
• rock paper         - Play rock paper scissors
• guess number       - Number guessing game
• open google        - Open Google
• open youtube       - Open YouTube
• open music         - Open YouTube Music
• listen             - Use voice input
• bye / exit         - Exit the chatbot
"""
        reply = help_text

    # If no command matched, use AI
    else:
        print("\n Asking AI...")
        reply = get_ai_response(user_input)

    # Print and save bot reply
    if reply:
        print(reply)
        save_to_memory("bot", reply)
        # Speak in background to not block
        threading.Thread(target=speak, args=(reply,), daemon=True).start()
