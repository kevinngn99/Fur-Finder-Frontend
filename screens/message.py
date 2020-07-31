from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, ColorProperty
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivymd.uix.snackbar import Snackbar
from kivy.uix.screenmanager import Screen, ScreenManager

import asyncio
import websockets
import json
from threading import Thread
from threading import Semaphore
import os


Builder.load_file(os.path.join(os.path.dirname(__file__), '../KivyFile/message.kv'))


class MessagePreview(ButtonBehavior, AnchorLayout):
    icon = StringProperty('')
    chevron = StringProperty('')


class MessageBox(AnchorLayout):
    icon = StringProperty('')
    rgb = ColorProperty(get_color_from_hex('#c9d0dc'))


class Sender(AnchorLayout):
    pass


class Receiver(AnchorLayout):
    pass


class MessageHeader(AnchorLayout):
    name = StringProperty('')
    icon = StringProperty('')


class CustomBackButton(ButtonBehavior, AnchorLayout):
    pass


class MainMessageHeader(BoxLayout):
    pass


class Header:
    def create(self, name='', padding=(dp(20), dp(20), dp(20), dp(0))):
        anchor_layout = AnchorLayout(size_hint=(1, 0.1), anchor_x='left', anchor_y='top', padding=padding)
        header = Label(halign='left', valign='top', font_size=sp(20), color=get_color_from_hex('#023b80'), text='[font=assets/Inter-SemiBold.ttf]' + name, markup=True)
        header.bind(size=header.setter('text_size'))
        anchor_layout.add_widget(header)
        return anchor_layout


class Chat(Screen):
    message = StringProperty('')

    def on_focus(self, instance, value, icon=None, border=None):
        if value:
            border.rgb = get_color_from_hex('#023b80')
            icon.color = get_color_from_hex('#023b80')
        else:
            if instance.text != '':
                pass
                sender = Sender()
                sender.ids.message.text = instance.text
                self.message_layout.add_widget(sender)
                self.message = instance.text

            border.rgb = get_color_from_hex('#c9d0dc')
            icon.color = get_color_from_hex('#c9d0dc')
            instance.text = ''

    def callback(self, instance, value):
        if value > self.sv_size:
            if len(self.message_layout.children) > 0:
                widget = self.message_layout.children[0]
                self.scroll_view.scroll_to(widget)

    def scroll_view_size(self, instance, value):
        self.sv_size = value

    def go_back(self, screen_manager):
        screen_manager.current = 'MS'

    def on_message(self, instance, value):
        # you can do this or use fbind method, didn't know that
        self.sem.release()
        return value

    def __init__(self, sm=None, sem=None, text_name=None, **kw):
        super().__init__(**kw)
        self.sv_size = None
        self.sem = sem
        self.text_name = text_name

        box_layout = BoxLayout(orientation='vertical', spacing=dp(14), padding=(dp(20), dp(0), dp(20), dp(0)))
        message_header = MessageHeader(name=self.text_name)
        message_header.ids.back_button.on_release = lambda: self.go_back(sm)
        box_layout.add_widget(message_header)

        message_box = MessageBox(size_hint=(1, None), height=dp(45), icon='')
        message_box.ids.category.fbind('focus', self.on_focus, icon=message_box.ids.icon, border=message_box)

        self.message_layout = BoxLayout(size_hint=(1, None), orientation='vertical', spacing=dp(7))
        self.message_layout.bind(minimum_height=self.message_layout.setter('height'))
        self.scroll_view = ScrollView(size_hint=(1, 1), effect_cls=ScrollEffect, bar_inactive_color=(0, 0, 0, 0), bar_color=(0, 0, 0, 0))
        self.scroll_view.add_widget(self.message_layout)
        self.scroll_view.fbind('size', self.scroll_view_size)
        self.scroll_view.fbind('viewport_size', self.callback)

        box_layout.add_widget(self.scroll_view)
        box_layout.add_widget(message_box)

        self.add_widget(box_layout)


