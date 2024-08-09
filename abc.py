import json
import os
import sys
import pyjokes
import pyttsx3
import time
import speech_recognition as sr
import pyaudio
import datetime
import requests
import webbrowser
import wikipedia
import smtplib
import pyautogui
from PIL import Image
from bs4 import BeautifulSoup
import pywhatkit
import random
import threading
import google.generativeai as genai
import customtkinter

# appearance setting gui
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x600")
app.title("VOICE ASSISTANT..... :)")



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open the audio stream
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)

    print("Listening...")

    # Variables to accumulate audio data
    audio_data = []
    timeout_seconds = 7  # Adjust as needed
    start_time = time.time()  # Get current time

    # Record audio input
    while time.time() - start_time < timeout_seconds:
        chunk = stream.read(1024)
        audio_data.append(chunk)

    print("Recognizing...")

    # Convert the accumulated audio data to a single bytearray
    audio_bytes = b"".join(audio_data)

    # Use speech recognition to transcribe audio data
    try:
        # Convert the audio bytes to an AudioData object
        audio_data = sr.AudioData(audio_bytes, sample_rate=44100, sample_width=2)
        query = r.recognize_google(audio_data)
        print(f"user said: {query}")
        return query
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        print("Listening...")
    except sr.RequestError as e:
        speak("Sorry, I'm having trouble. Please try again later.")
        print("Listening...")

    # Close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return "none"


def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")
    if 0 <= hour <= 12:
        speak(f"Good morning, its {tt}")
    elif 12 <= hour <= 18:
        speak(f"Good afternoon, its {tt}")
    else:
        speak(f"Good evening, its {tt}")
    speak("How may I assist you")


def news(source='techcrunch', count=5):
    api_key = "5d0eb078c4644dacaf809d8af5b189c0"
    main_url = f'https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=5d0eb078c4644dacaf809d8af5b189c0'
    try:
        main_page = requests.get(main_url).json()
        articles = main_page["articles"][:count]
        for i, article in enumerate(articles):
            speak(f"Headline {i + 1}: {article['title']}")
    except Exception as e:
        speak("Sorry, I'm unable to fetch the news at the moment. Please try again later.")
        print(e)


def scrape_quotes():
    url = 'http://quotes.toscrape.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('span', class_='text')
    for quote in quotes:
        speak(quote.text)


SCREENSHOT_DIR = "C://Users//HARSH KUMAR SONI//Documents//OneDrive//Pictures//Screenshots 1"



def take_screenshot():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    image_path = os.path.join(SCREENSHOT_DIR, filename)
    image = pyautogui.screenshot()
    image.save(image_path)
    Image.open(image_path).show()


def open_notepad():
    notepad_path = r"C:\Windows\system32\notepad.exe"
    os.startfile(notepad_path)


def write_notepad():
        speak("What do you want to write in Notepad?")
        content = takecommand()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"notepad_{timestamp}.txt"
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, "w") as f:
            f.write(content)
        os.startfile(filepath)
        speak("File saved.")

def tell_joke():
    joke = pyjokes.get_joke()
    print(joke)
    speak(joke)


def play_youtube():
    speak("What do you want me to search on YouTube?")
    search_query = takecommand()
    speak(f"Playing {search_query} on YouTube")
    pywhatkit.playonyt(search_query)


def search_google():
    speak("What do you want to search on Google?")
    query = takecommand()
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)


def search_wikipedia():
    try:
        speak("What do you want to search on wikipedia?")
        query = takecommand()
        results = wikipedia.search(query)
        page = wikipedia.page(results[0])
        summary = wikipedia.summary(page.title, sentences=3)
        print(summary)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Multiple results found for {query}. Please specify the query further.")
    except wikipedia.exceptions.PageError as e:
        print(f"Page for {query} not found on Wikipedia.")


def send_email():
    speak("Please enter the recipient's email address.")
    receiver_email = input("Recipient's email address: ").strip().lower()
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    try:
        s.login("rishu930023@gmail.com", "qnthmdibsvvxebhf")
        speak("Successfully authenticated with SMTP server")
    except Exception as e:
        print("SMTP login failed:", e)  # Print the error message
        speak("SMTP login failed. Please check your email credentials.")
        return

    speak("What should be the subject of this email?")
    subject = takecommand()
    speak("What content do you want to include in the email?")
    message = takecommand()
    username = receiver_email.split("@")[0]
    message_body = f"Subject: {subject}\n\nDear {username},\n\n{message}"
    s.sendmail("rishu930023@gmail.com", receiver_email, message_body)
    s.quit()
    speak("Email sent successfully!")


def get_weather(city):
    api_key = "32657d0b92c3c7d4d97e2cc3f8b226a3"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = json.loads(response.text)
    if data["cod"] != "404":
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        output = f"The weather in {city} is {weather}, with a temperature of {temperature} degrees Celsius, and it feels like {feels_like} degrees Celsius. The humidity is {humidity} percent."
        return output
    else:
        return f" Sorry, {city} not found. Please try again with a valid city name."


def weather_callback():
    speak("Sure! Please tell me the city for which you want to know the weather.")
    city = takecommand()
    weather_info = get_weather(city)
    speak(weather_info)


