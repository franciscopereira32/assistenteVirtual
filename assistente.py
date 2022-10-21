import speech_recognition as sr 

#criar o reconhecer
r = sr.Recognizer()

#Ligar o mic
with sr.Microphone() as source:
    while True:
        audio = r.listen(source) #define mic como fonte de audio

        print(r.recognize_google(audio, language='pt'))