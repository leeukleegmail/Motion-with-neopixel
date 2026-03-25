"""Project configuration for ESP32-S2 + RCWL-0516 + NeoPixel bar."""

# Pin mapping (change these to match your exact ESP32-S2 board pinout)
MOTION_PIN = 9
NEOPIXEL_PIN = 18

# LED settings
NUM_LEDS = 8
BRIGHTNESS = 0.25  # 0.0..1.0
ON_COLOR = (255, 180, 80)  # warm white/orange

# Motion hold behavior
HOLD_SECONDS = 60
HOLD_MS = HOLD_SECONDS * 1000

# Loop and debounce timings
POLL_MS = 50
DEBOUNCE_MS = 80
