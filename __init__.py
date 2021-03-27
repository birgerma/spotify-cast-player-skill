from mycroft import MycroftSkill, intent_file_handler

import pychromecast
import spotipy
import threading

# import spotify
# >>> 
import spotify_token
from pychromecast.controllers.spotify import SpotifyController


class SpotifyCastPlayer(MycroftSkill):

    _devices = []
    
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.sp_key = sp_key
        self.sp_dc = sp_dc
        token, expires = spotify_token.start_session(sp_dc,sp_key)
        self.spotify_controller = SpotifyController(token, expires)



        username = self.settings.get('username')
        password= self.settings.get('password')
        self.log.info("Settings:" + str(self.settings))
        self.log.info("Username:" + str(username))
        self.log.info("Password:" + str(password))
        # self.session = spotify.Session()
        # self.session.login(username, password)
        client_id = self.settings.get('client_id')
        client_secret = self.settings.get('client_secret')
        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)

        # self._devices.append("Init device")
        self.log.info("Init spotify cast skill")
        thread = threading.Thread(target=self.update_chromecasts)
        thread.start()
        # self.update_chromecasts()

    @intent_file_handler('player.cast.spotify.intent')
    def handle_player_cast_spotify(self, message):
        print("Testing ok")
        self.log.info("Testing:" + str(message))
        self.log.info(dir(message))
        self.log.info(str(message.reply))
        self.log.info(str(message.data))
        device = message.data.get('device')
        media = message.data.get('song')
        playlist = message.data.get('plist')
        text = message.data['utterance']
        self.log.info('User said:' + text)
        self.start_playback(media, playlist, device)
        self.speak_dialog('player.cast.spotify')

    @intent_file_handler('get.devices.indent')
    def handle_get_devices(self, message):
        self.log.info("Get devices:" + str(message))
        self.log.info(dir(message))
        self.log.info(str(message.reply))
        self.log.info(str(message.data))
        text = message.data['utterance']
        self.log.info('User said:' + text)
        device_names = []
        for device in self._devices:
            self.log.info("Device:" + str(device))
            device_names.append(device.name)
        self.speak_dialog('get.devices', {'devices':device_names})


    def start_playback(self, media, playlist, device_str):
        self.log.info("Init playback")
        self.log.info("Media:" + str(media))
        self.log.info("Playlist:" + str(playlist))
        self.log.info("Device:" + str(device_str))
        device = self.get_device(device_str)
        if (device):
            self.log.info("Selected device:" + str(device.name))
        else:
            self.log.info("No device found")

        # username = self.settings.get('username')
        # password= self.settings.get('password')
        # self.log.info("Settings:" + str(self.settings))
        # self.log.info("Username:" + str(username))
        # self.log.info("Password:" + str(password))

        

    # TODO: Fix implementation
    def get_device(self, devics_str):
        default_device = 'Living Room speaker'
        self.log.info("Available devices:" + str(self._devices))
        for device in self._devices:
            self.log.info("Comparing devices:" + str(device.name))
            if(device.name==default_device):
                return device

    def update_chromecasts(self):
        self.log.info("Scanning for chromecasts")
        # devices = pychromecast.get_chromecasts()
        devices, browser = pychromecast.get_chromecasts()
        self.log.info("Devices:" + str(devices))
        for device in devices:
            self.log.info("Device found:" + str(device))
            # print(dir(device))
            # if (device.friendly_name=='Living Room speaker'):
            #     selected = device
            # print(device)
            # print(device.name)
        self._devices = devices
        self.log.info("Done updating, devices found:" + str(len(self._devices)))
        self.log.info(str(len(devices)))
        # self.log.info(str(devices[1]))
        # self.log.info(str(devices[0]))
        self.log.info(devices)


def create_skill():
    return SpotifyCastPlayer()

