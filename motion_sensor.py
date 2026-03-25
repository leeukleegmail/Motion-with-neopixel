"""RCWL-0516 motion sensor helper with simple debounce and edge detection."""

import time
from machine import Pin


class MotionSensor:
    """Detect stable low->high transitions from a digital motion output."""

    def __init__(self, pin_number, debounce_ms=80):
        self.pin = Pin(pin_number, Pin.IN)
        self.debounce_ms = debounce_ms

        initial = self.pin.value()
        self._last_raw = initial
        self._stable_state = initial
        self._last_change_ms = time.ticks_ms()

    def triggered(self, now_ms=None):
        """Return True once when a debounced rising edge is detected."""
        if now_ms is None:
            now_ms = time.ticks_ms()

        raw = self.pin.value()

        if raw != self._last_raw:
            self._last_raw = raw
            self._last_change_ms = now_ms

        if (
            raw != self._stable_state
            and time.ticks_diff(now_ms, self._last_change_ms) >= self.debounce_ms
        ):
            self._stable_state = raw
            return self._stable_state == 1

        return False
