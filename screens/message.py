from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, ColorProperty
from kivy.uix.scrollview import ScrollView
import asyncio
import websockets
import json
from threading import Thread
from threading import Semaphore

import os


Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/message.kv'))


class MessageBox(AnchorLayout):
    icon = StringProperty('')
    rgb = ColorProperty(get_color_from_hex('#c9d0dc'))


class Sender(AnchorLayout):
    pass


class Receiver(AnchorLayout):
    pass


class Message(Screen):
    token = StringProperty('')
    room = StringProperty('')
    message = StringProperty('')

    class Header:
        def create(self):
            anchor_layout = AnchorLayout(size_hint=(1, 0.1), anchor_x='left', anchor_y='top', padding=(dp(20), dp(20), dp(20), dp(0)))
            header = Label(halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Inter-SemiBold.ttf]Messages', markup=True)
            header.bind(size=header.setter('text_size'))
            anchor_layout.add_widget(header)
            return anchor_layout

    def on_message(self, instance, value):
        self.sem.release()
        return value

    async def send_message(self, websocket):
        while self.stop:
            self.sem.acquire()
            await websocket.send(json.dumps({'message': self.message}))

    def message_loop(self, websocket):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_message(websocket))

    async def secret_room(self, uri):
        try:
            async with websockets.connect(uri) as websocket:
                th = Thread(target=self.message_loop, args=(websocket, ))
                th.setDaemon(True)
                th.start()

                while self.stop:
                    resp = json.loads(await websocket.recv())['message']

                    if resp != self.message:
                        receiver = Receiver()
                        receiver.ids.message.text = resp
                        self.message_layout.add_widget(receiver)

        except Exception as e:
            print(e)

    def chat(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        uri = 'wss://fur-finder-chat.herokuapp.com/ws/chatt/' + str(self.room) + '/'
        loop.run_until_complete(self.secret_room(uri))

    def run_chat(self, instance, value):
        th = Thread(target=self.chat)
        th.setDaemon(True)
        th.start()

    async def web(self, uri):
        try:
            async with websockets.connect(uri) as websocket:
                while self.stop:
                    resp = await websocket.recv()
                    print('PRIVATE ROOM: ', json.loads(resp)['message'])
                    self.room = json.loads(resp)['message']

        except Exception as e:
            print(e)

    def main(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        uri = 'wss://fur-finder-chat.herokuapp.com/ws/chatt/' + str(self.token) + '/'
        loop.run_until_complete(self.web(uri))

    def run_main(self, instance, value):
        th = Thread(target=self.main)
        th.setDaemon(True)
        th.start()

    def on_focus(self, instance, value, icon=None, border=None):
        if value:
            border.rgb = get_color_from_hex('#023b80')
            icon.color = get_color_from_hex('#023b80')
        else:
            if instance.text != '':
                sender = Sender()
                sender.ids.message.text = instance.text
                self.message_layout.add_widget(sender)
                self.message = instance.text

            border.rgb = get_color_from_hex('#c9d0dc')
            icon.color = get_color_from_hex('#c9d0dc')
            instance.text = ''

    def __init__(self, **kw):
        super().__init__(**kw)
        self.stop = True
        self.sem = Semaphore()

        box_layout = BoxLayout(orientation='vertical', spacing=dp(14), padding=(dp(20), dp(0), dp(20), dp(0)))
        box_layout.add_widget(self.Header().create())

        self.message_box = MessageBox(size_hint=(1, None), height=dp(45), icon='')
        self.message_box.ids.category.fbind('focus', self.on_focus, icon=self.message_box.ids.icon, border=self.message_box)

        self.message_layout = BoxLayout(orientation='vertical', spacing=dp(7))
        self.message_layout.bind(minimum_height=self.message_layout.setter('height'))
        self.message_layout.add_widget(Sender())
        self.message_layout.add_widget(Receiver())
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.message_layout)

        box_layout.add_widget(scroll_view)
        box_layout.add_widget(self.message_box)

        self.add_widget(box_layout)

        self.fbind('token', self.run_main)
        self.fbind('room', self.run_chat)
