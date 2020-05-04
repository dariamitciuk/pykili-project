import kivy #для самого приложения

import speech_recognition as sr #для распознавания речи
import pyaudio #для использования микрофона

import pymorphy2 #для понимания разных форм слова
morph = pymorphy2.MorphAnalyzer()

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

    def recognition_manual(self, args):
        
        self.transcript = ""

        """Keywords' understanding"""
        global saveInput
        keywords = self.box.text
        reminder = keywords.split()

        """Listening to the speech and recognizing"""
        r = sr.Recognizer()
        mic = sr.Microphone()

        with mic as audio_file:
            try:
                r.adjust_for_ambient_noise(audio_file)
                audio = r.listen(audio_file)
                self.transcript = r.recognize_google(audio, language="ru-RU") #распознавание РУССКОЙ речи
            except:
                self.textInfo.text += "Не удалось распознать речь, попробуйте ещё раз" #на случай ошибки распознавания

        """Finding missing keywords and creating a reminder"""
        words_in_speech = self.transcript.split()

        for word in words_in_speech:
            word = morph.parse(word)[0].normal_form
            for keyword in reminder:
                keyword_lemma = morph.parse(keyword)[0].normal_form
                if word != keyword_lemma:
                    pass
                else:
                    reminder.remove(keyword)

        self.box.text = ""
        self.box.text += " ".join(reminder) #стирание уже озвученных ключевых слов из списка слева

        output_reminder = ""
        if len(reminder) > 4: #ограничение длины напоминания
            output_reminder = "\n".join(reminder[:4])
        else:
            output_reminder = "\n".join(reminder)


        """Text to speech for the reminder"""
        output_audio = "reminder.mp3" #создание аудиофайла для озвучивания напоминания
        tts = gTTS(text=output_reminder, lang="ru")
        tts.save(output_audio)
        pygame.mixer.music.load(output_audio)
        pygame.mixer.music.play() #проигрывание напоминания

        self.textInfo.text = "" #для создания нового перечня напоминаний на каждой итерации
        self.textInfo.text += output_reminder + "\n"

        while pygame.mixer.music.get_busy(): #это для непрерывного проигрывания до конца аудиофайла
            pygame.time.Clock().tick(10)

    def recognition_auto(self, args):
        
        self.transcript = ""

        """Keywords' understanding"""
        global saveInput
        keywords = self.box.text
        reminder = keywords.split()

        """Listening to the speech and recognizing"""
        r = sr.Recognizer()
        mic = sr.Microphone()

        while True: #повторение без нажатия на кнопку
            with mic as audio_file:
                try:
                    r.adjust_for_ambient_noise(audio_file)
                    audio = r.listen(audio_file)
                    self.transcript = r.recognize_google(audio, language="ru-RU") #распознавание РУССКОЙ речи
                except:
                    self.textInfo.text += "Не удалось распознать речь, попробуйте ещё раз" #на случай ошибки распознавания

            """Finding missing keywords and creating a reminder"""
            words_in_speech = self.transcript.split()

            for word in words_in_speech:
                word = morph.parse(word)[0].normal_form
                for keyword in reminder:
                    keyword_lemma = morph.parse(keyword)[0].normal_form
                    if word != keyword_lemma:
                        pass
                    else:
                        reminder.remove(keyword)

            self.box.text = ""
            self.box.text += " ".join(reminder) #стирание уже озвученных ключевых слов из списка слева

            output_reminder = ""
            if len(reminder) > 4: #ограничение длины напоминания
                output_reminder = "\n".join(reminder[:4])
            else:
                output_reminder = "\n".join(reminder)


            """Text to speech for the reminder"""
            output_audio = "reminder.mp3" #создание аудиофайла для озвучивания напоминания
            tts = gTTS(text=output_reminder, lang="ru")
            tts.save(output_audio)
            pygame.mixer.music.load(output_audio)
            pygame.mixer.music.play() #проигрывание напоминания

            while pygame.mixer.music.get_busy(): #это для непрерывного проигрывания до конца аудиофайла
                pygame.time.Clock().tick(10)
    

class Speechka(App, Recognition):
    """Interface and buttons' functions"""
    
    def build(self):
        root = BoxLayout(orientation="horizontal", padding = 5)

        #######left
        left = BoxLayout(orientation = "vertical")

        self.box = TextInput(
            hint_text = 'Введите ключевые слова', readonly = False, font_size = 14,
            size_hint = [1, 1], background_color = [1, 1, 1, .7]
        )
        left.add_widget(self.box)

        buttonRun = Button(text = "Автоматический режим", size_hint = [1, .20], on_press = self.recognition_auto)
        left.add_widget(buttonRun)

        ##########right
        right = BoxLayout(orientation = "vertical")
        self.textInfo = TextInput(readonly = True, hint_text = 'Пропущенные слова появятся здесь', background_color = [1,1,1,.7])
        right.add_widget(self.textInfo)
        #self.textInfo.text += 
        right.add_widget(Button(text='Ручной режим', size_hint = [1, .20], on_press = self.recognition_manual))

        ###########altogether
        root.add_widget(left)
        root.add_widget(right)

        return root


if __name__ == '__main__':
    Speechka().run()