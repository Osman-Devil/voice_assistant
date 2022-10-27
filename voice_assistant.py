# Голосовой ассистент
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

# настройки
opts = {
    "alias": ('алиса','слушай'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "alarm": ('включи будильник', 'поставь будильник', 'будильник')
    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC



def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        # воспроизвести радио
        os.system("G:\\music1.mp3")
    elif cmd == 'alarm':
        def validate_time(alarm_time):
            if len(alarm_time) != 8:
                return "Невереный формат, попробуйте еще раз! "
            else:
                if int(alarm_time[0:2]) > 23:
                    return "невереный формат часов, попробуйте еще раз"
                elif int(alarm_time[3:5]) > 59:
                    return "невереный формат минут, попробуйте еще раз"
                else:
                    return "Отлично!"

        while True:
            alarm_time = input("Время \'HH:MM:SS\' \nВремя будильника: ")
            validate = validate_time(alarm_time)
            if validate != "Отлично!":
                print(validate)
            else:

                print(f"Будильник установлен на время: {alarm_time} ...")
                break

        alarm_hour = int(alarm_time[0:2])
        alarm_min = int(alarm_time[3:5])
        alarm_sec = int(alarm_time[6:8])

        while True:
            now = datetime.datetime.now()

            current_hour = now.hour
            current_min = now.minute
            current_sec = now.second

            if alarm_hour == current_hour:
                if alarm_min == current_min:
                    if alarm_sec == current_sec:
                        os.system("G:\\music1.mp3")
                        speak("Будильник сработал")
                        continue

    else:
        print('Команда не распознана, повторите!')

# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()
stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop