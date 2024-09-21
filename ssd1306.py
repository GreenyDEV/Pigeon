from PIL import Image, ImageDraw
import smbus
import spidev
import time

# Constants (same as in the original)
SET_CONTRAST = 0x81
SET_ENTIRE_ON = 0xA4
SET_NORM_INV = 0xA6
SET_DISP = 0xAE
SET_MEM_ADDR = 0x20
SET_COL_ADDR = 0x21
SET_PAGE_ADDR = 0x22
SET_DISP_START_LINE = 0x40
SET_SEG_REMAP = 0xA0
SET_MUX_RATIO = 0xA8
SET_IREF_SELECT = 0xAD
SET_COM_OUT_DIR = 0xC0
SET_DISP_OFFSET = 0xD3
SET_COM_PIN_CFG = 0xDA
SET_DISP_CLK_DIV = 0xD5
SET_PRECHARGE = 0xD9
SET_VCOM_DESEL = 0xDB
SET_CHARGE_PUMP = 0x8D

class SSD1306:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = Image.new('1', (self.width, self.height))  # Create a new image (1-bit color)
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP,  # display off
            SET_MEM_ADDR, 0x00,  # horizontal
            SET_DISP_START_LINE,
            SET_SEG_REMAP | 0x01,
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08,
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x02 if self.width > 2 * self.height else 0x12,
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL, 0x30,
            SET_CONTRAST, 0xFF,
            SET_ENTIRE_ON, SET_NORM_INV,
            SET_IREF_SELECT, 0x30,
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,  # display on
        ):
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def fill(self, color):
        # Fill the entire buffer with the given color (0 or 1)
        draw = ImageDraw.Draw(self.buffer)
        draw.rectangle((0, 0, self.width, self.height), outline=color, fill=color)

    def show(self):
        # This is where you'd send the buffer content to the display
        pass

    def write_cmd(self, cmd):
        # This function will send commands to the OLED (to be implemented for I2C or SPI)
        pass

class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c_bus, addr=0x3C, external_vcc=False):
        self.i2c_bus = i2c_bus
        self.addr = addr
        self.temp = [0, 0]
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.i2c_bus.write_byte_data(self.addr, 0x00, cmd)

    def write_data(self, buf):
        for byte in buf:
            self.i2c_bus.write_byte_data(self.addr, 0x40, byte)

class SSD1306_SPI(SSD1306):
    def __init__(self, width, height, spi_bus, dc, res, cs, external_vcc=False):
        self.spi_bus = spi_bus
        self.dc = dc
        self.res = res
        self.cs = cs
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.spi_bus.xfer2([cmd])

    def write_data(self, buf):
        self.spi_bus.xfer2(list(buf))
