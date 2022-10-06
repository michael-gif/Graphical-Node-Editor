from distutils.core import setup
import py2exe

setup(
    options={
        'py2exe': {
            'includes': ['tkinter', 'pygame']
        }
    },
    windows=[
        {
            'script': 'main.py',
            'icon_resources': [(1, 'icon.ico')]
        }
    ]
)