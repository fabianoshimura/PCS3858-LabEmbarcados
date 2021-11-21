# Fabiano M. Shimura
# RaspberryPi Projects
# Programa que emite um som ao pressionar um botão
# Colocar os terminais do botão no pino 17 e GND
# instalar a biblioteca gpiozero
# instalar RPi.GPIO
# instalar pygame

from gpiozero import Button
from signal import pause
from pygame import mixer


btn = Button(17)

mixer.init()
drum_snare = mixer.Sound('snare.wav')


def hello():
    print("snare!")
    drum_snare.play()


btn.when_pressed = hello

pause()
