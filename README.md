# CLI Chatbot

A command-line chatbot with weather support, Gemini AI integration, voice input, and fun features.

## Features

- **Voice Input** - Type `listen` or say voice commands
- **Text-to-Speech** - Bot speaks responses aloud
- **AI Fallback** - Unknown commands go to Gemini AI
- **Weather** - Get weather info, clothes advice, AQI, UV index, forecast
- **Jokes** - Programming jokes with `pyjokes`
- **Quotes** - Inspirational quotes
- **Calculator** - Basic arithmetic
- **Unit Converter** - Temperature, length, weight
- **Games** - Rock Paper Scissors, Guess the Number
- **Web Browser** - Open Google, YouTube, YouTube Music
- **Chat Memory** - Saves conversation history

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API keys:**
   - Copy `.env.example` to `.env` (already done)
   - Add your API keys:
     - `GEMINI_API_KEY` - Get from [Google AI Studio](https://aistudio.google.com/)
     - `WEATHER_API_KEY` - Get from [OpenWeatherMap](https://openweathermap.org/api)

3. **Run the chatbot:**
   ```bash
   python try_2.py
   ```

## Commands

| Command | Description |
|---------|-------------|
| `hello` / `hi` | Greet the bot |
| `sad` / `happy` | Emotional responses |
| `date` | Current date |
| `time` | Current time |
| `day` | Day of the week |
| `weather` | Get weather info |
| `joke` / `jokes` | Tell a joke |
| `quotes` / `quote` | Show inspirational quote |
| `calculate` | Basic calculator |
| `convert` | Unit converter (temp, length, weight) |
| `rock paper` | Play rock paper scissors |
| `guess number` | Number guessing game |
| `open google` | Open Google in browser |
| `open youtube` | Open YouTube in browser |
| `open music` | Open YouTube Music |
| `listen` | Use voice input |
| `bye` / `exit` | Exit chatbot |

**Tip:** Any unknown command is automatically answered by AI!

## File Structure

```
project-chatbot/
├── try_2.py          # Main chatbot
├── allweather.py     # Weather module
├── gemini.py         # Gemini AI wrapper
├── memory.txt        # Chat history
├── .env              # API keys
├── .env.example      # Example env file
├── requirements.txt  # Python dependencies
├── .gitignore        # Git ignore file
└── README.md         # This file
```

## Chat Memory

All conversations are saved to `memory.txt` with timestamps.
