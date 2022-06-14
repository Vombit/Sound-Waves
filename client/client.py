from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
Window.size = (400, 600)

from flask import Flask, request
from threading import Thread

import pyaudio
from urllib.request import urlopen

class ScatterTextWidget(Widget):

    def start_flask(self, *args):
        data_ip = self.ids['ip_add']
        data_port = self.ids['port_add']

        FORMAT = pyaudio.paInt16
        CHUNK = 1024
        RATE = 48000
        bitsPerSample = 16
        CHANNELS = 1
        # url = "http://192.168.1.103:80/radio"
        url = self.ids['full_address'].text

        self.audio = pyaudio.PyAudio()
        stream = self.audio.open(format = pyaudio.paInt16,channels = CHANNELS,rate = RATE,output = True)
        ulrss = urlopen(url)
        self.data = ulrss.read(CHUNK)
        try:
            while self.data:
                stream.write(self.data)
                self.data = ulrss.read(CHUNK)
        except Exception:
            print('Error!')




    def connections(self, *args):
        Thread(target=self.start_flask).start()
        # color = [1, 0, 0, 1]

        # label = self.ids['test_label']
        # label.color = color
    


class MyApp(App):
    def build(self):
        return ScatterTextWidget()


if __name__ == '__main__':
    MyApp().run()