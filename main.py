from kivy.app import App
import time
from kivy.uix.image import Image
from kivy.core.window import Window
import cv2
from kivy.graphics.texture import Texture
import threading
from popup import PopUp
import requests
import config
import base64
import numpy as np
import CustomTime
import os
from queue import Queue
from Encoding import encrypt_cisco
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import arabic_reshaper
import bidi.algorithm
import datetime
import socket
from messagebox import MessageBox
from kivy.uix.treeview import TreeView
import translate
from initConfig import initConfig
import traceback
import re
from generate_key import GenerateKey
import win32api
from distutils.dir_util import copy_tree
import shutil
from progressbar import CustomProgressBar

class VideoPlayerNoCrl(Image):
    def __init__(self, **kwargs):
        super(VideoPlayerNoCrl, self).__init__(**kwargs)
        self.start()
    def pr1(self):
        Clock.schedule_interval(self.update,1.0/30)

    def start(self):
        self.capture=cv2.VideoCapture("Assets/video/1.mp4")
        th1=threading.Thread(target=self.pr1)
        th1.daemon=True
        th1.start()

    def update(self,dt):
        ret,frame=self.capture.read()
        if ret:
            frame=cv2.resize(frame,(self.width,self.height))
            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()
        else:
            time.sleep(2)
            Clock.unschedule(self.update)
            self.source="none.jpg"
            Window.maximize()
            MainKivyApp.my_screenmanager.current="customsetting"

# all screens sort ......

class Tizer(Screen):
    pass

class MyComputerView(Screen):


    def on_pre_leave(self, *args):
        MainKivyApp.my_screenmanager.ids.txt_path.text=""
        MainKivyApp.my_screenmanager.ids.drive.text=".."
        MainKivyApp.my_screenmanager.ids.type_data_transfer.text=".."
        MainKivyApp.my_screenmanager.ids.soojeh_name.text=".."
    def on_enter(self, *args):
        threading.Thread(target=self.get_first_data).start()
    def get_first_data(self):
        MainKivyApp.app.show_popup()
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            address=(MainKivyApp.conf.get_update_config('sender_ip'),int(MainKivyApp.conf.get_update_config('port_rec_video_frame')))
            s.connect(address)
            s.sendall('e@e@e@'.encode('utf-8'))
            do=True
            try:
                encoding=encrypt_cisco('qwe!@#rty$%^uio&*(oiuytrewq(*&^%$#@!')
                while do:
                    recive=s.recv(1024)
                    recive=encoding.decrypt(recive)
                    recive=recive.decode('utf-8')
                    arr=recive.strip().split(MainKivyApp.conf.get_update_config('communicate_spliter'))
                    if len(arr)>0:
                        MainKivyApp.app.close_popup()
                        MainKivyApp.dir_copy_paste=arr[0]
                        MainKivyApp.dir_copy_paste=MainKivyApp.dir_copy_paste+"/media/"
                        MainKivyApp.my_screenmanager.ids.txt_path.text=MainKivyApp.dir_copy_paste
                        MainKivyApp.arr_soojeh=arr[1].split(',')
                        if len(MainKivyApp.arr_soojeh)>0 and len(MainKivyApp.arr_soojeh[0])>0:
                            MainKivyApp.arr_soojeh.insert(0,'..')
                            MainKivyApp.my_screenmanager.ids.soojeh_name.values=MainKivyApp.arr_soojeh
                        else:
                            MainKivyApp.my_screenmanager.ids.txt_path.text=MainKivyApp.app.init_persian_text('...')
                            MainKivyApp.arr_soojeh=list()
                        tmp_arr=arr[2].split(',')
                        for x in range(0,len(tmp_arr)) :
                            if len(tmp_arr[x].split('@')[1])>0:
                                tmp_arr[x]=tmp_arr[x].split('@')[0]+"    "+tmp_arr[x].split('@')[1]
                            else:
                                tmp_arr[x]=tmp_arr[x].split('@')[0]
                        MainKivyApp.my_screenmanager.ids.drive.values=tmp_arr
                        do=False

            except:
                MainKivyApp.app.close_popup()
                traceback.print_exc()
        except:
            MainKivyApp.app.close_popup()
            MainKivyApp.app.ShowMessageBox('توجه','ارتباط با فرستنده برقرار نشد')

