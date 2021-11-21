# Fabiano M. Shimura
# Primeiro programa para testar o GPIO da placa RaspberryPi4
# Colocar os terminais do botão no pino 17 e GND
# instalar a biblioteca gpiozero
# instalar RPi.GPIO

from gpiozero import Button
from signal import pause

btn = Button(17)


def hello():
    print("hello")


btn.when_pressed = hello

pause()
