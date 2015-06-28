from twisted.scripts.twistd import run
from os.path import dirname,join
from sys import argv


argv[1:1] = ['-n', '-y', join(dirname(__file__), 'app.py')]
run()