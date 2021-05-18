from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.app import App
from itertools import cycle
import json

# Configure Window
Window.size = (1920, 1080)
Window.clearcolor = (1, 1, 1, 1)


class Participant:
    def __init__(self, name, roles):
        self.name = name
        self.roles = roles
        self.short_name = " ".join([word[0] for word in name.split()])


class AreaCanvas(Widget):
    def __init__(self, **kwargs):
        super(AreaCanvas, self).__init__(**kwargs)

        with self.canvas:

            self.ids = {}
            self.participants = []
            Color(0, 1, 0, 1)
            for obj in self.participants:
                Line(points=obj, width=2)

    def on_touch_down(self, touch):

        def draw_diamond(x, y, r=10):
            return [x, y, x + r, x, y - 2*r, x - r, y - r, x, y]

        def draw_squer(x, y, r=10):
            return [x, y, x + r, y, x + r, y - r, x, y - r, x, y]

        self.participants.append(draw_squer(touch.x, touch.y))




class ParticipantsList(RecycleView):
    def __init__(self, **kwargs):
        super(ParticipantsList, self).__init__(**kwargs)
        self.data = []


class DragLabel(Label):
    def delete_participant(self, touch, drg_lbl):
        prt_list = drg_lbl.parent.parent
        if touch.is_double_tap and self.collide_point(*touch.pos):
            prt_list.data = [x for x in prt_list.data if list(x.values())[0] != drg_lbl.text]
            prt_list.refresh_from_data()


class MainView(Screen):
    def add_participant(_, value, prt_list, *args):
        roles = [role.text for role in args if role.state == 'down']
        for btn in args:
            btn.state = 'normal'

        participant = Participant(value.text, roles)
        prt_list.data.append({"text": participant.name, 'roles': participant.roles})
        value.text = ""
        prt_list.refresh_from_data()

    def save_participants(_, participants):
        with open('./participants.json', 'w') as file:
            json.dump(participants.data, file)

    def clear_list(_, prt_list):
        prt_list.data = []
        prt_list.refresh_from_data()


class CheerApp(App):

    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        self.main = MainView()
        return self.main

    def _on_file_drop(self, window, file_path):
        file_path = file_path.decode('ascii')
        if file_path.find('.json'):
            with open(file_path, 'r') as json_data:
                for data in json_data:
                    data = json.loads(data)
                    self.main.children[0].children[0].children[1].data = data


if __name__ == "__main__":
    CheerApp().run()
