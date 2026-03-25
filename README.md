# ESP32-S2 + RCWL-0516 + 8x NeoPixel (MicroPython)

This project turns on an 8-LED WS2812B/NeoPixel bar for 60 seconds when motion is detected.
If motion is detected again during that time, the 60-second timer is reset.

## Files

- `main.py` - Main loop and timer logic.
- `config.py` - Pins and behavior settings.
- `motion_sensor.py` - Debounced RCWL-0516 trigger detection.
- `neopixel_bar.py` - NeoPixel bar control.
- `boot.py` - Minimal boot script.

## Physical wiring (by board pin labels)

This uses the pin labels printed on most ESP32-S2 dev boards (VIN, GND, IO9, IO18).
If your board uses a different naming style (for example D9/D18), use the equivalent pin.

| Module | Pin | Connect To |
|---|---|---|
| RCWL-0516 | VCC | ESP32-S2 VIN / 5V pin |
| RCWL-0516 | GND | ESP32-S2 GND pin |
| RCWL-0516 | OUT | ESP32-S2 IO9 pin |
| NeoPixel Bar (8x WS2812B) | +5V | External regulated 5V supply (+) |
| NeoPixel Bar (8x WS2812B) | GND | External 5V supply (-) and ESP32-S2 GND |
| NeoPixel Bar (8x WS2812B) | DIN | ESP32-S2 IO18 pin |

### Quick physical lookup on board

- VIN / 5V: header pin labeled VIN (or 5V), usually close to USB connector area.
- GND: any header pin labeled GND (use one near VIN if available).
- IO9: header pin labeled IO9 (or GPIO9 / D9 depending on board silk).
- IO18: header pin labeled IO18 (or GPIO18 / D18 depending on board silk).

Do not connect NeoPixel +5V to 3V3.

Important:
- All grounds must be common (ESP32-S2 GND, RCWL GND, LED power GND).
- Use an external 5V supply for the NeoPixel bar if possible.
- Recommended: 330 ohm resistor in series on DIN line.
- Recommended: 470 to 1000 uF capacitor across NeoPixel +5V and GND near the strip.
- ESP32-S2 data is 3.3V. Many WS2812B bars work with this, but a 74AHCT125/74HCT14 level shifter is recommended for robust operation.

## ASCII connection diagram

```text
               +------------------- ESP32-S2 -------------------+
               |                                                 |
               |  IO9    <---------------- RCWL-0516 OUT         |
               |  IO18   ----------------> NeoPixel DIN          |
               |  GND    -----------------+-------------------+  |
               |                          |                   |  |
               |  VIN/5V <-------------- RCWL-0516 VCC       |  |
               +--------------------------+-------------------|--+
                                              common ground   |
                                                              |
                   +--------------- RCWL-0516 ---------------+|
                   | VCC ------------------------------ 5V/VIN||
                   | GND ------------------------------ GND   ||
                   | OUT ------------------------------ IO9   ||
                   +------------------------------------------+|
                                                               |
                +------------- External 5V Supply -------------+
                | +5V ----------------------------------+      |
                | GND ---------------------------+-------|------+
                +--------------------------------|-------+
                                                 |       |
                                 +---------------v-------v--------------+
                                 |      NeoPixel Bar (8x WS2812B)       |
                                 | +5V <----------------------- +5V      |
                                 | GND <----------------------- GND      |
                                 | DIN <---- IO18 (via 330 ohm)         |
                                 +---------------------------------------+
```

## Flash MicroPython firmware (example)

Use the latest ESP32-S2 MicroPython firmware (`.bin`) from micropython.org.

```bash
# Erase flash (replace PORT)
esptool.py --chip esp32s2 --port /dev/tty.usbmodemXXXX erase_flash

# Write firmware at 0x1000
esptool.py --chip esp32s2 --port /dev/tty.usbmodemXXXX --baud 460800 write_flash -z 0x1000 ESP32S2_FIRMWARE.bin
```

## Upload files (example with mpremote)

```bash
mpremote connect /dev/tty.usbmodemXXXX fs cp boot.py :
mpremote connect /dev/tty.usbmodemXXXX fs cp config.py :
mpremote connect /dev/tty.usbmodemXXXX fs cp motion_sensor.py :
mpremote connect /dev/tty.usbmodemXXXX fs cp neopixel_bar.py :
mpremote connect /dev/tty.usbmodemXXXX fs cp main.py :
```

Then reset the board. `main.py` should auto-run.

## Quick behavior test

1. Power on board and modules, keep area still: LEDs should stay off.
2. Move near sensor: LEDs turn on.
3. Wait 60 seconds with no further motion: LEDs turn off.
4. Trigger motion again before timeout: on-time extends by another 60 seconds from the latest motion.

## Tuning

Edit `config.py`:
- `MOTION_PIN`, `NEOPIXEL_PIN` if your board wiring is different.
- `HOLD_SECONDS` to change on-time.
- `BRIGHTNESS` to reduce current draw.
- `DEBOUNCE_MS` if you notice false triggering.
