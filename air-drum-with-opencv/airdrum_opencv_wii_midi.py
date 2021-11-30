import numpy as np
import time
import cv2
from pygame import mixer
import cwiid

print 'Please press buttons 1 + 2 on your Wiimote now ...'
time.sleep(3)

# This code attempts to connect to your Wiimote and if it fails the program quits
try:
  wii=cwiid.Wiimote()
except RuntimeError:
  print "Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!"
  quit()

print 'Wiimote connection established!\n'
print 'Go ahead and press some buttons\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'

time.sleep(2)

wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC


def state_machine(sumation, sound, trigger):
    # Check if blue color object present in the ROI
    yes = (sumation) > Hatt_thickness[0] * Hatt_thickness[1] * 0.8

    # If present play the respective instrument.
    if yes and sound == 1 and trigger > 10000:
        drum_clap.play()
        print('CLAP!')
        print(trigger)
        #time.sleep(0.3)


    elif yes and sound == 2 and trigger > 10000:
        drum_snare.play()
        print('SNARE!')
        print(trigger)
        #time.sleep(0.3)




def ROI_analysis(frame, sound):
    # converting the image into HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # generating mask for
    mask = cv2.inRange(hsv, blueLower, blueUpper)

    # Calculating the nuber of white pixels depecting the blue color pixels in the ROI
    sumation = np.sum(mask)

    # Function that decides to play the instrument or not.
    state_machine(sumation, sound, trigger)

    return mask


Verbsoe = False

# importing the audio files
mixer.init()
drum_clap = mixer.Sound('batterrm.wav')
drum_snare = mixer.Sound('button-2.ogg')

# Frame accusition from webcam/ usbcamera
camera = cv2.VideoCapture(0)
ret, frame = camera.read()
H, W = frame.shape[:2]

kernel = np.ones((7, 7), np.uint8)


# HSV range for detecting blue color
# blueLower = (80,150,10)
# blueUpper = (120,255,255)

# HSV para vermelho
_, frame = camera.read()
frame = cv2.flip(frame, 1)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
blueLower = (164,19,36)
blueUpper = (256, 256, 256)
blue_mask = cv2.inRange(hsv, blueLower, blueUpper)



# reading the image of hatt and snare for augmentation.
Hatt = cv2.resize(cv2.imread('./Images/drum_cy.png'), (200, 100), interpolation=cv2.INTER_AREA)
Snare = cv2.resize(cv2.imread('./Images/drum_sn.png'), (200, 100), interpolation=cv2.INTER_AREA)

# Setting the ROI area for blue color detection
Hatt_center = [np.shape(frame)[1] * 2 // 8, np.shape(frame)[0] * 6 // 8]
Snare_center = [np.shape(frame)[1] * 6 // 8, np.shape(frame)[0] * 6 // 8]
Hatt_thickness = [200, 100]
Hatt_top = [Hatt_center[0] - Hatt_thickness[0] // 2, Hatt_center[1] - Hatt_thickness[1] // 2]
Hatt_btm = [Hatt_center[0] + Hatt_thickness[0] // 2, Hatt_center[1] + Hatt_thickness[1] // 2]

Snare_thickness = [200, 100]
Snare_top = [Snare_center[0] - Snare_thickness[0] // 2, Snare_center[1] - Snare_thickness[1] // 2]
Snare_btm = [Snare_center[0] + Snare_thickness[0] // 2, Snare_center[1] + Snare_thickness[1] // 2]

#time.sleep(0.05)

while True:

    buttons = wii.state['buttons']

    # Detects whether + and - are held down and if they are it quits the program
    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        print
        '\nClosing connection ...'
        # NOTE: This is how you RUMBLE the Wiimote
        wii.rumble = 1
        time.sleep(1)
        wii.rumble = 0
        exit(wii)

    (x, y, z) = wii.state['acc']
    acc_value_ant = x * y * z
    time.sleep(0.5)
    (x, y, z) = wii.state['acc']
    print(wii.state['acc'])
    acc_value_pos = x * y * z
    trigger = ((acc_value_pos - acc_value_ant) * (acc_value_pos - acc_value_ant)) / 10000000

    #if (trigger > 50):
        #print(trigger)
        # wii.rumble = 1
        # time.sleep(0.1)
        # wii.rumble = 0

    # grab the current frame
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    if not (ret):
        break

    # Selecting ROI corresponding to snare
    snare_ROI = np.copy(frame[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]])
    mask = ROI_analysis(snare_ROI, 1)

    # Selecting ROI corresponding to Hatt
    hatt_ROI = np.copy(frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[0]])
    mask = ROI_analysis(hatt_ROI, 2)

    cv2.putText(frame, 'Projeto: Air Drums GRUPO 5', (10, 30), 2, 1, (20, 20, 20), 2)

    # Display the ROI to view the blue colour being detected
    if Verbsoe:
        # Displaying the ROI in the Image
        frame[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]] = cv2.bitwise_and(
            frame[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]],
            frame[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]],
            mask=mask[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]])
        frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[0]] = cv2.bitwise_and(
            frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[0]],
            frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[0]],
            mask=mask[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[0]])

    # Augmenting the instruments in the output frame.
    else:
        # Augmenting the image of the instruments on the frame.
        frame[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]] = cv2.addWeighted(Snare, 1,
                                                                                      frame[Snare_top[1]:Snare_btm[1],
                                                                                      Snare_top[0]:Snare_btm[0]], 1, 0)
        frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[0]] = cv2.addWeighted(Hatt, 1,
                                                                                  frame[Hatt_top[1]:Hatt_btm[1],
                                                                                  Hatt_top[0]:Hatt_btm[0]], 1, 0)

    cv2.imshow('Output', frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break



# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
