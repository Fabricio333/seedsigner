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
    # It has a d-pad plus A/B/X/Y, START/SELECT and TL/TR instead of a joystick
    # and 3 side keys, so:
    #   KEY_PRESS <- A        KEY1 (top) <- X    KEY2 (mid) <- Y    KEY3 (bottom) <- B
    BUTTON_PINS = dict(
        KEY_UP=36,      # BCM16
        KEY_DOWN=29,    # BCM5
        KEY_LEFT=31,    # BCM6
        KEY_RIGHT=33,   # BCM13
        KEY_PRESS=40,   # BCM21 "A"
        KEY1=10,        # BCM15 "X"
        KEY2=32,        # BCM12 "Y"
        KEY3=38,        # BCM20 "B"
    )

    # Extra physical buttons that behave as an existing logical key
    BUTTON_ALIASES = dict(
        KEY_PRESS=[35, 5],  # BCM19 "START", BCM3 "KEY PRESS"
    )

    LCD_DC_PIN = 15     # BCM22
    LCD_RST_PIN = 13    # BCM27
    LCD_BL_PIN = None   # backlight is hardwired on

    # MADCTL: the vendor's fbtft overlay drives this panel at rotate=0
    LCD_MADCTL = 0x00

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
