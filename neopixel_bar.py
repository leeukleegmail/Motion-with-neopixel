"""NeoPixel bar helper for an addressable LED strip/bar."""

from machine import Pin
import neopixel


class NeoPixelBar:
    def __init__(self, pin_number, num_leds=8, brightness=0.25):
        self.num_leds = num_leds
        self.brightness = max(0.0, min(1.0, brightness))
        self.np = neopixel.NeoPixel(Pin(pin_number, Pin.OUT), num_leds)

    def _scale(self, color):
        r, g, b = color
        factor = self.brightness
        return (
            int(r * factor),
            int(g * factor),
            int(b * factor),
        )

    def set_all(self, color):
        scaled = self._scale(color)
        for i in range(self.num_leds):
            self.np[i] = scaled

    def show(self):
        self.np.write()

    def on(self, color):
        self.set_all(color)
        self.show()

    def off(self):
        self.set_all((0, 0, 0))
        self.show()
