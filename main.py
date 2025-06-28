import os
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import webbrowser
import requests
from datetime import datetime
import musicLibrary
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pywhatkit
import pyaudio
import newsapi

#API & model
client = genai.configure(api_key="GEMINI_API") # Gemini API
model = genai.GenerativeModel("gemini-2.5-flash") # Gemini Model
news_api ='NEWS_API' # News API

# Set up Spotify API access
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="76a6a4a2a2b44ed2a161f21b364981b8",
    client_secret="af385b01289047a6bb5ad720c2b952ae"
))

# Initializing Text-to-Speech
engine = pyttsx3.init()

# Greetings for the User  
def greet_user():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        greeting = "Good Morning Gojo! How May I Help You?"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon Gojo! How May I Help You?"
    elif 17 <= current_hour < 22:
        greeting = "Good Evening Gojo! How May I Help You?"
    else:
        greeting = "Good Evening! How May I Help You?"

    print(greeting)
    speak(greeting)

# Function to get Weather Update
def speak(text):
    print(f"🔊 {text}")
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    api_key = "WEATHER_API_KEY"  # Replace with your actual Weather API key
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=yes"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        # Extract desired info
        location = data['location']['name']
        temp_c = data['current']['temp_c']
        condition = data['current']['condition']['text']
        humidity = data['current']['humidity']
        wind_kph = data['current']['wind_kph']

        print(f"Weather in {location}:")
        speak(f"Weather in {location}:")
        print(f"Condition: {condition}")
        speak(f"Condition: {condition}")
        print(f"Temperature: {temp_c}°C")
        speak(f"Temperature: {temp_c}°C")
        print(f"Humidity: {humidity}%")
        speak(f"Humidity: {humidity}%")
        print(f"Wind: {wind_kph} kph")
        speak(f"Wind: {wind_kph} kph")

        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching weather data:", e)
        return None

# Example usage
def speak(text):
    print("🔊", text)  # Replace with pyttsx3 or your voice function


# Integrating News_API to get Technical News
def get_news_titles(news_api , command):
    if "tech news" in command.lower():
        try:
            # Make the API request
            r = requests.get(f"https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={news_api}")

            # Check for successful response
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])

                if not articles:
                    speak("No news articles found.")
                    return

                # Speak and print headlines
                for article in articles:
                    print(article['description'])
                    speak(article['description'])
            else:
                speak(f"Failed to fetch news. Status code: {r.status_code}")

        except Exception as e:
            speak(f"An error occurred: {e}")
    else:
        print("Please specify the category of news you want, like 'tech news'.")
        speak("Please specify the category of news you want, like 'tech news'.")

# Integrating Gemini as AI
def gemini(command):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(f"You are personal and virtual assistant named ULTRON. {command} in a consice communicative way.")
    print(response.text)
    speak(response.text)

# Text to Speech Function
def speak(text):
    engine.say(text)
    engine.runAndWait()

