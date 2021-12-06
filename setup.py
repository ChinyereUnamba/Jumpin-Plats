import os
import sys
from cx_Freeze import setup, Executable, sys

build_exe_options = {
    "packages": ['os', 'pygame'],
    "include_files": [
        'cloud.png',
        'Happy Tune.wav',
        'Jump.wav',
        'Pickup_coin.wav',
        'Power Up.wav',
        'spritesheet_jumper.png',
        'Yippee.wav',
        'Hitl.wav',
        'snd.txt',
        'highscore.txt',
        "sprites.py",
        'settings.py',
    ]
}
base = None

if sys.platform == 'win32':
    base = 'Win32Gui'


setup(
    name="Jumpin' platforms",
    version="1",
    description="pygame",
    options={'build_exe': build_exe_options},
    executables=[Executable(
        'main.py',
        base=base,
        icon='Jumpin.ico'),
    ])
