"""Main loop: motion turns on NeoPixel bar for 60 seconds, retrigger extends timer."""

import time

import config
from motion_sensor import MotionSensor
from neopixel_bar import NeoPixelBar


def run():
    sensor = MotionSensor(config.MOTION_PIN, debounce_ms=config.DEBOUNCE_MS)
    leds = NeoPixelBar(
        config.NEOPIXEL_PIN,
        num_leds=config.NUM_LEDS,
        brightness=config.BRIGHTNESS,
    )

    leds.off()
    expires_at = None

    while True:
        now = time.ticks_ms()

        if sensor.triggered(now):
            leds.on(config.ON_COLOR)
            expires_at = time.ticks_add(now, config.HOLD_MS)

        if expires_at is not None and time.ticks_diff(now, expires_at) >= 0:
            leds.off()
            expires_at = None

        time.sleep_ms(config.POLL_MS)


if __name__ == "__main__":
    run()
