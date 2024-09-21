import smbus
import time
from PIL import Image, ImageDraw
from ssd1306 import SSD1306_I2C  # Use the SSD1306_I2C class from earlier

# Constants for display size
WIDTH = 128
HEIGHT = 64

# Initialize I2C (bus 1 is typically used on Raspberry Pi)
i2c_bus = smbus.SMBus(1)

# Initialize the display (make sure the address matches your display, typically 0x3C)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c_bus)

def read_cpu_temp():
    # Reads the CPU temperature on Raspberry Pi
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
    temperature = float(temp) / 1000  # Convert from millidegrees to degrees Celsius
    formatted_temperature = "{:.1f}".format(temperature)
    string_temperature = "CPU Temp: " + formatted_temperature + " C"
    print(string_temperature)
    return string_temperature

while True:
    # Clear the display buffer
    display.fill(0)
    
    # Write example text and temperature
    display.text('Example 1:', 0, 0)
    temperature = read_cpu_temp()
    display.text(temperature, 0, 14)
    
    # Display the result on the screen
    display.show()
    
    # Sleep for a while
    time.sleep(2)
