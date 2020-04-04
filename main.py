import kivy #для самого приложения

import speech_recognition as sr #для распознавания речи
import pyaudio #для использования микрофона

#######для интерфейса##############
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
#########################################

import pygame #для озвучивания напоминания
from gtts import gTTS #для озвучивания напоминания
pygame.init()

saveInput = ""

class Recognition():

    def recognition(self, args):
        self.transcript = ""

        """Keywords' understanding"""
        global saveInput
        keywords = self.box.text
        reminder = keywords.split()

        """Listening to the speech and recognizing"""
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        with mic as audio_file:
            r.adjust_for_ambient_noise(audio_file)
            audio = r.listen(audio_file)
            self.transcript = r.recognize_google(audio) #распознавание дефолтной АНГЛИЙСКОЙ речи
            #в следующем обновлении локализую для русского языка:)

        """Finding missing keywords and creating a reminder"""
        words_in_speech = self.transcript.split()

        for word in words_in_speech:
            for keyword in reminder:
                if word != keyword:
                    pass
                else:
                    reminder.remove(keyword)
                    
        output_reminder = "\n".join(reminder)
        self.textInfo.text += output_reminder

        """Text to speech for the reminder"""
        output_audio = "reminder.mp3" #создание аудиофайла для озвучивания напоминания
        tts = gTTS(text=output_reminder, lang="en")
        tts.save(output_audio)
        pygame.mixer.music.load(output_audio)
        pygame.mixer.music.play() #проигрывание напоминания

        while pygame.mixer.music.get_busy(): #это для непрерывного проигрывания до конца аудиофайла
            pygame.time.Clock().tick(10)

        
    def clear(self, args):
        """Cleaning all the data in the boxes"""

        self.box.text = ""
        self.textInfo.text = ""

class Speechka(App, Recognition):
    """Interface and buttons' functions"""
    
    def build(self):
        root = BoxLayout(orientation="horizontal", padding = 5)

        #######left
        left = BoxLayout(orientation = "vertical")

        self.box = TextInput(
            hint_text = 'Введите ключевые слова', readonly = False, font_size = 10,
            size_hint = [1, 1], background_color = [1, 1, 1, .7]
        )
        left.add_widget(self.box)

        buttonRun = Button(text='Начать', size_hint = [1, .20], on_press = self.recognition) #.*
        left.add_widget(buttonRun)

        ##########right
        right = BoxLayout(orientation = "vertical")
        self.textInfo = TextInput(readonly = True, hint_text = 'Пропущенные слова появятся здесь', background_color = [1,1,1,.7])
        right.add_widget(self.textInfo)
        #self.textInfo.text += 
        right.add_widget(Button(text = "Заново", size_hint = [1,.055], on_press = self.clear))

        ###########altogether
        root.add_widget(left)
        root.add_widget(right)

        return root


if __name__ == '__main__':
    Speechka().run()
   