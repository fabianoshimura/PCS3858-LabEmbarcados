# PCS3858-LabEmbarcados
Projeto de Laboratório de Embarcados

Módulos / Subssistemas:

1. Módulo de reconhecimento das baquetas
Open CV + Python
OpencvPythonAirDrum/README.md

2. Módulo de sensores (acelerômetro e giroscópio)

3. Módulo de sensor do bumbo (botão)


COMANDOS para RPI4

sudo rpi-update

baixar PyCharm
sudo apt install default-jdk


sudo apt-get install cmake
sudo apt-get install python3-pip
sudo apt-get install python3-opencv
pip3 install opencv-python

pip3 install --upgrade imutils
pip3 install pyautogui


sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test
sudo apt-get install libatlas-base-dev

Erro 
Building wheel for opencv-python (pyproject.toml) ... 
Trava e não instala opencv-python
Baixar versão anterior!!!


AIR-DRUMS (https://github.com/kaustubh-sadekar/AIR_Drums.git)


ERROR
raspberry NotImplementedError: mixer module not available (ImportError: libSDL2_mixer-2.0.so.0: cannot open shared object file: No such file or directory)
Instalar:
sudo apt-get install libsdl2-mixer-2.0-0
