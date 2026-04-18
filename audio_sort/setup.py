from setuptools import setup
setup(
    name = 'audio_sort',
    version = '0.1.0',
    packages = ['audio_sort'],
    entry_points = {
        'console_scripts': [
            'audio_sort = audio_sort.__main__:main'
        ]
    })
