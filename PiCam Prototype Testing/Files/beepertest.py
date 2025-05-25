from gpiozero import Buzzer
from time import sleep

# Initialize the Buzzer on GPIO pin 17
buzzer = Buzzer(17)

# Beep with the active buzzer
# First set of beeps
buzzer.on()
sleep(2)
buzzer.off()
sleep(0.2)
for _ in range(2):
    buzzer.on()
    sleep(0.05)
    buzzer.off()
    sleep(0.09)
for _ in range(2):
    buzzer.on()
    sleep(0.05)
    buzzer.off()
    sleep(0.09)
for _ in range(2):
    buzzer.on()
    sleep(0.05)
    buzzer.off()
    sleep(0.09)
buzzer.on()
sleep(2)
buzzer.off()
sleep(0.2)
# You can optionally close the buzzer object when you're done
buzzer.close()