class ViewCameraSetting(Screen):
    def show_popup(self):
        self.flg=False
        self.popup=PopUp('در حال اتصال','لطفا صبر کنید',MainKivyApp.app)
        self.popup.show_popup_loading_dynamic()

    def refresh_fo_black(self,img):
        frame=cv2.imread(config.img_none)
        width=int(img.width)
        height=int(img.height)
        frame=cv2.resize(frame,(width,height))
        texture = img.texture
        w, h = frame.shape[1], frame.shape[0]
        if not texture or texture.width != w or texture.height != h:
            img.texture = texture = Texture.create(size=(w, h))
            texture.flip_vertical()
        texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
        img.canvas.ask_update()

    def on_pre_enter(self, *args):
        self.refresh_fo_black(MainKivyApp.my_screenmanager.ids.img1)
        self.refresh_fo_black(MainKivyApp.my_screenmanager.ids.img2)
        self.refresh_fo_black(MainKivyApp.my_screenmanager.ids.img3)
        self.refresh_fo_black(MainKivyApp.my_screenmanager.ids.img4)
    def on_enter(self, *args):
        threading.Thread(target=self.starting).start()


    def starting(self):
        self.qu_camera=40
        self.show_popup()
        self.flg_th1=False
        self.flg_img1=False
        self.flg_th2=False
        self.flg_img2=False
        self.flg_th3=False
        self.flg_img3=False
        self.flg_th4=False
        self.flg_img4=False
        self.th1=threading.Thread(target=self.cam1)
        self.th1.start()
        self.th2=threading.Thread(target=self.cam2)
        self.th2.start()
        self.th3=threading.Thread(target=self.cam3)
        self.th3.start()
        self.th4=threading.Thread(target=self.cam4)
        self.th4.start()
        time.sleep(2)
        Clock.schedule_interval(self.update,1.0/30)

    def on_pre_leave(self, *args):
        try:
            Clock.unschedule(self.update)
            self.flg_th1=True
            self.th1.join()
            self.flg_th2=True
            self.th2.join()
            self.flg_th3=True
            self.th3.join()
            self.flg_th4=True
            self.th4.join()
            self.cap1.release()
            self.cap2.release()
            self.cap3.release()
            self.cap4.release()
        except:
            traceback.print_exc()



    def update(self,dt):
        if self.flg==False:
            self.popup.close()
            self.flg=True

        try:
            if self.flg_img1:
                texture = MainKivyApp.my_screenmanager.ids.img1.texture
                w, h = self.frame1.shape[1], self.frame1.shape[0]
                if not texture or texture.width != w or texture.height != h:
                    MainKivyApp.my_screenmanager.ids.img1.texture = texture = Texture.create(size=(w, h))
                    texture.flip_vertical()
                texture.blit_buffer(self.frame1.tobytes(), colorfmt='bgr')
                MainKivyApp.my_screenmanager.ids.img1.canvas.ask_update()

            if self.flg_img2:
                texture = MainKivyApp.my_screenmanager.ids.img2.texture
                w, h = self.frame2.shape[1], self.frame2.shape[0]
                if not texture or texture.width != w or texture.height != h:
                    MainKivyApp.my_screenmanager.ids.img2.texture = texture = Texture.create(size=(w, h))
                    texture.flip_vertical()
                texture.blit_buffer(self.frame2.tobytes(), colorfmt='bgr')
                MainKivyApp.my_screenmanager.ids.img2.canvas.ask_update()

            if self.flg_img3:
                texture = MainKivyApp.my_screenmanager.ids.img3.texture
                w, h = self.frame3.shape[1], self.frame3.shape[0]
                if not texture or texture.width != w or texture.height != h:
                    MainKivyApp.my_screenmanager.ids.img3.texture = texture = Texture.create(size=(w, h))
                    texture.flip_vertical()
                texture.blit_buffer(self.frame3.tobytes(), colorfmt='bgr')
                MainKivyApp.my_screenmanager.ids.img3.canvas.ask_update()


            if self.flg_img4:
                texture = MainKivyApp.my_screenmanager.ids.img4.texture
                w, h = self.frame4.shape[1], self.frame4.shape[0]
                if not texture or texture.width != w or texture.height != h:
                    MainKivyApp.my_screenmanager.ids.img4.texture = texture = Texture.create(size=(w, h))
                    texture.flip_vertical()
                texture.blit_buffer(self.frame4.tobytes(), colorfmt='bgr')
                MainKivyApp.my_screenmanager.ids.img4.canvas.ask_update()
        except:
            print("error in cameras")

    def cam1(self):
        try:
            self.cap1=cv2.VideoCapture(config.sourc1)
            while self.flg_th1==False:
                ret,frame=self.cap1.read()
                if ret:
                    self.flg_img1=True
                    width=int(MainKivyApp.my_screenmanager.ids.img1.width)
                    height=int(MainKivyApp.my_screenmanager.ids.img1.height)
                    frame=cv2.resize(frame,(width,height))
                    encodec_param=[int(cv2.IMWRITE_JPEG_QUALITY),self.qu_camera]
                    ret,frame=cv2.imencode('.jpg',frame,encodec_param)
                    self.frame1=cv2.imdecode(frame,cv2.IMREAD_COLOR)
        except:
            print("cam1 not start...")

    def cam2(self):
        try:
            self.cap2=cv2.VideoCapture(config.sourc2)
            while self.flg_th2==False:
                ret,frame=self.cap2.read()
                if ret:
                    self.flg_img2=True
                    width=int(MainKivyApp.my_screenmanager.ids.img2.width)
                    height=int(MainKivyApp.my_screenmanager.ids.img2.height)
                    frame=cv2.resize(frame,(width,height))
                    encodec_param=[int(cv2.IMWRITE_JPEG_QUALITY),self.qu_camera]
                    ret,frame=cv2.imencode('.jpg',frame,encodec_param)
                    self.frame2=cv2.imdecode(frame,cv2.IMREAD_COLOR)
        except:
            print("cam2 not start...")


    def cam3(self):
        try:
            self.cap3=cv2.VideoCapture(config.sourc3)
            while self.flg_th3==False:
                ret,frame=self.cap3.read()
                if ret:
                    self.flg_img3=True
                    width=int(MainKivyApp.my_screenmanager.ids.img3.width)
                    height=int(MainKivyApp.my_screenmanager.ids.img3.height)
                    frame=cv2.resize(frame,(width,height))
                    encodec_param=[int(cv2.IMWRITE_JPEG_QUALITY),self.qu_camera]
                    ret,frame=cv2.imencode('.jpg',frame,encodec_param)
                    self.frame3=cv2.imdecode(frame,cv2.IMREAD_COLOR)
        except:
            print("cam3 not start...")

    def cam4(self):
        try:
            self.cap4=cv2.VideoCapture(config.sourc4)
            while self.flg_th4==False:
                ret,frame=self.cap4.read()
                if ret:
                    self.flg_img4=True
                    width=int(MainKivyApp.my_screenmanager.ids.img4.width)
                    height=int(MainKivyApp.my_screenmanager.ids.img4.height)
                    frame=cv2.resize(frame,(width,height))
                    encodec_param=[int(cv2.IMWRITE_JPEG_QUALITY),self.qu_camera]
                    ret,frame=cv2.imencode('.jpg',frame,encodec_param)
                    self.frame4=cv2.imdecode(frame,cv2.IMREAD_COLOR)
        except:
            print("cam4 not start...")


