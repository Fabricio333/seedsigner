"""
Physical board wiring (buttons + LCD control pins) for the supported display hats.

The active profile is read from the `SEEDSIGNER_HARDWARE` env var, which
SeedSigner OS sets at boot from /etc/seedsigner-hardware (see the OS's
`build.sh --hardware=...`). Unset means the original Waveshare 1.3" hat.

All pin numbers are physical header pins (GPIO.BOARD numbering).
"""
import os

HARDWARE__WAVESHARE_13 = "waveshare_1.3"
HARDWARE__SPOTPEAR_GAME_154 = "spotpear_game_1.54"

ALL_HARDWARE = [HARDWARE__WAVESHARE_13, HARDWARE__SPOTPEAR_GAME_154]

HARDWARE = os.environ.get("SEEDSIGNER_HARDWARE", "").strip() or HARDWARE__WAVESHARE_13
if HARDWARE not in ALL_HARDWARE:
    raise ValueError(f"Unsupported SEEDSIGNER_HARDWARE: {HARDWARE}")


if HARDWARE == HARDWARE__SPOTPEAR_GAME_154:
    # Spotpear/Zopsc "1.54inch LCD Mini Game Console" hat (ST7789V 240x240).
    # https://spotpear.com/wiki/Raspberry-Pi-Game-1.54inch-LCD-touchscreen-display-ST7789.html
    # Held landscape: 5-way joystick on the left; on the right, the column of
    # buttons next to the screen (Y, X, SELECT) stands in for KEY1/2/3. The
    # outer B/A, START and the L/R shoulders are left unused.
    BUTTON_PINS = dict(
        KEY_UP=36,      # BCM16
        KEY_DOWN=29,    # BCM5
        KEY_LEFT=31,    # BCM6
        KEY_RIGHT=33,   # BCM13
        KEY_PRESS=5,    # BCM3  joystick press
        KEY1=32,        # BCM12 "Y"      (top)
        KEY2=10,        # BCM15 "X"      (middle)
        KEY3=37,        # BCM26 "SELECT" (bottom)
    )

    BUTTON_ALIASES = {}

    LCD_DC_PIN = 15     # BCM22
    LCD_RST_PIN = 13    # BCM27
    LCD_BL_PIN = None   # backlight is hardwired on

    # MADCTL: panel's native scan (0x00) is 90° CCW when held landscape; 0x70
    # rotates it 90° CW (same as the Waveshare hat, and needs no GRAM offset)
    LCD_MADCTL = 0x70

else:
    # Waveshare 1.3inch LCD HAT (the original SeedSigner hardware)
    from RPi import GPIO
    if GPIO.RPI_INFO['P1_REVISION'] == 3: #This indicates that we have revision 3 GPIO
        BUTTON_PINS = dict(
            KEY_UP=31,
            KEY_DOWN=35,
            KEY_LEFT=29,
            KEY_RIGHT=37,
            KEY_PRESS=33,
            KEY1=40,
            KEY2=38,
            KEY3=36,
        )
    else:
        # Assuming 26 Pin GPIO (Raspberry Pi 1)
        BUTTON_PINS = dict(
            KEY_UP=5,
            KEY_DOWN=11,
            KEY_LEFT=3,
            KEY_RIGHT=15,
            KEY_PRESS=7,
            KEY1=16,
            KEY2=12,
            KEY3=8,
        )

    BUTTON_ALIASES = {}

    LCD_DC_PIN = 22
    LCD_RST_PIN = 13
    LCD_BL_PIN = 18

    LCD_MADCTL = 0x70
