#!/usr/bin/env python3

from subprocess import Popen
from random import choice
from requests import get as rget
from json import loads, dumps
from PIL import Image, ImageDraw, ImageFont
from os import path, remove


class Overlay:
    def __init__(self, joke, width, height):
        self.image = Image.new('RGB', (width, height), color=(69, 39, 44))
        font = ImageFont.truetype('/usr/share/fonts/MesloLGS/MesloLGS NF Regular.ttf', 24)
        drawed = ImageDraw.Draw(self.image)
        drawed.text(
            (((width - len(joke['punch']) * 10) / 2), height / 2),
            joke['title'] + '\n' + joke['punch'],
            font=font,
            fill=(248, 228, 215)
        )


class Background:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.width, self.height = self.image.size
        self.converted = self.image.convert("RGBA")


class Joke:
    def __init__(self):
        self.joke = None
        self.saved_jokes = '/tmp/saved_jokes.json'
        if not path.exists(self.saved_jokes):
            self.request_jokes()
        self.joke = self.get_joke()

    def request_jokes(self):
        request_header = {
            'User-agent': 'dergnomi-dadjoke-bot'
        }
        jsondata = rget('https://www.reddit.com/r/ProgrammerDadJokes.json', headers=request_header).json()

        jokes = []
        for joke_object in jsondata['data']['children']:
            jokes.append({'title': joke_object['data']['title'], 'punch': joke_object['data']['selftext']})

        with open(self.saved_jokes, 'w') as fp:
            fp.write(dumps(jokes))

    def get_joke(self):
        with open(self.saved_jokes, 'r') as fp:
            jokes = loads(fp.read())
        return choice(jokes)


class Screenshot:
    def __init__(self):
        self.path = '/tmp/screen.png'
        self.create_screenshot()

    def create_screenshot(self):
        # Create a Screenshot
        scrot = Popen(['scrot', self.path])
        scrot.wait()
        # Open Image and get width and height
        image = Image.open(self.path)
        width, height = image.size
        # create pixelart by scale it down to 10% and back to previous resolution
        convert = Popen([
            'convert',
            self.path,
            '-scale', '10%',
            '-resize', str(width) + 'x' + str(height),
            self.path
        ])
        convert.wait()

    def clean(self):
        remove(self.path)


def create_lockscreen(lockscreen_path):
    screenshot = Screenshot()
    joke = Joke().joke
    bg = Background(screenshot.path)
    overlay = Overlay(joke, bg.width, bg.height).image
    lockscreen = Image.blend(bg.image, overlay, 0.5)
    lockscreen.save(lockscreen_path, 'PNG')
    # Cleanup of tmp files
    screenshot.clean()


if __name__ == '__main__':
    lock_location = '/tmp/lock.png'
    create_lockscreen(lock_location)
    lock = Popen(['i3lock', '-i', lock_location])
    lock.wait()
    remove(lock_location)