#  For opening APPS
def openApps(app):
    app = app.lower()
    if "open spotify" in app.lower() or "open spotify app" in app.lower():
        speak("Opening Spotify")
        os.startfile(r'C:\Users\JoySengupta521\AppData\Roaming\Spotify\Spotify.exe')

    elif "open browser" in app.lower() or "open chrome" in app.lower():
        speak("Opening Chrome Browser")
        os.startfile(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')

    elif "open word" in app.lower() or "open microsoft word" in app.lower():
        speak("Opening Microsoft Word")
        os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk")

    elif "open excel" in app.lower() or "open microsoft excel" in app.lower():
        speak("Opening Microsoft Excel")
        os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk")

    elif "open powerpoint" in app.lower() or "open microsoft powerpoint" in app.lower():
        speak("Opening Microsoft PowerPoint")
        os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint.lnk")

    elif "open photoshop" in app.lower() or "open adobe photoshop" in app.lower():
        speak("Opening Adobe Photoshop")
        os.startfile(r"C:\Program Files\Adobe\Adobe Photoshop CC 2019\Photoshop.exe")

    elif "open access" in app.lower() or "open microsoft access" in app.lower():
        speak("Opening Microsoft Access")
        os.startfile(r"C:\Program Files (x86)\Microsoft Office\root\Office16\MSACCESS.EXE")

    elif "open firefox" in app.lower() or "open mozilla firefox" in app.lower():
        speak("Opening Mozilla Firefox")
        os.startfile(r"C:\Program Files\Mozilla Firefox\firefox.exe")

    elif "open file explorer" in app.lower() or "open explorer" in app.lower():
        speak("Opening File Explorer")
        os.startfile("explorer")

    elif "open vs code" in app.lower() or "open visual studio code" in app.lower():
        speak("Opening Visual Studio Code")
        os.startfile(r"C:\Users\<YourUsername>\AppData\Local\Programs\Microsoft VS Code\Code.exe")

    elif "open github" in app.lower() or "open github desktop" in app.lower():
        speak("Opening GitHub Desktop")
        os.startfile(r"C:\Users\JoySengupta521\AppData\Local\GitHubDesktop\GitHubDesktop.exe")

    elif "open terminal" in app.lower() or "open command prompt" in app.lower():
        speak("Opening Command Prompt")
        os.startfile(r"C:\Windows\System32\cmd.exe")

    elif "open notepad" in app.lower() or "open microsoft notepad" in app.lower():
        speak("Opening Notepad")
        os.startfile(r"C:\Windows\System32\notepad.exe")

    elif "open paint" in app.lower() or "open microsoft paint" in app.lower():
        speak("Opening Microsoft Paint")
        os.startfile(r"C:\Windows\System32\mspaint.exe")

    elif "open calculator" in app.lower() or "open windows calculator" in app.lower():
        speak("Opening Calculator")
        os.startfile(r"C:\Windows\System32\calc.exe")

    elif "open microsoft edge" in app.lower() or "open edge browser" in app.lower():
        speak("Opening Microsoft Edge")
        os.startfile(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    else:
        app = app.split(" ")[-1]  # Get the last word as app name
        try:
            os.startfile(app)  # Search for the app in the system
        except Exception as e:
            print(f"Error searching for {app}: {e}")

# Playing Music
def playMusic(command):
    if "spotify" in command.lower():
        
        # Extract song name (e.g., "play spotify shape of you" -> "shape of you")
        song_query = command.lower().replace("play", "").replace("spotify", "").replace("on spotify", "").replace("on" , "").strip()
        get_spotify_track_link(song_query)

        # Search for the song
        # results = f"https://open.spotify.com/search/{song_query}"
        # webbrowser.open(results) 

    elif "youtube" in command.lower():
        speak(f"Playing {command}")
        pywhatkit.playonyt(command)
    else:
        if len(command.split(" ")) == 2:
            song = command.lower().split(" ")[1]
            link = musicLibrary.ytvideo[song]
            webbrowser.open(link)

        elif len(command.split(" ")) == 3:
            song1 = command.lower().split(" ")[1]
            song2 = command.lower().split(" ")[2]
            song = song1 + " " + song2
            link = musicLibrary.ytvideo[song]
            webbrowser.open(link)
        else:
            speak("Sorry, I can't find that song in my library.")
            return
        
# Function to get Spotify track link from track name
def get_spotify_track_link(track_name):
    results = sp.search(q=track_name, type='track', limit=1)
    tracks = results.get('tracks', {}).get('items', [])
    if tracks:
        track = tracks[0]
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        url = track['external_urls']['spotify']
        webbrowser.open(url)
        return f"🎵 Found: {track_name} by {artist_name}\n🔗 Link: {url}"
    else:
        return "❌ No track found for that name."

# For Opening Links
def openLinks(link):
    if "google" in link.lower():
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "youtube" in link.lower():
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "linkedin" in link.lower():
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif "youtube" in link.lower():
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "instagram" in link.lower():
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")
    elif "facebook" in link.lower():
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "github in chrome" in link.lower():
        speak("Opening GitHub in Chrome")
        webbrowser.open("https://github.com")
    elif "chatgpt" in link.lower():
        speak("Opening ChatGPT")
        webbrowser.open("https://chat.openai.com/")
    elif "grok" in link.lower():
        speak("Opening Grok")
        webbrowser.open("https://grok.com/")

# Main function
if __name__ == "__main__" :
    print("Initializing ULTRON...")
    speak("Initializing ULTRON")
    greet_user()
    while True:
        r = sr.Recognizer() 
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            print("Recognizing.......")
            audio = r.listen(source , phrase_time_limit=1)
        try:
            command = r.recognize_google(audio)
            print(command)
            if command.lower() == "ultron":
                speak("Ya") 
                with sr.Microphone() as source:

                    print("ULTRON Activated")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    print(command)
                    if "who r u" in command.lower() or "hu r u" in command.lower() or "who are you" in command.lower():
                        speak("I am ULTRON, your personal assistant. How can I assist you today?")
                    elif "time" in command.lower():
                        current_time = datetime.now().strftime("%H:%M")
                        speak(f"The current time is {current_time}")
                    elif "date" in command.lower():
                        current_date = datetime.now().strftime("%Y-%m-%d")
                        speak(f"Today's date is {current_date}")
                    elif "how are you" in command.lower() or "how r u" in command.lower() or "how are you doing" in command.lower():
                        speak("I'm good sir, thank you for asking! How can I assist you today?")
                    elif "weather" in command.lower():
                        city = command.split(" ")[-1] if len(command.split(" ")) > 2 else "London"
                        speak(f"Getting weather information for {city}")
                        get_weather(city)
                    elif "open" in command.lower():
                        openApps(command)
                        openLinks(command)
                    elif "exit" in command.lower():
                        exit()
                    elif "news" in command.lower():
                        get_news_titles(news_api , command) 
                    elif "play" in command.lower():
                        playMusic(command)
                    else:
                        gemini(command)
        except Exception as e:
            print("Error {0}".format(e))
            continue