def open_control_panel():
    os.system("control")

def search_in_control_panel():
    speak("What would you like to search for in the control panel?")
    query = takecommand()
    os.system(f'start ms-settings:search?query={query}')


def remind_after_delay(reminder, mins):
    secs = mins * 60
    time.sleep(secs)
    speak(f"Reminder: {reminder}")
def set_reminder():
    speak("What do you want me to remind you about?")
    reminder = takecommand()
    speak("How many minutes from now should I remind you?")
    mins_text = input("Enter the number of minutes: ")
    try:
        mins = int(mins_text)
        threading.Thread(target=remind_after_delay, args=(reminder, mins)).start()
    except ValueError:
        speak("Sorry, I couldn't understand the number of minutes. Please enter a valid number.")


def power(mode):
    if mode == "restart":
        os.system("shutdown /r /t 1")
    elif mode == "sleep":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif mode == "shutdown":
        os.system("shutdown /s /t 1")
    else:
        speak("Invalid power mode. Please choose from 'restart', 'sleep', or 'shutdown'.")


def get_chat_response(query):
    try:
        genai.configure(api_key="AIzaSyDwEGs5SdrU8ZQ3HyNZq909sA_KOJv9zPk")

        # Create a generative model object
        model = genai.GenerativeModel("gemini-pro")

        # Generate content based on the query
        response = model.generate_content(query)

        print("Raw Response:", response.text)

        # Split the generated text into paragraphs based on newline characters
        paragraphs = response.text.split('\n')

        # Speak the first two paragraphs if available
        if len(paragraphs) >= 2:
            speak(paragraphs[0])
            speak(paragraphs[1])
        elif paragraphs:
            speak(paragraphs[0])
    except Exception as e:
        pass  # Silence any exceptions without printing or speaking anything


def button_callback():
    query = entry_1.get().lower()
    handle_command(query)

def speak_button_callback():
    speak("Listening for your command.")
    query = takecommand().lower()
    handle_command(query)

def handle_command(query):


        if "open notepad" in query:
            open_notepad()
            speak("Opening Notepad!")
            write_notepad()


        elif "open wikipedia" in query:
            search_wikipedia()


        elif "open control panel" in query:
            speak("Opening Control Panel.")
            open_control_panel()
            search_in_control_panel()


        elif "take a screenshot" in query:
            take_screenshot()
            speak("Screenshot taken successfully!")


        elif "play music" in query:
            music_dir = "C://Users//HARSH KUMAR SONI//Music//Soft Songs"
            songs = os.listdir(music_dir)
            # Select a random song from the list
            random_song = random.choice(songs)
            os.startfile(os.path.join(music_dir, random_song))


        elif "tell me a joke" in query:
            tell_joke()


        elif "tell me news" in query or "news" in query:
            news()


        elif "extract phrases" in query:
            scrape_quotes()


        elif "play youtube" in query or "play YouTube" in query:
            play_youtube()


        elif "search google for" in query:
            search_google()


        elif "send email" in query:
            send_email()


        elif "weather" in query:
            weather_callback()


        elif "set reminder" in query:
            set_reminder()


        elif "power" in query:
            speak("Which mode do you want to activate? 'restart', 'sleep', or 'shutdown'?")
            mode = takecommand().lower()
            power(mode)
            speak(f"{mode} mode activated!")


        elif "no thanks" in query or "thanks" in query or "quite it" in query:
            speak("thanks for using me, sir, have a good day :-) ")
            sys.exit()

        else:
            get_chat_response(query)



# GUI source starts here:
if __name__ == "__main__":
    wish()
    frame_1 = customtkinter.CTkFrame(master=app)
    frame_1.pack(pady=20, padx=60, fill="both", expand=True)

    label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text="Desktop Voice Assistant", font=("Helvetica", 16, "bold"))
    label_1.pack(pady=10, padx=10)

    entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Enter Command:", width=300, height=50)
    entry_1.pack(pady=10, padx=10)

    button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback, text="RUN", fg_color="blue")
    button_1.pack(pady=10, padx=10)

    label_2 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text="or", font=("Helvetica", 16))
    label_2.pack(pady=10, padx=10)

    speak_button = customtkinter.CTkButton(master=frame_1, command=speak_button_callback, text="SPEAK", fg_color="blue")
    speak_button.pack(pady=10, padx=10)

    progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
    progressbar_1.pack(pady=10, padx=10)

    text_1 = customtkinter.CTkTextbox(master=frame_1, width=200, height=70)
    text_1.pack(pady=10, padx=10)
    text_1.insert("0.0", "Status\n\n\n\n")

    quit_button = customtkinter.CTkButton(master=frame_1, command=app.quit, text="QUIT", fg_color="red")
    quit_button.pack(pady=10, padx=10)

    app.mainloop()


"""
keywords

1. open notepad
2. open wikipedia
3. open control panel
4. take a screenshot
5. play music
6. tell me a joke
7. "tell me news" or "news"
8. extract phrases
9. play youtube
10. search google for
11. send email
12. weather
13. set reminder
14. power
15. "no thanks" or "thanks" or "quite it"

"""