class CustomSetting(Screen):
    def on_leave(self, *args):
        MainKivyApp.my_screenmanager.ids.gr_1.opacity=1
        MainKivyApp.my_screenmanager.ids.gr_1.size_hint=(1,.2)
        MainKivyApp.my_screenmanager.ids.gr_2.opacity=0

    def show_popup(self):
        self.popup=PopUp('در حال اتصال','لطفا صبر کنید',MainKivyApp.app)
        self.popup.show_popup_loading_dynamic()
    def close_popup(self):
        self.popup.close()

    def on_enter(self, *args):
        if len(MainKivyApp.conf.get_update_config('sender_ip'))>1:
            MainKivyApp.my_screenmanager.ids.txt_sender_ip.text=MainKivyApp.conf.get_update_config('sender_ip')

    def clicked_btn_save_info_before(self):
        threading.Thread(target=self.clicked_btn_save_info).start()

    def clicked_btn_save_info(self):
        ip=MainKivyApp.my_screenmanager.ids.txt_center_ip.text
        if len(ip.split('.'))==4:
            try:
                change_data='sender_ip="'+MainKivyApp.conf.get_update_config('sender_ip')+'"'
                change_data+='\n'
                center_ip=MainKivyApp.my_screenmanager.ids.txt_center_ip.text
                change_data+='reciver_ip="'+center_ip+'"'
                change_data+='\n'
                #key=MainKivyApp.my_screenmanager.ids.txt_key.text
                change_data+='key='+MainKivyApp.conf.get_update_config('key')
                change_data+='\n'
                if MainKivyApp.my_screenmanager.ids.txt_qu_frame_up.state=="down":
                    qu=90
                elif MainKivyApp.my_screenmanager.ids.txt_qu_frame_middle.state=="down":
                    qu=70
                elif MainKivyApp.my_screenmanager.ids.txt_qu_frame_down.state=="down":
                    qu=50
                change_data+='qu='+str(qu)
                change_data+='\n'
                sourc1=MainKivyApp.my_screenmanager.ids.txt_url_cam1.text.strip()
                if sourc1.isdigit():
                    change_data+='sourc1='+sourc1
                else:
                    change_data+='sourc1="'+sourc1+'"'
                change_data+='\n'
                sourc2=MainKivyApp.my_screenmanager.ids.txt_url_cam2.text.strip()
                if sourc2.isdigit():
                    change_data+='sourc2='+str(sourc2)
                else:
                    change_data+='sourc2="'+sourc2+'"'
                change_data+='\n'
                sourc3=MainKivyApp.my_screenmanager.ids.txt_url_cam3.text.strip()
                if sourc3.isdigit():
                    change_data+='sourc3='+str(sourc3)
                else:
                    change_data+='sourc3="'+sourc3+'"'
                change_data+='\n'
                sourc4=MainKivyApp.my_screenmanager.ids.txt_url_cam4.text.strip()
                if sourc4.isdigit():
                    change_data+='sourc4='+str(sourc4)
                else:
                    change_data+='sourc4="'+sourc4+'"'
                change_data+='\n'
                if MainKivyApp.my_screenmanager.ids.txt_cont_detect_high.state=="down":
                    count_frame_detect=5
                elif MainKivyApp.my_screenmanager.ids.txt_cont_detect_middle.state=="down":
                    count_frame_detect=10
                elif MainKivyApp.my_screenmanager.ids.txt_cont_detect_low.state=="down":
                    count_frame_detect=15
                change_data+='count_frame_detect='+str(count_frame_detect)
                change_data+='\n'
                if MainKivyApp.my_screenmanager.ids.txt_save_video.active==False:
                    do_save_video=0
                else:
                    do_save_video=1

                change_data+='do_save_video_in_sender='+str(do_save_video)
                change_data+='\n'

                change_data+='do_save_video=0'
                change_data+='\n'

                if len(MainKivyApp.my_screenmanager.ids.txt_soojeh_name.text)>0:
                    change_data+='soojeh_name="'+str(MainKivyApp.my_screenmanager.ids.txt_soojeh_name.text)+'"'
                else:
                    change_data+='soojeh_name=""'
                change_data+='\n'
                change_data+='\n'

                s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                address=(MainKivyApp.conf.get_update_config('sender_ip'),int(MainKivyApp.conf.get_update_config('port_rec_video_frame')))
                s.connect(address)
                s.sendall('b@b@b@'.encode('utf-8'))
                do=True
                encoding=encrypt_cisco('qwe!@#rty$%^uio&*(oiuytrewq(*&^%$#@!')
                while do:
                    recive=s.recv(1024)
                    recive=encoding.decrypt(recive)
                    recive=recive.decode('utf-8')
                    if recive=="88":
                        change_data=change_data.encode('utf-8')
                        data=encoding.encrypt(change_data)
                        s.sendall(data)
                        while True:
                            recive=s.recv(1024)
                            recive=encoding.decrypt(recive)
                            recive=recive.decode('utf-8')
                            if recive=="88":
                                if len(MainKivyApp.my_screenmanager.ids.txt_soojeh_name.text)<1:
                                    msg=MessageBox('انجام شد','ذخیره سازی انجام شد اما نام سوژه را وارد نکردید،در صورت تمایل دوباره نام سوژه را اصلاح کنید',MainKivyApp.app)
                                    msg.show_message_box()
                                msg=MessageBox('انجام شد','با موفقیت در فرستنده ذخیره شد',MainKivyApp.app)
                                msg.show_message_box()
                                s.close()

                            else:
                                msg=MessageBox('انجام نشد','اطلاعات به درستی ارسال نشد',MainKivyApp.app)
                                msg.show_message_box()
                            do=False
                            break

            except:
                traceback.print_exc()
        else:
            msg=MessageBox(translate.mytr.get('warning'),translate.mytr.get('plz_check_reciver_ip'),MainKivyApp.app)
            msg.show_message_box()

    def save_info_to_config(self,new_data):
        data=new_data+'br=""'+MainKivyApp.conf.get_data().split('br=""')[1]
        MainKivyApp.conf.write_data(data)

    def clicked_btn_update_info_before(self):
        threading.Thread(target=self.clicked_btn_update_info).start()

    def clicked_btn_update_info(self):
        ip=MainKivyApp.my_screenmanager.ids.txt_sender_ip.text
        if len(ip.split('.'))==4:
            self.show_popup()
            try:
                s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                address=(ip,int(MainKivyApp.conf.get_update_config('port_rec_video_frame')))
                s.connect(address)
                s.sendall('a@a@a@'.encode('utf-8'))
                while True:
                    data=s.recv(5214)
                    self.close_popup()
                    encoding=encrypt_cisco('qwe!@#rty$%^uio&*(oiuytrewq(*&^%$#@!')
                    data=encoding.decrypt(data)
                    data=data.decode('utf-8')
                    data=data.split('br=""')[0]
                    self.save_info_to_config(data)
                    center_ip=self.parse_setting(data,'reciver_ip')
                    MainKivyApp.my_screenmanager.ids.txt_center_ip.text=center_ip
                    #MainKivyApp.my_screenmanager.ids.txt_key.text=self.parse_setting(data,'key')
                    qu=int(self.parse_setting(data,'qu'))
                    if qu==50:
                        MainKivyApp.my_screenmanager.ids.txt_qu_frame_down.state="down"
                    elif qu==70:
                        MainKivyApp.my_screenmanager.ids.txt_qu_frame_middle.state="down"
                    elif qu==90:
                        MainKivyApp.my_screenmanager.ids.txt_qu_frame_up.state="down"
                    sourc1=self.parse_setting(data,'sourc1')
                    MainKivyApp.my_screenmanager.ids.txt_url_cam1.text=sourc1
                    sourc2=self.parse_setting(data,'sourc2')
                    MainKivyApp.my_screenmanager.ids.txt_url_cam2.text=sourc2
                    sourc3=self.parse_setting(data,'sourc3')
                    MainKivyApp.my_screenmanager.ids.txt_url_cam3.text=sourc3
                    sourc4=self.parse_setting(data,'sourc4')
                    MainKivyApp.my_screenmanager.ids.txt_url_cam4.text=sourc4

                    MainKivyApp.my_screenmanager.ids.txt_soojeh_name.text=str(self.parse_setting(data,'soojeh_name'))
                    count_frame_detect=int(self.parse_setting(data,'count_frame_detect'))
                    if count_frame_detect==15:
                        MainKivyApp.my_screenmanager.ids.txt_cont_detect_low.state="down"
                    elif count_frame_detect==10:
                        MainKivyApp.my_screenmanager.ids.txt_cont_detect_middle.state="down"
                    elif count_frame_detect==5:
                        MainKivyApp.my_screenmanager.ids.txt_cont_detect_high.state="down"

                    do_save_video=self.parse_setting(data,'do_save_video_in_sender')
                    if do_save_video=="0":
                        MainKivyApp.my_screenmanager.ids.txt_save_video.active=False
                    else:
                        MainKivyApp.my_screenmanager.ids.txt_save_video.active=True
                    MainKivyApp.my_screenmanager.ids.gr_1.opacity=0
                    MainKivyApp.my_screenmanager.ids.gr_1.size_hint=(1,.05)
                    MainKivyApp.my_screenmanager.ids.gr_2.opacity=1
                    s.close()
                    break
            except:
                self.close_popup()
                MainKivyApp.app.ShowMessageBox('توجه','ارتباط برقرا نشد، لطفا آی پی فرستنده را اصلاح نمایید')
                traceback.print_exc()
        else:
            msg=MessageBox(translate.mytr.get('warning'),translate.mytr.get('plz_check_sender_ip'),MainKivyApp.app)
            msg.show_message_box()

    def parse_setting(self,data,key):
        try:
            az=data.find(key)
            ta=data.find('\n',az)
            tmp=data[az:ta]
            if tmp.find('"') > -1 :
                return tmp.split('"')[1]
            else:
                return tmp.split('=')[1]
        except:
            traceback.print_exc()


