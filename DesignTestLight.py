# Lights imports
import time
from python_hue_v2 import Hue, BridgeFinder

class HueLightSystem:

    ipAddress = ""
    appKey = ""


    def __init__(self):
        finder = BridgeFinder()
        time.sleep(1)  # wait for search
        # Get server by mdns
        host_name = finder.get_bridge_server_lists()[0]  # Here we use first Hue Bridge
        addresses = finder.get_bridge_addresses()
        # If you don't have hue-app-key, press the button and call bridge.connect() (this only needs to be run a single time)
        print("press the button on your hue")
        self.hue = Hue(host_name)
        app_key = self.hue.bridge.connect()  # you can get app_key and storage on disk
        self.lights = self.hue.lights

    def create_hue_with_nothing(self):
        finder = BridgeFinder()
        time.sleep(1)  # wait for search
        # Get server by mdns
        host_name = finder.get_bridge_server_lists()[0]  # Here we use first Hue Bridge
        addresses = finder.get_bridge_addresses()
        # If you don't have hue-app-key, press the button and call bridge.connect() (this only needs to be run a single time)
        print("press the button on your hue")
        self.hue = Hue(host_name)
        app_key = self.hue.bridge.connect()  # you can get app_key and storage on disk

    def create_hue(self, ipAddress, appKey):
        self.ipAddress = ipAddress
        self.appKey = appKey
        self.hue = Hue(ipAddress, appKey)
        self.lights = self.hue.lights

    def change_all_lights_pink(self):
        for light in self.lights:
            light.color_xy = {'x':0.451, 'y':0.172}

    def change_all_lights_green(self):
        for light in self.lights:
            light.color_xy = {'x':0.226, 'y':0.554}

    def turn_off_all_lights(self):
        for light in self.lights:
            light.on = False

    def turn_on_all_lights(self):
        for light in self.lights:
            light.on = True