import os
from api.gui_api import GuiApi
import match
import argparse
import json
import threading
import time

def get_config(config_file=None):
    if config_file:
        config = json.loads(open(config_file, 'r').read())
    else:
        config = json.loads(open('config.json', 'r').read())

    return config


parser = argparse.ArgumentParser(description='NeonFC')
parser.add_argument('--config_file', default='config.json')
parser.add_argument('--env', default='simulation')

args = parser.parse_args()

class Game():
    def __init__(self, config_file=None, env='simulation'):
        self.fps = 0
        self.config = get_config(config_file)
        self.match = match.Match(self,
            **self.config.get('match')
        )
        self.environment = env

        self.gui_api_active = self.config.get("gui_api")
        self.gui_api_addr = self.config.get("network").get("gui_api_addr")
        self.gui_api_port = self.config.get("network").get("gui_api_port")
        # self.gui_api = GuiApi(self.gui_api_addr, self.gui_api_port)
        
        self.start()

    def start(self):
        self.match.start()
        # thread do match
        # match_thread = threading.Thread(target=self.match.start)
        # match_thread.start()

        # thread da GUI API
        if self.gui_api_active:
            self.gui_api = GuiApi(self.gui_api_addr, self.gui_api_port, self.match)
            # time.sleep(1000)  # wait for Match to be set up
            gui_thread = threading.Thread(target=self.gui_api.start)
            gui_thread.start()

        # self.match.start()

        # if self.gui_api_active:
        #     self.gui_api.start()

        self.prev_time = time.time()

        self.update()
    
    def update(self):
        while True:
            time.sleep(0.01)
            self.match.update()
            self.fps = 1.0 / (time.time() - self.prev_time)
            self.prev_time = time.time()
            # print(round(self.fps))

        # self.match.update(frame)

        # if self.gui_api_active:
            #     # TODO receive info, process info, send new info
            #     pass

g = Game(config_file=args.config_file, env=args.env)
