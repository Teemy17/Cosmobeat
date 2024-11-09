from gpiozero import Button, LED
from signal import pause

led = LED(20)

def when_pressed():
    print("Button was pressed!")
    led.on()

def when_released():
    print("Button was released!")
    led.off()

button = Button(26)

button.when_pressed = when_pressed
button.when_released = when_released

pause()  # Wait indefinitely for signals
