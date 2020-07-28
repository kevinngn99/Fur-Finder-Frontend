from kivy.uix.anchorlayout import AnchorLayout
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp
from kivy.properties import StringProperty
import asyncio
import websockets
import json
from threading import Thread


class Header:
    def create(self):
        header = Label(size_hint=(1, 0.1), halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Inter-SemiBold.ttf]Messages', markup=True)
        header.bind(size=header.setter('text_size'))
        return header


class Message(Screen):
    token = StringProperty('')
    room = StringProperty('')

    '''
    async def secret_room(self, uri):
        try:
            async with websockets.connect(uri) as websocket:
                while self.stop:
                    resp = await websocket.recv()
                    print(json.loads(resp)['message'])

        except Exception as e:
            print(e)

    def chat(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        uri = 'wss://fur-finder.herokuapp.com/ws/chatt/' + str(self.room) + '/'
        loop.run_until_complete(self.secret_room(uri))

    def run_chat(self, instance, value):
        th = Thread(target=self.chat)
        th.setDaemon(True)
        th.start()
    '''

    async def web(self, uri):
        try:
            async with websockets.connect(uri) as websocket:
                while self.stop:
                    resp = await websocket.recv()
                    print(json.loads(resp)['message'])
                    self.room = json.loads(resp)['message']

        except Exception as e:
            print(e)

    def main(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        uri = 'wss://fur-finder.herokuapp.com/ws/chatt/' + str(self.token) + '/'
        loop.run_until_complete(self.web(uri))

    def run_main(self, instance, value):
        th = Thread(target=self.main)
        th.setDaemon(True)
        th.start()

    def __init__(self, **kw):
        super().__init__(**kw)
        anchor_layout = AnchorLayout(anchor_x='left', anchor_y='top', padding=(dp(20), dp(20), dp(0), dp(0)))
        anchor_layout.add_widget(Header().create())
        self.add_widget(anchor_layout)
        self.fbind('token', self.run_main)
        self.fbind('room', self.run_chat)
        self.stop = True