class Message(Screen):
    token = StringProperty('')
    room = StringProperty('')

    async def send_message(self, websocket, sem, uri):
        screen = self.screen_manager.get_screen(uri)

        while self.stop:
            sem.acquire()
            if screen.message != '':
                await websocket.send(json.dumps({'message': screen.message}))

    def message_loop(self, websocket, sem, uri):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_message(websocket, sem, uri))

    async def secret_room(self, uri, initiator=False):
        try:
            async with websockets.connect(uri) as websocket:
                if not initiator:
                    sem = Semaphore()

                    while self.stop:
                        resp = json.loads(await websocket.recv())['message']

                        if not self.screen_manager.has_screen(uri):
                            Snackbar(text='You got a new message!').show()
                            message_preview = MessagePreview(size_hint=(1, None), height=dp(60))
                            username = uri.replace('wss://fur-finder-chat.herokuapp.com/ws/chatt/', '').replace(self.token, '').replace('/', '')
                            message_preview.ids.user.text = username
                            message_preview.on_release = lambda: self.profile_callback(self.screen_manager, uri)
                            chat_screen = Chat(name=uri, sm=self.screen_manager, sem=sem, text_name=username)
                            receiver = Receiver()
                            receiver.ids.message.text = resp
                            chat_screen.message_layout.add_widget(receiver)
                            self.screen_manager.add_widget(chat_screen)
                            self.message_layout.add_widget(message_preview)

                            th = Thread(target=self.message_loop, args=(websocket, sem, uri))
                            th.setDaemon(True)
                            th.start()
                        else:
                            chat_screen = self.screen_manager.get_screen(uri)

                            if chat_screen.message != resp:
                                receiver = Receiver()
                                receiver.ids.message.text = resp
                                self.screen_manager.get_screen(uri).message_layout.add_widget(receiver)
                else:
                    sem = Semaphore()

                    if not self.screen_manager.has_screen(uri):
                        message_preview = MessagePreview(size_hint=(1, None), height=dp(60))
                        username = uri.replace('wss://fur-finder-chat.herokuapp.com/ws/chatt/', '').replace(self.token, '').replace('/', '')
                        message_preview.ids.user.text = username
                        message_preview.on_release = lambda: self.profile_callback(self.screen_manager, uri)
                        chat_screen = Chat(name=uri, sm=self.screen_manager, sem=sem, text_name=username)
                        self.screen_manager.add_widget(chat_screen)
                        self.message_layout.add_widget(message_preview)
                        self.screen_manager.current = chat_screen.name

                    th = Thread(target=self.message_loop, args=(websocket, sem, uri))
                    th.setDaemon(True)
                    th.start()

                    while self.stop:
                        resp = json.loads(await websocket.recv())['message']

                        if chat_screen.message != resp:
                            receiver = Receiver()
                            receiver.ids.message.text = resp
                            self.screen_manager.get_screen(uri).message_layout.add_widget(receiver)

        except Exception as e:
            print(e)

    def chat(self, value=None):
        if value is None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            uri = 'wss://fur-finder-chat.herokuapp.com/ws/chatt/' + str(self.room) + '/'
            loop.run_until_complete(self.secret_room(uri))
        else:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            uri = 'wss://fur-finder-chat.herokuapp.com/ws/chatt/' + value + '/'
            loop.run_until_complete(self.secret_room(uri, True))

    def run_chat(self, instance, value):
        if instance is not None:
            th = Thread(target=self.chat)
            th.setDaemon(True)
            th.start()
        else:
            th = Thread(target=self.chat, args=(value, ))
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

    async def connect_room(self, uri, user):
        try:
            async with websockets.connect(uri) as websocket:
                await websocket.send(json.dumps({'message': user + self.token}))

        except Exception as e:
            print(e)

    def send_room(self, user):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        uri = 'wss://fur-finder-chat.herokuapp.com/ws/chatt/' + user + '/'
        loop.run_until_complete(self.connect_room(uri, user))
        print('ROOM SENT')

    def run_send_room(self, user):
        th = Thread(target=self.send_room, args=(user, ))
        th.setDaemon(True)
        th.start()
        th.join()

        self.run_chat(None, user + self.token)

    def init_chat(self, user):
        self.run_send_room(user)

    def profile_callback(self, screen_manager, screen_name):
        screen_manager.current = str(screen_name)

    def __init__(self, **kw):
        super().__init__(**kw)

        self.stop = True
        self.screen_manager = ScreenManager(size_hint=(1, 1))

        box_layout = BoxLayout(orientation='vertical')
        box_layout.add_widget(MainMessageHeader())
        self.message_layout = BoxLayout(size_hint=(1, None), orientation='vertical', spacing=dp(20), padding=(dp(20), dp(0), dp(20), dp(0)))
        self.message_layout.bind(minimum_height=self.message_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 0.9), effect_cls=ScrollEffect, bar_inactive_color=(0, 0, 0, 0), bar_color=(0, 0, 0, 0))
        scroll_view.add_widget(self.message_layout)
        box_layout.add_widget(scroll_view)

        message_layout_screen = Screen(name='MS')
        message_layout_screen.add_widget(box_layout)

        self.screen_manager.add_widget(message_layout_screen)
        self.screen_manager.current = 'MS'
        self.add_widget(self.screen_manager)

        self.fbind('token', self.run_main)
        self.fbind('room', self.run_chat)