class WindowManager(ScreenManager):
    def __init__(self):
        super(WindowManager, self).__init__()

# end all screens sort .........

class MainKivyApp(App):
    my_screenmanager=None
    app=None
    conf=initConfig()
    encoding=None
    gen=GenerateKey()
    dir_copy_paste=""
    arr_soojeh=list()
    list_drives=list()
    def build(self):
        MainKivyApp.encoding=encrypt_cisco(MainKivyApp.gen.get_uniq_key(MainKivyApp.conf.get_update_config('key')))
        MainKivyApp.app=self
        self.icon="Assets/icons/logo.jpg"
        MainKivyApp.my_screenmanager=WindowManager()
        return MainKivyApp.my_screenmanager

    def init_persian_text(self,text):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = bidi.algorithm.get_display(reshaped_text)
        return bidi_text

    def convert_code_string(self,key):
        return self.init_persian_text(translate.mytr.get(key))

    def change_screen_for_refresh(self,first,second):
        MainKivyApp.my_screenmanager.current=first
        MainKivyApp.my_screenmanager.current=second

    def go_to_page(self,page_name):
        MainKivyApp.my_screenmanager.current=page_name

    def check_persian_char(self,body):
        ret=""
        for x in body:
            if 0>ord(x) > 500 :
                ret="en"
                break
            elif 1500>ord(x)>2000:
                ret="fa"
                break
            elif 60000>ord(x)<70000:
                ret="fa_k"
                break

        return ret


    def show_go_back(self):
        MainKivyApp.my_screenmanager.ids.gr_1.opacity=1
        MainKivyApp.my_screenmanager.ids.gr_1.size_hint=(1,.2)
        MainKivyApp.my_screenmanager.ids.gr_2.opacity=0

    def ShowMessageBox(self,title,message):
        msg=MessageBox(title,message,MainKivyApp.app)
        msg.show_message_box()

    def show_popup(self):
        self.popup=PopUp('در حال اتصال','لطفا صبر کنید',MainKivyApp.app)
        self.popup.show_popup_loading_dynamic()
    def close_popup(self):
        self.popup.close()

    def bef_copy_paste_data(self):
        if len(MainKivyApp.arr_soojeh)>0:
            threading.Thread(target=self.copy_paste_data).start()
        else:
            self.ShowMessageBox('توجه','هیچ رسانه ای ذخیره نشده است')
    def copy_paste_data(self):
        self.popup=PopUp('در حال بررسی','لطفا صبر کنید',MainKivyApp.app)
        self.popup.show_popup_loading_dynamic()
        drive=MainKivyApp.my_screenmanager.ids.drive.text[0]
        t=MainKivyApp.my_screenmanager.ids.type_data_transfer.text
        soojeh=MainKivyApp.my_screenmanager.ids.soojeh_name.text
        src=MainKivyApp.dir_copy_paste+soojeh+"/"
        if soojeh=="..":
            src=MainKivyApp.dir_copy_paste
        dst=drive+":/"
        sender_data=t+MainKivyApp.conf.get_update_config('communicate_spliter')+src+MainKivyApp.conf.get_update_config('communicate_spliter')+dst
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address=(MainKivyApp.conf.get_update_config('sender_ip'),int(MainKivyApp.conf.get_update_config('port_rec_video_frame')))
        s.connect(address)
        s.sendall('f@f@f@'.encode('utf-8'))
        do=True
        try:
            encoding=encrypt_cisco('qwe!@#rty$%^uio&*(oiuytrewq(*&^%$#@!')
            while do:
                recive=s.recv(1024)
                recive=encoding.decrypt(recive)
                recive=recive.decode('utf-8')
                if recive=="88":
                    data_str=sender_data.encode('utf-8')
                    data=encoding.encrypt(data_str)
                    s.sendall(data)
                    while True:
                        recive=s.recv(1024)
                        recive=encoding.decrypt(recive)
                        recive=recive.decode('utf-8')
                        if recive.startswith("77"):
                            self.popup.close()
                            self.ShowMessageBox('توجه','حجم رسانه بیش از ظرفیت ارد درایو انتخاب شده میباشد')
                            do=False
                            break
                        elif recive.startswith("11"):
                            self.popup.close()
                            self.popup.close()
                            size_kol=int(recive.split("@")[1])
                            size_kol=int(size_kol/1000)
                            cl=CustomProgressBar('در حال جابجایی',size_kol)
                            cl.show_popup_loading_dynamic()
                        elif recive.startswith("23"):
                            sent=int(recive.split('@')[1])
                            sent=int(sent/1000)
                            cl.sent=sent
                        elif recive.startswith('12'):
                            self.popup=PopUp('در حال حذف','عملیات انتقال انجام شد.در حال حذف اطلاعات ، بهتر است تا پایان حرف منتظر بمانید',MainKivyApp.app)
                            self.popup.show_popup_loading_dynamic()
                        elif recive.startswith('88'):
                            self.popup.close()
                            cl.close()
                            self.ShowMessageBox('توجه','عملیات به خوبی و با موفقیت انجام شد')
                            do=False
                            break

        except:
            self.popup.close()
            traceback.print_exc()


    def ccc(self):

        cl=CustomProgressBar('در حال جابجایی',1200)
        cl.show_popup_loading_dynamic()
        sent=1
        while True:
            cl.sent=sent
            time.sleep(0.5)
            sent+=50


if __name__=="__main__":
    main=MainKivyApp()
    main.run()

