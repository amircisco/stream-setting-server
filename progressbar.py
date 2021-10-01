from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
import arabic_reshaper
import bidi.algorithm
import time


class CustomProgressBar():
    def __init__(self,title,max_lenght):
        self.title=self.init_persian_text(title)
        self.max_lenght=max_lenght
        self.sent=0
        self.done=int((self.sent*100)/self.max_lenght)
        self.is_live=True

    def show_popup_loading_dynamic(self):
        layout=BoxLayout(padding=10,orientation="vertical")
        self.popupLabel= Label(text=str(self.done)+"%",font_size=20,font_name="Assets/Fonts/BKoodakBold.ttf",size_hint=(1,.2))
        layout.add_widget(self.popupLabel)
        self.pb=ProgressBar()
        self.pb.height=50
        layout.add_widget(self.pb)
        text_btn=self.init_persian_text("انصراف")
        self.btn=Button(text=text_btn,font_size=20,font_name="Assets/Fonts/BKoodakBold.ttf",size_hint=(1,.2))
        self.btn.on_press=self.click_enseraf
        layout.add_widget(self.btn)
        self.popup = Popup(title=self.title,content=layout,auto_dismiss = False,size_hint= (.6,.3))
        self.popup.title_font="Assets/Fonts/BKoodakBold.ttf"
        self.popup.title_size=20
        self.popup.title_align="right"
        self.popup.open()
        Clock.schedule_interval(self.update_loading,0.5)

    def update_loading(self,dt):
        self.done=int((self.sent*100)/self.max_lenght)
        self.popupLabel.text=str(self.done)+"%"
        self.pb.value=self.done
        if self.done>=100:
            Clock.unschedule(self.update_loading)
            self.popupLabel.text=self.init_persian_text("با موفقیت انجام شد")
            time.sleep(.5)
            self.close()

    def click_enseraf(self):
        Clock.unschedule(self.update_loading)
        self.close()
        self.is_live=False

    def close(self):
        try:
            self.popup.dismiss()
        except:
            print("pop up dont run")


    def init_persian_text(self,text):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = bidi.algorithm.get_display(reshaped_text)
        return bidi_text