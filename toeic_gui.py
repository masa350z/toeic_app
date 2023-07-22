# coding:utf-8

import toeic_def as tc
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.text import LabelBase, DEFAULT_FONT
LabelBase.register(DEFAULT_FONT, "ipaexg.ttf")

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        self.toeic = tc.Word()
        self.word = self.toeic.ret_word()
        self.answer = self.toeic.ret_answer()

        self.upper = BoxLayout(padding=10)
        self.upper.orientation = "vertical"
        self.word_l = Label(text=self.word)
        self.answer_l = Label(text=' ')
        self.states_l = Label(text=' ')
        self.upper.add_widget(self.word_l)
        self.upper.add_widget(self.answer_l)
        self.upper.add_widget(self.states_l)
        self.add_widget(self.upper)

        self.box = BoxLayout(padding=10)
        button = Button(text='回答を表示')
        button.bind(on_press=self.make_answer_button)
        self.box.add_widget(button)
        self.add_widget(self.box)

    def show_answer(self):
        self.upper.remove_widget(self.answer_l)
        self.upper.remove_widget(self.states_l)
        self.answer_l = Label(text=self.answer)
        self.states_l = BoxLayout()
        for i in ['正答率','表示回数','スコア']:
            temp = BoxLayout()
            temp.orientation = 'vertical'
            temp.add_widget(Label(text=i))
            temp.add_widget(Label(text='ー'))
            self.states_l.add_widget(temp)
        self.upper.add_widget(self.answer_l)
        self.upper.add_widget(self.states_l)

    def make_show_button(self,a):
        self.remove_widget(self.box)
        self.box = BoxLayout(padding=10)
        button = Button(text='回答を表示')
        button.bind(on_press=self.make_answer_button)
        self.box.add_widget(button)
        self.add_widget(self.box)

    def show_score(self,t_or_f):
        states = self.toeic.refresh_states(t_or_f)
        self.upper.remove_widget(self.states_l)

        self.states_l = BoxLayout()
        correct = str(states[0])+'%'
        appear = str(states[1])+'回'
        score = str(states[2])
        for i in [['正答率',correct],['表示回数',appear],['スコア',score]]:
            temp = BoxLayout()
            temp.orientation = 'vertical'
            temp.add_widget(Label(text=i[0]))
            temp.add_widget(Label(text=i[1]))
            self.states_l.add_widget(temp)

        self.upper.add_widget(self.states_l)

    def correct_answer(self,a):
        self.show_score(True)

        self.remove_widget(self.box)
        self.box = BoxLayout(padding=10)
        button = Button(text='次へ')
        button.bind(on_press=self.clear)
        self.box.add_widget(button)
        self.add_widget(self.box)
        self.toeic.to_csv()

    def incorrect_answer(self,a):
        self.show_score(False)


        self.remove_widget(self.box)
        self.box = BoxLayout(padding=10)
        button = Button(text='次へ')
        button.bind(on_press=self.clear)
        self.box.add_widget(button)
        self.add_widget(self.box)
        self.toeic.to_csv()

    def make_answer_button(self,a):
        self.show_answer()
        self.remove_widget(self.box)
        self.box = BoxLayout(padding=10)
        button = Button(text='正解')
        button.bind(on_press=self.correct_answer)
        self.box.add_widget(button)
        button = Button(text='不正解')
        button.bind(on_press=self.incorrect_answer)
        self.box.add_widget(button)
        self.add_widget(self.box)

    def clear(self,a):
        self.clear_widgets()
        self.orientation = "vertical"

        self.toeic = tc.Word()
        self.word = self.toeic.ret_word()
        self.answer = self.toeic.ret_answer()

        self.upper = BoxLayout(padding=10)
        self.upper.orientation = "vertical"
        self.word_l = Label(text=self.word)
        self.answer_l = Label(text=' ')
        self.states_l = Label(text=' ')
        self.upper.add_widget(self.word_l)
        self.upper.add_widget(self.answer_l)
        self.upper.add_widget(self.states_l)
        self.add_widget(self.upper)

        self.box = BoxLayout(padding=10)
        button = Button(text='回答を表示')
        button.bind(on_press=self.make_answer_button)
        self.box.add_widget(button)
        self.add_widget(self.box)



class MainApp(App):
    def build(self):
        MS = MainScreen()
        return MS

if __name__=="__main__":
    MainApp().run()
