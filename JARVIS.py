import pyttsx3
import requests
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import smtplib
from covid import Covid
import random
import cv2
import os
import numpy as np
import face_recognition as fr

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


video_capture = cv2.VideoCapture(0)

edith_img = fr.load_image_file("edith.jpg")
edith_face_encoding = fr.face_encodings(edith_img)[0]

known_face_encodings = [edith_face_encoding]
known_face_names = ["Ramana"]

while True:
    ret, frame = video_capture.read()

    rgb_frame = frame[:, :, ::-1]

    face_locations = fr.face_locations(rgb_frame)
    face_encodings = fr.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        matches = fr.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        face_distances = fr.face_distance(known_face_encodings, face_encoding)

        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 260), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Webxam_facerecognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

if name != "Unknown":

    print("FACE FOUNDED!")
    speak("FACE FOUNDED")
    print("$ ACCESS GRANTED $")
    speak("ACCESS GRANTED")


    def greet():
        hrs = int(datetime.datetime.now().hour)
        if 0 <= hrs < 12:
            speak("GOOD MORNING SIR")

        elif 12 <= hrs < 18:
            speak("GOOD AFTERNOON SIR")

        else:
            speak("GOOD EVENING SIR")

        speak("I AM JARVIS SIR,TELL ME HOW CAN I HELP YOU ?")

        Time = datetime.datetime.now().strftime("%d %b %y | %I:%M:%S %p")
        print("----------------------------")
        print(Time)
        print("----------------------------")
        speak(f"NOW THE TIME {Time}")


    def takeCommand():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("LISTENING..")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"THE QUERY THAT USER SAID	; {query}\n")

        except Exception as e:
            print(e)
            print("SAY THAT AGAIN PLEASE")
            return "None"
        return query


    if __name__ == "__main__":
        greet()
        while True:
            query = takeCommand().lower()

            if 'according to wikipedia' in query:
                speak("SEARCHING WIKIPEDIA...")
                query = query.replace('according to wikipedia', '')
                results = wikipedia.summary(query, sentences=4)
                speak("According to wikipedia")
                print(results)
                speak(results)

            elif 'amazon' in query:
                speak("OPENING AMAZON.....")
                webbrowser.open("amazon.com")

            elif 'facebook' in query:
                speak("OPENING FACEBOOK.....")
                webbrowser.open("facebook.com")

            elif 'youtube' in query:
                speak("OPENING YOUTUBE.....")
                webbrowser.open("youtube.com")

            elif 'instagram' in query:
                speak("OPENING INSTAGRAM.....")
                webbrowser.open("instagram.com")

            elif 'weather' in query:
                speak("IN PROGRESS SIR.....")
                speak("ENTER THE CITY NAME")
                user_api = '8f646ce4984e2e1040610eb6bbf9d592'
                location = input("ENTER THE CITY NAME : ")

                complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + user_api

                api_link = requests.get(complete_api_link)
                api_data = api_link.json()

                if api_data['cod'] == '404':
                    print("INVALID CITY: {}, PLEASE CHECK YOUR CITY NAME".format(location))
                else:
                    temp_city = ((api_data['main']['temp']) - 273.15)
                    weather_desc = api_data['weather'][0]['description']
                    hmdt = api_data['main']['humidity']
                    wind_spd = api_data['wind']['speed']
                    date_time = datetime.datetime.now().strftime("%d %b %y | %I:%M:%S %p")

                    print("------------------------------------------------------------")
                    print("WEATHER STATUS FOR - {} || {}".format(location.upper(), date_time))
                    print("------------------------------------------------------------")

                    print("CURRENT TEMPERATURE IS: {:.2f} deg C".format(temp_city))
                    speak("CURRENT TEMPERATURE IS: {:.2f} deg C".format(temp_city))
                    print("CURRENT WEATHER DESCRIPTION  :", weather_desc)
                    speak("CURRENT WEATHER DESCRIPTION  :" + weather_desc)
                    print("CURRENT HUMIDITY      :", hmdt, '%')
                    print("CURRENT WIND SPEED    :", wind_spd, 'kmph')

            elif 'covid' in query:
                speak("COVID CASES IN INDIA...")
                covid = Covid()
                cases = covid.get_status_by_country_name("India")
                for x in cases:
                    print(x, ":", cases[x])

            elif 'according to google' in query:
                speak('SEARCHING IN GOOGLE...')
                query = query.replace('according to google', '')
                webbrowser.open("http://google.com/#q= " + query, new=2)

            elif 'play music' in query:
                music_dir = "C:/Users/asimov/Music"
                songs = os.listdir(music_dir)
                n = len(songs)
                index = random.randint(1, n)
                os.startfile(os.path.join(music_dir, songs[1]))

            elif 'play video' in query:
                Video_dir = "C:/Users/asimov/Videos/Videos"
                Videos = os.listdir(Video_dir)
                n = len(Videos)
                index = random.randint(1, n)
                os.startfile(os.path.join(Video_dir, Videos[index]))

            elif 'open python' in query:
                pycharm = "C:/Program Files/JetBrains/PyCharm Community Edition 2020.2/bin/pycharm64.exe"
                os.startfile(pycharm)

            elif 'open java' in query:
                intellij = "C:/Program Files/JetBrains/IntelliJ IDEA Community Edition 2020.2/bin/idea64.exe"
                os.startfile(intellij)

            elif 'open code' in query:
                code = "C:/Users/asimov/AppData/Local/Programs/Microsoft VS Code/Code.exe"
                os.startfile(code)

            elif 'open antivirus' in query:
                McAfee = "C:/Program Files/Common Files/McAfee/Platform/McUICnt.exe"
                os.startfile(McAfee)

            elif 'open fighter' in query:
                mf = "C:/Program Files (x86)/IObit/IObit Malware Fighter/IMF.exe"
                os.startfile(mf)

            elif 'time' in query:
                strTime = datetime.datetime.now().strftime("%d %b %y | %I:%M:%S %p")
                print("----------------------------")
                print(strTime)
                print("----------------------------")
                speak(f"SIR, NOW THE TIME {strTime}")

            elif 'name' in query:
                print("MY NAME IS Just A Rather Very Intelligent System, AND YOU CAN CALL ME AS J.A.R.V.I.S, JARVIS")
                speak("MY NAME IS Just A Rather Very Intelligent System, AND YOU CAN CALL ME AS J.A.R.V.I.S, JARVIS")

            elif 'hey jarvis' in query:
                speak("YES SIR, I AM IN ONLINE, TELL ME HOW CAN I HELP YOU SIR")

            elif 'thank you' in query:
                speak("AS YOUR WISH,THANK YOU SIR")
                break
else:
    print("FACE NOT FOUNDED!")
    speak("FACE NOT FOUNDED")
    print("!!! ACCESS DENIED !!!")
    speak("ACCESS DENIED")
