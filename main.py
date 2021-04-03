
import matplotlib
#matplotlib.use('module://garden_matplotlib.backend_kivy')
from matplotlib.figure import Figure


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, DictProperty
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, PushMatrix,Rotate, PopMatrix
from kivy.uix.label import Label
from kivy.metrics import dp, sp, Metrics
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
import datetime
import math
import calendar
from kivy.uix.screenmanager import NoTransition
from kivy.uix.textinput import TextInput
from kivy.storage.jsonstore import JsonStore
from dateutil.relativedelta import *
#from kivy.core.text import Label as CoreLabel
from kivy.uix.bubble import Bubble
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner, SpinnerOption
import random
import time
from functools import partial
from garden_matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from garden_matplotlib.backend_kivyagg import FigureCanvas
import numpy as np
import locale


locale.setlocale(locale.LC_ALL, 'pl_PL.UTF8')


global store
store = JsonStore("store.json")
Builder.load_string("""

#:import ScrollEffect  kivy.effects.scroll.ScrollEffect               

<S1>: #Ekran początkowy, mają być tu wpisy
    sc: sc
    scroll: scroll
    dropdown: dropdown.__self__
    
    Label:
        text: root.mies
        size_hint: 1,None
        pos_hint: {"top": 0.974, "center_x": 0.5}
        height: app.wy/20
        font_size: sp(21)
        canvas.before:
            Color:
                rgba: 1,1,1, 0.5
            Line:
                width: 1.5
                rectangle: (self.x, self.y , self.width,0.00000001)     
    
    ScrollView:
        id: scroll
        size_hint: 1, None
        
        height: app.wy - app.sz/5 - app.wy/15
        do_scroll_y: True
        do_scroll_x: False
        pos_hint: {"top": 0.9}
        on_scroll_move: root.move()
        on_scroll_stop: root.stop()
         
        
        GridLayout:
            id: sc
            cols:1
            padding: app.sz/21,app.wy/35,app.sz/21,0
            spacing: 0, app.wy/23
            size_hint: 1, None
            height: max(scroll.height, self.minimum_height)
            

    GridLayout: # Dolny Layout
        canvas.before:
            Color:
                rgba: 119/255,71/255,131/255,1
            Rectangle:
                pos: self.pos
                size: self.size                   
        bg_color: (1, 0, 0, 0.5)
        rows: 1
        cols: 5
        size_hint: 1, None
        height: app.sz/7
        spacing: (app.sz - 2*app.sz/20)/11.5
        padding: app.sz/20,0,app.sz/20,0
        But:
            textt:"Wpisy"
            bold:True
            background_normal: "wpisyNP.png"
            bacgkround_down: "wpisyNP.png"
        But:
            textt: "Kalendarz"
            background_normal: "kalendarzP.png"
            bacgkround_down: "kalendarzNP.png"
            on_release: root.manager.current = "2"
        GridLayout:
            cols : 1
            size_hint: None, None
            width: q.width
            height: q.height
            orientation: "lr-bt"
            But:
                id: q
                textt: "Dodaj Wpis"
                background_normal: "plus.png"
                bacgkround_down: "plus.png"      
                on_release: dropdown.open(self)
                on_kv_post: dropdown.dismiss()
            DropDown:
                id: dropdown
                size_hint: None, None
                auto_width: False
                auto_height: False
                width: app.sz
                BoxLayout:
                    size_hint: None, None
                    width: app.sz
                    height: self.minimum_height + self.minimum_height/2 
                    spacing: app.sz/12   
                    padding: app.sz/3,0,app.sz/4,app.wy/60
                    Kolko2:
                        textt: "Wczoraj"
                        size_hint: None, None
                        size: app.sz/7,app.sz/7
                        on_release:
                            app.root.get_screen("2").WpisWczoraj()
                            dropdown.dismiss()                   
                    Kolko2:
                        textt: "Dziś"
                        size_hint: None, None
                        size: app.sz/7,app.sz/7
                        font_size: sp(18)
                        on_release: 
                            app.root.get_screen("2").WpisDzis()
                            dropdown.dismiss()
        But:
            textt: "Statystyki"
            background_normal: "statystykiP.png"
            bacgkround_down: "statstykiNP.png"
            on_release: root.manager.current = "3"
        But:
            textt: "Ustawienia"
            background_normal: "ustawieniaP.png"
            bacgkround_down: "ustawieniaNP.png"
            on_release: root.manager.current = "4"



<S2>: #Kalendarz
    zm: zm
    kal: kal
    dropdown: dropdown.__self__

    BoxLayout:
        id: zm
        pos_hint: {"center_x": 0.6, "top": 0.3}
        size_hint: 1,None
    Label:
        size_hint: 1,None
        text: root.zobaczmy
        pos_hint: {"top": 0.974, "center_x": 0.5}
        height: app.wy/20
        font_size:'21sp'
        canvas.before:
            Color:
                rgba: 1,1,1, 0.5
            Line:
                width: 1.5
                rectangle: (self.x, self.y , self.width,0.00000001) 
    BoxLayout:
        orientation: "vertical"
        pos_hint: {"center_x": 0.5, "top": 0.85}
        size_hint: 1,None
        #height: app.wy - app.sz/5.5 - app.wy/10
        
        height: self.minimum_height
        #padding: app.sz/30,0,app.sz/30,-app.wy/10
        padding: app.sz/30,0,app.sz/30,0
        canvas.before:
            Color:
                rgba: 1,1,1, 0.5
            Line:
                width: 1.5
                rectangle: (self.x - app.sz/20, self.y - app.wy/20, self.width + app.sz/10, self.height + app.wy/20) 
      
        GridLayout:
            cols: 7
            rows: 1
            height: app.wy/18
            size_hint: 1,None
            padding: -app.sz/160,0,0,0
            spacing: app.sz/37
            Label:
                text: "Pn"
                font_size: dp(15)
            Label:
                text: "Wt"
                font_size: dp(15)
            Label:
                text: "Śr"
                font_size: dp(15)
            Label:
                text: "Cz"
                font_size: dp(15)
            Label:
                text: "Pt"
                font_size: dp(15)
            Label:
                text: "Sb"
                font_size: dp(15)
            Label:
                text: "Nd"
                font_size: dp(15)

        GridLayout:
            id: kal
            size_hint: 1,None
            height: self.minimum_height
            cols: 7
            spacing: app.sz/30, app.wy/95
            row_default_height: (app.sz - app.sz *8/30) / 7
            row_force_default: True   
    
    GridLayout: # Dolny Layout
        canvas.before:
            Color:
                rgba: 119/255,71/255,131/255,1
            Rectangle:
                pos: self.pos
                size: self.size                   
        bg_color: (1, 0, 0, 0.5)
        rows: 1
        cols: 5
        size_hint: 1, None
        height: app.sz/7
        spacing: (app.sz - 2*app.sz/20)/11.5
        padding: app.sz/20,0,app.sz/20,0
        But:
            textt:"Wpisy"
            background_normal: "wpisyP.png"
            bacgkround_down: "wpisyNP.png"
            on_release: root.manager.current = "1"
        But:
            textt: "Kalendarz"
            bold:True 
            background_normal: "kalendarzNP.png"
            bacgkround_down: "kalendarzNP.png"

        GridLayout:
            cols : 1
            size_hint: None, None
            width: q.width
            height: q.height
            orientation: "lr-bt"
            But:
                id: q
                textt: "Dodaj Wpis"
                background_normal: "plus.png"
                bacgkround_down: "plus.png"      
                on_release: dropdown.open(self)
                on_kv_post: dropdown.dismiss()
            DropDown:
                id: dropdown
                size_hint: None, None
                auto_width: False
                auto_height: False
                width: app.sz
                BoxLayout:
                    size_hint: None, None
                    width: app.sz
                    height: self.minimum_height + self.minimum_height/2
                    spacing: app.sz/12   
                    padding: app.sz/3,0,app.sz/4,app.wy/60
                    Kolko2:
                        textt: "Wczoraj"
                        size_hint: None, None
                        size: app.sz/7,app.sz/7
                        on_release: 
                            app.root.get_screen("2").WpisWczoraj()
                            dropdown.dismiss()                
                    Kolko2:
                        textt: "Dziś"
                        size_hint: None, None
                        size: app.sz/7,app.sz/7
                        font_size: sp(18)
                        on_release: 
                            app.root.get_screen("2").WpisDzis()
                            dropdown.dismiss()
        But:
            textt: "Statystyki"
            background_normal: "statystykiP.png"
            bacgkround_down: "statstykiNP.png"
            on_release: root.manager.current = "3"
        But:
            textt: "Ustawienia"
            background_normal: "ustawieniaP.png"
            bacgkround_down: "ustawieniaNP.png"
            on_release: root.manager.current = "4"

<S3>: #Statystyki
    dropdown: dropdown.__self__
    dropdown2: dropdown2.__self__
    wykresy: wykresy
    box: box
    box2: box2
    box3: box3
    box4: box4
    liniowy: liniowy
    ee: ee
    bar: bar
    pas: pas
    labs: labs
    emotes: emotes
    gl: gl
    
    Label:
        text: root.mies
        size_hint: 1,None
        pos_hint: {"top": 0.974, "center_x": 0.5}
        height: app.wy/20
        font_size: sp(21)
        canvas.before:
            Color:
                rgba: 1,1,1, 0.5
            Line:
                width: 1.5
                rectangle: (self.x, self.y , self.width,0.00000001)     
    ScrollView:
        size_hint: 1, None
        size: (self.parent.width, self.parent.height)
        #height: app.wy - app.sz/5 - app.wy/15
        do_scroll_y: True
        do_scroll_x: False
        pos_hint: {"top": 0.9}
        effect_cls: ScrollEffect
        
        StackLayout:
            id: wykresy
            size_hint: 1, None          
            height: self.minimum_height
            spacing: app.wy/7
            BoxLayout:
                id: box
                orientation: "vertical"
                size_hint: 1,None
                height: self.minimum_height
                spacing: app.wy/80
                canvas.before:
                    Color:
                        rgba: 1,1,1, 0.5
                    Line:
                        width: 1.5
                        rectangle: (self.x, self.y - self.height/50, self.width, 0) 
                Label:
                    text: "Wykres nastroju"
                    size_hint: 1, None
                    height: app.wy/25
                    font_size: sp(25)
                    canvas.before:
                        Color:
                            rgba: 1,1,1, 0.5
                        Line:
                            width: 1.5
                            rectangle: (self.x, self.y, self.width, 0) 
                GridLayout:
                    cols: 2
                    size_hint: 1,None
                    height: self.minimum_height
                    GridLayout:
                        id: ee
                        cols: 1
                        size_hint: None,1
                        width: 0
                        padding: -10,liniowy.height/10,0,0
                        spacing: liniowy.height/22
                        Image:
                            source: "bhappyP.png"
                            size_hint: None,None
                            height: liniowy.height/8
                        Image:
                            source: "happyP.png"        
                            size_hint: None,None
                            height: liniowy.height/8                    
                        Image:
                            source: "takseP.png"   
                            size_hint: None,None
                            height: liniowy.height/8                       
                        Image:
                            source: "sadP.png"
                            size_hint: None,None
                            height: liniowy.height/8                       
                        Image:
                            source: "bsadP.png"
                            size_hint: None,None
                            height: liniowy.height/8                  
                    GridLayout:
                        id: liniowy
                        cols: 1
                        size_hint: 1,None
                        height: app.wy/2.5
            
            BoxLayout:
                id: box2
                orientation: "vertical"
                size_hint: 1,None
                height: self.minimum_height 
                spacing: app.wy/89
                canvas.before:
                    Color:
                        rgba: 1,1,1, 0.5
                    Line:
                        width: 1.5
                        rectangle: (self.x, self.y - self.height/50, self.width, 0.5) 
                Label:
                    text: "Wykres nastroju dni tygodni"
                    size_hint: 1, None
                    height: app.wy/25
                    font_size: sp(25)
                    canvas.before:
                        Color:
                            rgba: 1,1,1, 0.5
                        Line:
                            width: 1.5
                            rectangle: (self.x, self.y, self.width, 0) 
                GridLayout:
                    cols: 2
                    size_hint: 1,None
                    height: self.minimum_height
                    GridLayout:
                        cols: 1
                        size_hint: None,1
                        width: 0
                        padding: -15,bar.height/10,0,0
                        spacing: bar.height/22
                        Image:
                            source: "bhappyP.png"
                            size_hint: None,None
                            height: bar.height/8
                        Image:
                            source: "happyP.png"        
                            size_hint: None,None
                            height: bar.height/8                    
                        Image:
                            source: "takseP.png"   
                            size_hint: None,None
                            height: bar.height/8                       
                        Image:
                            source: "sadP.png"
                            size_hint: None,None
                            height: bar.height/8                       
                        Image:
                            source: "bsadP.png"
                            size_hint: None,None
                            height: bar.height/8                  
                    GridLayout:
                        id: bar
                        cols: 1
                        size_hint: 1,None
                        height: app.wy/3
            
            
            BoxLayout:
                id: box3
                orientation: "vertical"
                size_hint: 1,None
                height: self.minimum_height
                spacing: app.wy/89
                canvas.before:
                    Color:
                        rgba: 1,1,1, 0.5
                    Line:
                        width: 1.5
                        rectangle: (self.x, self.y - self.height/50, self.width, 0)     
                Label:
                    text: "Procentowy rozkład nastrojów"
                    size_hint: 1, None
                    height: app.wy/25
                    font_size: sp(25)
                    canvas.before:
                        Color:
                            rgba: 1,1,1, 0.5
                        Line:
                            width: 1.5
                            rectangle: (self.x, self.y, self.width, 0) 
                GridLayout:
                    id: pas
                    cols: 1
                    size_hint: 1,None
                    height: app.wy/8

                GridLayout:
                    cols: 5
                    rows: 1
                    size_hint: 1,None
                    #padding: -25,liniowy.height/10,0,0
                    #spacing: liniowy.height/22
                    #height: self.minimum_height
                    BoxLayout:
                        size_hint: 1,None
                        height: self.minimum_height
                        orientation: "vertical"
                        Image:
                            source: "bsadP.png"
                            size_hint: 1, None
                            height: app.wy/12
                        Label:
                            text: "1-2"
                            size_hint: 1, None
                            height: app.wy/60
                            font_size: sp(13)
                            color: (120 / 255, 144 / 255, 156 / 255, 1)
                        Label:
                            text: root.jeden
                            size_hint: 1, None
                            height: app.wy/45
                            font_size: sp(18)
                    BoxLayout:
                        size_hint: 1,None
                        height: self.minimum_height
                        orientation: "vertical"
                        Image:
                            source: "sadP.png"
                            size_hint: 1, None
                            height: app.wy/12
                        Label:
                            text: "3-4"
                            size_hint: 1, None
                            height: app.wy/60
                            font_size: sp(13)
                            color: (69 / 255, 99 / 255, 137 / 255, 1)
                        Label:
                            text: root.dwa
                            size_hint: 1, None
                            height: app.wy/45
                            font_size: sp(18)
                    BoxLayout:
                        size_hint: 1,None
                        height: self.minimum_height
                        orientation: "vertical"
                        Image:
                            source: "takseP.png"
                            size_hint: 1, None
                            height: app.wy/12
                        Label:
                            text: "5-6"
                            size_hint: 1, None
                            height: app.wy/60
                            font_size: sp(13)
                            color: (119 / 255, 71 / 255, 131 / 255, 1)
                        Label:
                            text: root.trzy
                            size_hint: 1, None
                            height: app.wy/45
                            font_size: sp(18)
                    BoxLayout:
                        size_hint: 1,None
                        height: self.minimum_height
                        orientation: "vertical"
                        Image:
                            source: "happyP.png"
                            size_hint: 1, None
                            height: app.wy/12
                        Label:
                            text: "7-8"
                            size_hint: 1, None
                            height: app.wy/60
                            font_size: sp(13)
                            color: (53 / 255, 138 / 255, 83 / 255, 1)
                        Label:
                            text: root.cztery
                            size_hint: 1, None
                            height: app.wy/45
                            font_size: sp(18)
                    BoxLayout:
                        size_hint: 1,None
                        height: self.minimum_height
                        orientation: "vertical"
                        Image:
                            source: "bhappyP.png"
                            size_hint: 1, None
                            height: app.wy/12
                        Label:
                            text: "9-10"
                            size_hint: 1, None
                            height: app.wy/60
                            font_size: sp(13)
                            color: (203 / 255, 155 / 255, 25 / 255, 1)
                        Label:
                            text: root.piec
                            size_hint: 1, None
                            height: app.wy/45
                            font_size: sp(18)
                Widget:
                    size_hint: 1,None
                    height: app.wy/13 
            
            BoxLayout:
                id: box4
                orientation: "vertical"
                size_hint: 1, None
                height: self.minimum_height
                spacing: app.wy/69
                Label:
                    size_hint: 1,None
                    font_size: sp(18)
                    text: "Najczęstsze oceny Aktywności dla nastroju Dnia"
                    height: app.wy/25
                    canvas.before:
                        Color:
                            rgba: 1,1,1, 0.5
                        Line:
                            width: 1.5
                            rectangle: (self.x, self.y, self.width, 0) 
                GridLayout:
                    cols : 1
                    size_hint: 1, None
                    #orientation: "lr-bt"
                    height: self.minimum_height
                    padding: app.sz/2.5,0,0,0
                    But:
                        id: gl
                        size_hint: None, None
                        size: app.wy/8.5, app.wy/8.5
                        #textt: "Nastrój"
                        background_normal: "happyP.png"
                        bacgkround_down: "happyP.png"      
                        on_release: dropdown2.open(self)
                        on_kv_post: dropdown2.dismiss()
                    DropDown:
                        id: dropdown2
                        size_hint: None, None
                        BoxLayout:
                            orientation: "vertical"
                            size_hint: 1,None
                            height: self.minimum_height
                            #spacing: app.sz/12   
                            #padding: app.sz/3,0,app.sz/4,app.wy/60
                            canvas.before:
                                Color:
                                    rgba: 1,1,1,1
                                RoundedRectangle:
                                    pos: self.pos
                                    size: self.size
                                    radius: [10,]
                            But:
                                size_hint: None, None
                                size: app.wy/11, app.wy/11
                                background_normal: "bsadP.png"
                                on_press:
                                    app.root.get_screen("3").Stworz(root.today.year,root.today.month,1)
                                    gl.background_normal = self.background_normal
                                    dropdown2.dismiss()           
                            But:
                                size_hint: None, None
                                size: app.wy/11, app.wy/11
                                background_normal: "sadP.png"
                                on_press:
                                    app.root.get_screen("3").Stworz(root.today.year,root.today.month,2)
                                    gl.background_normal = self.background_normal
                                    dropdown2.dismiss()                           
                            But:
                                size_hint: None, None
                                size: app.wy/11, app.wy/11
                                background_normal: "takseP.png"  
                                on_press:
                                    app.root.get_screen("3").Stworz(root.today.year,root.today.month,3)
                                    gl.background_normal = self.background_normal
                                    dropdown2.dismiss()             
                            But:
                                size_hint: None, None
                                size: app.wy/11, app.wy/11
                                background_normal: "happyP.png"
                                on_press:
                                    app.root.get_screen("3").Stworz(root.today.year,root.today.month,4)
                                    gl.background_normal = self.background_normal
                                    dropdown2.dismiss()  
                            But:
                                size_hint: None, None
                                size: app.wy/11, app.wy/11
                                background_normal: "bhappyP.png" 
                                on_press:
                                    app.root.get_screen("3").Stworz(root.today.year,root.today.month,5)
                                    gl.background_normal = self.background_normal
                                    dropdown2.dismiss()                
                GridLayout:
                    cols: 2
                    size_hint: 1,None
                    height: self.minimum_height
                    #orientation: "lr-bt"
                    canvas.before:
                        Color:
                            rgba: 1,1,1, 0.5
                        Line:
                            width: 1.5
                            rectangle: (self.x, self.y, self.width, self.height)                 
                    GridLayout:
                        id: labs
                        cols: 1
                        size_hint: 0.4, None
                        height: self.minimum_height
    
                    
                    GridLayout:
                        id: emotes
                        cols: 1
                        size_hint: 1,None
                        height: self.minimum_height


 

            
            Widget:
                size_hint: 1,None
                height: app.wy/3
    
    
    GridLayout: # Dolny Layout
        canvas.before:
            Color:
                rgba: 119/255,71/255,131/255,1
            Rectangle:
                pos: self.pos
                size: self.size                   
        bg_color: (1, 0, 0, 0.5)
        rows: 1
        cols: 5
        size_hint: 1, None
        height: app.sz/7
        spacing: (app.sz - 2*app.sz/20)/11.5
        padding: app.sz/20,0,app.sz/20,0
        But:
            textt:"Wpisy"
            background_normal: "wpisyP.png"
            bacgkround_down: "wpisyNP.png"
            on_release: root.manager.current = "1"
        But:
            textt: "Kalendarz"           
            background_normal: "kalendarzP.png"
            bacgkround_down: "kalendarzNP.png"
            on_release: root.manager.current = "2"
        GridLayout:
            cols : 1
            size_hint: None, None
            width: q.width
            height: q.height
            orientation: "lr-bt"
            But:
                id: q
                textt: "Dodaj Wpis"
                background_normal: "plus.png"
                bacgkround_down: "plus.png"      
                on_release: dropdown.open(self)
                on_kv_post: dropdown.dismiss()
            DropDown:
                id: dropdown
                size_hint: None, None
                auto_width: False
                auto_height: False
                width: app.sz
                BoxLayout:
                    size_hint: None, None
                    width: app.sz
                    height: self.minimum_height + self.minimum_height/2
                    spacing: app.sz/12   
                    padding: app.sz/3,0,app.sz/4,app.wy/60
                    Kolko2:
                        textt: "Wczoraj"
                        size_hint: None, None
                        size: app.sz/7,app.sz/7
                        on_release:
                            app.root.get_screen("2").WpisWczoraj()
                            dropdown.dismiss()                   
                    Kolko2:
                        textt: "Dziś"
                        size_hint: None, None
                        size: app.sz/7,app.sz/7
                        font_size: sp(18)
                        on_release: 
                            app.root.get_screen("2").WpisDzis()
                            dropdown.dismiss()
        But:
            textt: "Statystyki"
            bold:True 
            background_normal: "statystykiNP.png"
            bacgkround_down: "statstykiNP.png"

        But:
            textt: "Ustawienia"
            background_normal: "ustawieniaP.png"
            bacgkround_down: "ustawieniaNP.png"
            on_release: root.manager.current = "4"

<S4>: #Ustawienia
    dropdown: dropdown.__self__
    
    ScrollView:
        size_hint: 1, None
        height: app.wy - 2*app.wy/13
        pos_hint: {"top": 0.9}
        do_scroll_y: True
        do_scroll_x: False
                
        GridLayout:
            cols: 1
            size_hint: 1,None
            height: self.minimum_height
            Button:
                size_hint: 1,None
                text: "Ustawienia Aktywnosci"
                background_color: 1,1,0,0.5
                font_size: dp(20)
                on_release: root.manager.current = "5"          
            Button:
                size_hint: 1,None
                text: "Informacje"
                background_color: 1,1,0,0.5
                font_size: dp(20)
                on_release: root.manager.current = "8" 

    Label:
        text: "Ustawienia"
        size_hint: 1,None
        pos_hint: {"top": 0.974, "center_x": 0.5}
        height: app.wy/20
        font_size: sp(21)
        canvas.before:
            Color:
                rgba: 1,1,1, 0.5
            Line:
                width: 1.5
                rectangle: (self.x, self.y , self.width,0.00000001)   
         
    
    
    GridLayout: # Dolny Layout
        canvas.before:
            Color:
                rgba: 119/255,71/255,131/255,1
            Rectangle:
                pos: self.pos
                size: self.size                   
        bg_color: (1, 0, 0, 0.5)
        rows: 1
        cols: 5
        size_hint: 1, None
        height: app.sz/7
        spacing: (app.sz - 2*app.sz/20)/11.5
        padding: app.sz/20,0,app.sz/20,0
        But:
            textt:"Wpisy"
            background_normal: "wpisyP.png"
            bacgkround_down: "wpisyNP.png"
            on_release: root.manager.current = "1"
        But:
            textt: "Kalendarz"
            background_normal: "kalendarzP.png"
            bacgkround_down: "kalendarzNP.png"
            on_release: root.manager.current = "2"
        GridLayout:
            cols : 1
            size_hint: None, None
            width: q.width
            height: q.height
            orientation: "lr-bt"
            But:
                id: q
                textt: "Dodaj Wpis"
                background_normal: "plus.png"
                bacgkround_down: "plus.png"      
                on_release: dropdown.open(self)
                on_kv_post: dropdown.dismiss()
            DropDown:
                id: dropdown
                size_hint: None, None
                auto_width: False
                auto_height: False
                width: app.sz
                BoxLayout:
                    size_hint: None, None
                    width: app.sz
                    spacing: app.sz/12   
                    height: self.minimum_height + self.minimum_height/2
                    padding: app.sz/3,0,app.sz/4,app.wy/60
                    Kolko2:
                        textt: "Wczoraj"
                        size_hint: None, None
                        size: app.sz/7,app.sz/7
                        on_release:
                            app.root.get_screen("2").WpisWczoraj()
                            dropdown.dismiss()                   
                    Kolko2:
                        textt: "Dziś"
                        size_hint: None, None
                        size: app.sz/7,app.sz/7
                        font_size: sp(18)
                        on_release: 
                            app.root.get_screen("2").WpisDzis()
                            dropdown.dismiss()
        But:
            textt: "Statystyki"
            background_normal: "statystykiP.png"
            bacgkround_down: "statstykiNP.png"
            on_release: root.manager.current = "3"
        But:
            textt: "Ustawienia"
            bold:True
            background_normal: "ustawieniaNP.png"
            bacgkround_down: "ustawieniaNP.png"

            
<S5>: #Ustawienia Aktywności
    text: text
    arch: arch
    aktyw: aktyw
    GridLayout:
        cols: 1
        size_hint: 1, None
        height: self.minimum_height
        pos_hint: {"top": 0.85}
        spacing: app.wy/70
        padding: app.sz/10,0, app.sz/10,0
        canvas.before:
            Color:
                #rgba: 119/255,71/255,131/255,0.5
                rgba: (.2,.2,.2,0.8)
            Rectangle:
                pos: self.x, self.y - app.wy/30
                size: self.width, self.height + app.wy/15

        TextInput:
            id: text
            halign: "center"
            text: ""
            #color: 1,1,1,1
            selection_color: 1,1,1,1
            size_hint: 1, None
            #size: 100,100
            height: max(app.wy/21, self.minimum_height)
            hint_text: "Wpisz nazwę Aktywności"
            hint_text_color: 1,1,1,1
            foreground_color: (1, 1, 1, 1)
            background_color: 1,1,1,0
            keyboard_suggestions: True
            input_type: 'text'
            canvas.after:
                Color:
                    rgba: 119/255,71/255,131/255,1
                Line:
                    width: 0.3
                    rectangle: (self.x, self.y, self.width, self.height)
        Button:
            size_hint: 0.2, None
            #width: app.sz/3
            height: app.wy/18
            text: "Dodaj Aktywność"
            on_press: root.dodaj()
            background_color: 0,0,0,0
            canvas.before:
                Color:
                    rgba: 119/255,71/255,131/255,0.5
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [25,]
    GridLayout:
        cols: 1
        size_hint: 1, None
        height: self.minimum_height
        pos_hint: {"top": 0.63}
        spacing: app.wy/15
        BoxLayout:
            orientation: "vertical"
            size_hint: 1, None
            height: self.minimum_height
            #spacing: app.wy/1000
            padding: 0,app.wy/55,0,0
            canvas.before:
                Color:
                    #rgba: 119/255,71/255,131/255,0.5
                    rgba: (.2,.2,.2,0.8)
                Rectangle:
                    pos: self.x, self.y
                    size: self.width, self.height       
            Label:
                text: "Aktywności"
                size_hint: 1, None
                height: app.wy/45
                font_size: sp(20)
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1
                    Line:
                        width: 0.5
                        rectangle: (self.x - app.sz/20, self.y - app.wy/120, self.width + app.sz/10, 0)
            ScrollView:
                size_hint: 1, None
                effect_cls: ScrollEffect
                height: (app.wy/2 - app.wy/10)/1.6
                do_scroll_y: True
                do_scroll_x: False
                BoxLayout:
                    id: aktyw
                    size_hint: 1, None
                    height: self.minimum_height
                    orientation: "vertical"
                    padding: app.sz/5,app.wy/40, app.sz/5,0
                    spacing: app.wy/40
     
        BoxLayout:
            orientation: "vertical"
            size_hint: 1, None
            height: self.minimum_height
            #spacing: app.wy/1000
            padding: 0,app.wy/55,0,0
            canvas.before:
                Color:
                    #rgba: 119/255,71/255,131/255,0.5
                    rgba: (.2,.2,.2,0.8)
                Rectangle:
                    pos: self.x, self.y
                    size: self.width, self.height       
            Label:
                text: "Archiwa"
                size_hint: 1, None
                height: app.wy/45
                font_size: sp(20)
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1
                    Line:
                        width: 0.5
                        rectangle: (self.x - app.sz/20, self.y - app.wy/120, self.width + app.sz/10, 0)
            ScrollView:
                size_hint: 1, None
                height: (app.wy/2 - app.wy/10)/1.6
                do_scroll_y: True
                do_scroll_x: False
                effect_cls: ScrollEffect
                BoxLayout:
                    id: arch
                    size_hint: 1, None
                    height: self.minimum_height
                    orientation: "vertical"
                    padding: app.sz/5,app.wy/40, app.sz/5,0
                    spacing: app.wy/40

                

    Label:
        text: "Ustawienia Aktywności"
        size_hint: 1,None
        pos_hint: {"top": 0.974, "center_x": 0.5}
        height: app.wy/20
        font_size: sp(21)
        canvas.before:
            Color:
                rgba: 1,1,1, 0.5
            Line:
                width: 1.5
                rectangle: (self.x, self.y , self.width,0.00000000001) 


<S6>: #Ekran po Kalendarzu
    Button:
        size_hint: 1,None
        height: app.wy/13
        text: "Dodaj Wpis"
        font_size: sp(20)
        on_press: root.manager.current = "7"
        background_normal: ""
        background_color: 119/255,71/255,131/255, 1
        
<S7>: #Dodanie Wpisu
    stack: stack
    scrolek: scrolek
    
    Label:
        text: root.wp
        size_hint: 1,None
        pos_hint: {"top": 0.974, "center_x": 0.5}
        height: app.wy/20
        font_size: sp(21)
        canvas.before:
            Color:
                rgba: 1,1,1, 0.5
            Line:
                width: 1.5
                rectangle: (self.x, self.y , self.width,0.0000001)      
    ScrollView:
        id: scrolek
        size_hint: 1, None
        #size: (self.parent.width, self.parent.height)
        height: app.wy - 2*app.wy/20
        do_scroll_y: True
        effect_cls: ScrollEffect
        StackLayout:
            id: stack
            size_hint: 1,None
            height: self.minimum_height

<S8>: #Screen informacyjny

    GridLayout:
        cols: 2
        size_hint: 1,None
        pos_hint: {"top": 0.93}
        height: self.minimum_height
        
        Label:
            size_hint: 0.4, None
            text: "Wysokosc"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text: str(app.wy)
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 0.4, None
            text: "Szerokosc"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text: str(app.sz)
            height: app.wy/25
            font_size: sp(17)        
        Label:
            size_hint: 0.4, None
            text: "sp(100)"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text: str(sp(100))
            height: app.wy/25
            font_size: sp(17)            
        Label:
            size_hint: 0.4, None
            text: "dp(100)"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text: str(dp(100))
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 0.4, None
            text: "10"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text: str(10)
            height: app.wy/25
            font_size: sp(17)        
        Label:
            size_hint: 0.4, None
            text: "cm(10)"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text: str(cm(10))
            height: app.wy/25
            font_size: sp(17)       
        Label:
            size_hint: 0.4, None
            text: "inch(10)"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text: str(inch(10))
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 0.4, None
            text: "mm(10)"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text: str(mm(10))
            height: app.wy/25
            font_size: sp(17)
            
        Label:
            size_hint: 0.4, None
            text: "pt(100)"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text: str(pt(100))
            height: app.wy/25
            font_size: sp(17)              
        
        Label:
            size_hint: 0.4, None
            text: "Density"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text: root.dens
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 0.4, None
            text: "DPI"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text: root.dpi
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 0.4, None
            text: "dpi_rounded"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text: root.rounded
            height: app.wy/25
            font_size: sp(17) 
        Label:
            size_hint: 0.4, None
            text: "fontscale"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text: root.font
            height: app.wy/25
            font_size: sp(17)           
        Label:
            size_hint: 0.4, None
            text: "ZmienWpis"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text:  root.czas
            height: app.wy/25
            font_size: sp(17)             
        Label:
            size_hint: 0.4, None
            text: "StworzPuste"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text:  root.czas2
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 0.4, None
            text: "Czas Liniowy"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text:  root.czas3
            height: app.wy/25
            font_size: sp(17) 
        Label:
            size_hint: 0.4, None
            text: "Czas Bar"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text:  root.czas4
            height: app.wy/25
            font_size: sp(17) 
        Label:
            size_hint: 0.4, None
            text: "Czas Pasek"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1,None
            text:  root.czas5
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 1, None
            text: "Czas otwarcia Aplikacji"
            height: app.wy/25
            font_size: sp(17)
        Label:
            size_hint: 0.5,None
            text:  app.open
            height: app.wy/25
            font_size: sp(17)      
<Aktywa@BoxLayout>: #Do Ustawien Aktywnosci
    dropdown: dropdown.__self__
    size_hint: 1, None
    height: app.wy/21
    #padding: -app.sz/7,0,0, -self.height/4.5
    padding: 0,0,0, -self.height/3
    textt: "Aktywnosc"
    #on_touch_down: root.proba()
    canvas.before:
        Color:
            rgba: 119/255,71/255,131/255,0.5
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10,]
    Label:
        size_hint: 1, None
        text: root.textt
        height: app.wy/13
        font_size: sp(18) 
    GridLayout:
        cols: 1
        size_hint: None,None
        width: 1.4* root.height
        height: 1.4* root.height
        Button:
            size_hint: None,None
            height: app.wy/18
            width: app.wy/18
            background_normal: "arrow.png"
            on_release: dropdown.open(self)
            on_kv_post: dropdown.dismiss()
            state: "normal" if self.state == "normal" else ("normal")
        DropDown:
            id: dropdown
            size_hint: None, None
            auto_width: False
            width: app.sz/3
            BoxLayout:
                orientation: "vertical"
                size_hint: None, None
                width: app.sz/3
                height: app.wy/10
                canvas.before:
                    Color:
                        #rgba: 119/255,71/255,131/255,1
                        rgba: (.2,.2,.2,1)
                    Rectangle:
                        pos: self.x, self.y
                        size: self.width, self.height                     
                Button:
                    size_hint: 1,1
                    background_color: 0,0,0,0
                    height: app.wy/15
                    text: "Usun"
                    on_press: 
                        app.root.get_screen("5").UsunAkt(root)
                        dropdown.dismiss()
                Button:
                    size_hint: 1,1
                    height: app.wy/15
                    text: "Archiwizuj"
                    background_color: 0,0,0,0
                    on_press: 
                        app.root.get_screen("5").Archiwizuj(root)
                        dropdown.dismiss()

<Archiwa@BoxLayout>: #Do Ustawien Aktywnosci
    dropdown: dropdown.__self__
    size_hint: 1, None
    height: app.wy/21
    padding: 0,0,0, -self.height/3
    textt: "Aktywnosc"
    #on_touch_down: root.proba
    canvas.before:
        Color:
            rgba: 119/255,71/255,131/255,0.5
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10,]
    Label:
        size_hint: 1, None
        font_size: sp(18)
        text: root.textt
        height: app.wy/13
    GridLayout:
        cols: 1
        size_hint: None,None
        width: 1.4* root.height
        height: 1.4* root.height
        Button:
            size_hint: None,None
            height: app.wy/18
            width: app.wy/18
            background_normal: "arrow.png"
            on_press: dropdown.open(self)
            on_kv_post: dropdown.dismiss()
            state: "normal" if self.state == "normal" else ("normal")
        DropDown:
            id: dropdown
            size_hint: None, None
            auto_width: False
            width: app.sz/3
            BoxLayout:
                orientation: "vertical"
                size_hint: None, None
                width: app.sz/3
                height: app.wy/10  
                canvas.before:
                    Color:
                        #rgba: 119/255,71/255,131/255,1
                        rgba: (.2,.2,.2,1)
                    Rectangle:
                        pos: self.x, self.y
                        size: self.width, self.height                     
                Button:
                    size_hint: 1,1
                    background_color: 0,0,0,0
                    height: app.wy/15
                    text: "Usun"
                    on_press: 
                        app.root.get_screen("5").UsunArch(root)
                        dropdown.dismiss()
                Button:
                    size_hint: 1,1
                    height: app.wy/15
                    text: "Przywróć"
                    background_color: 0,0,0,0
                    on_press:                   
                        app.root.get_screen("5").Przywroc(root)
                        dropdown.dismiss()

<But@Button>: #Do dolnego Layoutu
    bold: False
    textt: ""
    size_hint: None,None
    #size: app.wy/13/1.2, app.wy/13/1.2 # DO ZMIANY RACZEJ NA app.sz
    size: app.sz/8.5, app.sz/8.5
    #background_color: (1,1,1,1) if self.state == "normal" else (1,1,1,0.2)
    #background_normal: self.background_normal if self.state == "normal" else self.background_down
    state: "normal" if self.state == "normal" else ("normal")
    Label:
        id: lab
        center_x: root.center_x
        center_y: root.center_y - app.sz/8.5/1.8
        #y: -app.wy/50
        text: root.textt
        bold: root.bold
        font_size: sp(13)

<Kolko2@Button>: #Do dolnego layoutu
    la: la
    t: 0,0,0,0
    textt: ""
    font_size: sp(13)
    background_normal: ""
    background_color: 1,1,1,0
    background_down: ""
    canvas.before:
        Color:
            rgba: 119/255,71/255,131/255,1  
        Line:
            width: 4
            circle:
                (self.center_x, self.center_y, min(self.width, self.height)/2)
        Color:
            rgba: 151/255,89/255,166/255,1
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [90]
    Label:
        id: la
        bold: True
        center: root.center
        color: 1,1,1,1
        text: root.textt
        font_size: root.font_size

<ArrowButton>:
    background_normal: ""
    background_down: ""
    background_color: 1, 1, 1, 0
    size_hint: .1, .1
    font_size:'30sp' 
    bold: True
    disabled_color: (128 / 255, 128 / 255, 128 / 255, 1)

<Kolko@Button>:
    la: la
    t: 0,0,0,0
    background_normal: ""
    background_color: 1,1,1,0
    background_down: ""
    canvas.before:
        Color:
            rgba: root.t
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [90]
    Label:
        id: la
        center: root.center
        color: 1,1,1,1
        text: ""
        font_size: dp(15) 

<Spin>:
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba: 119/255,71/255,131/255,0.5
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15,]


<ScrollWpis@ScrollView>:
    st: st
    size_hint: 1, 1
    #size: (self.child.width, self.child.height)
    #height: self.minimum_height 
    do_scroll_y: True
    StackLayout:
        id: st
        size_hint: 1,None
        height: self.minimum_height             


<Stackk@StackLayout>:
    size_hint: 1,None
    height: self.minimum_height    
    canvas.before:
        Color:
            rgba: 1, 1, 1, .5
        Line:
            width: 1.5
            rectangle: (self.x + app.sz/30, self.y - app.wy/40, self.width - app.sz/15, self.height + app.wy/40)

<Grid1@GridLayout>:
    cols: 5
    rows: 1
    size_hint: 1, None
    padding: app.sz/10,0,app.sz/16 ,0
    spacing: app.sz / 24
    height: self.minimum_height

<Grid2@GridLayout>:
    hei: 0
    wyso: 0
    niesamowite: 0
    cols: 5
    rows: 2 # może dać rows: 3 i wpierodlic tam widgety zeby byl wiekszy odstep miedzy kolkami
    size_hint:1, None
    spacing: app.sz / 74
    padding: app.sz/12,0,app.sz/13 ,0
    row_default_height: app.wy / 11
    height: self.minimum_height # TO SPROBOWAC

<Textt@TextInput>:
    halign: "center"
    #color: 1,1,1,1
    selection_color: 1,1,1,1
    size_hint: None, None
    height: self.minimum_height
    hint_text: "Dodaj Komentarz"
    hint_text_color: 1,0.5,0.5,0.5
    foreground_color: (1, 1, 1, 1)
    background_color: 1,1,1,0.1
    keyboard_suggestions: True
    input_type: 'text'
    canvas.after:
        Color:
            rgba: 1, 0, 0, 1
        Line:
            width: 1
            rectangle: (self.x, self.y, self.width, self.height)

<Komentarz@GridLayout>:
    b: b
    g: g
    cols: 1
    size_hint: None,None
    height: self.minimum_height
    padding: app.sz/12,0,app.sz/13 ,0
    width: app.sz - 2*app.sz/13
    canvas.before:
        Color:
            rgba: 1, 1, 1, .5
        Line:
            width: 0.5
            rectangle: (self.x + app.sz/12, self.y, self.width, self.height)    
    Label:   
        text: "Zapisane Komentarze(Max 4)"
        size_hint: None, None
        height: app.wy/40
        width: app.sz - 2*app.sz/13
        font_size: sp(15)
        canvas.before:
            Color:
                rgba: 1, 1, 1, .5
            Line:
                width: 0.5
                rectangle: (self.x, self.y, self.width, self.height)             
    GridLayout:
        id: g
        cols: 5
        rows: 1
        size_hint: 1,None
        height: self.minimum_height
        width: self.minimum_width
        orientation: "rl-bt"
        col_default_width: (self.width - app.sz/6) / 4
        Button:
            id: b
            background_normal: "plus.png"
            background_down: "plus.png"
            size_hint: None,None
            size: app.sz/6.5, app.sz/6.5

<tekscik@TextInput>:
    background_color: (1,1,1,0) if self.focus else (1,1,1,0)
    canvas.after:
        Color:
            #rgba: 119/255,71/255,131/255,1
            #rgba: 53/255, 138/255, 83/255,1
            rgba: 1,1,1,0.5
        Line:
            width: 0.5
            rectangle: (self.x, self.y, self.width, self.height)
    #text: ""
    size_hint: (1,1)
    #height: 0 if self.text == "" else max(app.wy/25, self.minimum_height)
    cursor_color: 0,0,0,0
    hint_text_color: 1,1,1,1
    selection_color: 0,0,0,0
    readonly: False
    background_active: ""
    auto_indent: True
    allow_copy: False
    foreground_color: 1,1,1,1
    #color: 0,1,0,1
    font_size: sp(12)
    #halign: "center"





<PodstawaWpisu@GridLayout>:
    im1: im1
    im2: im2
    gr: gr
    te: te
    dzien: dzien
    dropdown: dropdown.__self__
    cl: 1,1,1,1
    data: {}    
    cols: 1
    size_hint: 1,None
    height: self.minimum_height
    canvas.before:
        Color:
            rgba: root.cl
        Line:
            width: 1.5
            rectangle: (self.x, self.y, self.width, self.height)
        Color:
            rgba: 1,1,1,0.21
        Rectangle:
            pos: self.pos
            size: self.size

    GridLayout:
        cols: 2
        size_hint: None,None
        width: root.width
        #padding: 0,-app.sz/8/6.5,0,-app.sz/8/6.5
        height: self.minimum_height
        Label: #Tutaj bedzie informacja jaki to dzien
            id: dzien
            size_hint: 1,None
            #text: "Tutaj bedzie tekst"
            height: app.wy/19
            font_size: sp(18)  
        Button:
            size_hint: None, None
            background_normal: "arrow.png"
            height: app.wy/18
            width: app.wy/18
            on_press: dropdown.open(self)
            on_kv_post: dropdown.dismiss()
            state: "normal" if self.state == "normal" else ("normal")
        DropDown:
            id: dropdown
            size_hint: None, None
            auto_width: False
            width: app.sz/3
            BoxLayout:
                orientation: "vertical"
                size_hint: 1, None
                width: app.sz/3
                height: app.wy/6
                
                canvas.before:
                    Color:
                        #rgba: 119/255,71/255,131/255,1
                        rgba: (.2,.2,.2,1)
                    Rectangle:
                        pos: self.x, self.y
                        size: self.width, self.height                     
                Button:
                    size_hint: 1,1
                    background_color: 0,0,0,0
                    height: app.wy/15
                    text: "Edytuj"
                    font_size: sp(17)
                    on_press:
                        app.root.get_screen("1").Edit(root)
                        dropdown.dismiss()
                Button:
                    size_hint: 1,1
                    height: app.wy/15
                    text: "Usuń"
                    background_color: 0,0,0,0
                    font_size: sp(17)
                    on_press:
                        app.root.get_screen("1").Usun(root)           
                        dropdown.dismiss()            

    
    GridLayout: #TRZYMACZ głownej cześci
        id: trzymacz
        cols: 2
        rows: 1
        size_hint: 1, None
        height: max(app.wy/4, self.minimum_height, gr.height)

        GridLayout: #LEWO czyli oceny i komentarz do dnia
            cols: 1
            rows: 2
            size_hint: 0.4, 1
            #height: self.minimum_height
            Image:
                id: im1
                #source: "happyP.png"
                canvas.before:
                    Color:
                        rgba: root.cl
                    Line:
                        width: 1.5
                        rectangle: (self.x, self.y, self.width, self.height)  
            Image:
                id: im2
                #source: "7P.png"
                canvas.before:
                    Color:
                        rgba: root.cl
                    Line:
                        width: 1.5
                        rectangle: (self.x, self.y, self.width, self.height)  
    
        GridLayout: # PRAWO Trzymacz do wpisu aktywnosci
            id: gr
            cols: 1
            size_hint: 1,None
            #height: max(self.minimum_height, trzymacz.height)
            height: max(app.wy/4,self.minimum_height)
            canvas.before:
                Color:
                    rgba: root.cl
                Line:
                    width: 1.5
                    rectangle: (self.x, self.y, self.width, self.height)  

 
    TextInput:
        id: te
        background_color: (1,1,1,0) if self.focus else (1,1,1,0)
        #text:"SZlachetne zdrowie nikt sie nei dowie jako smakujesz"
        size_hint: (1,None) if self.text != "" else (None,None) 
        width: 0
        height: 0 if self.text == "" else max(app.wy/25, self.minimum_height)
        cursor_color: 0,0,0,0
        selection_color: 0,0,0,0
        readonly: True
        background_active: ""
        auto_indent: True
        allow_copy: False
        foreground_color: 1,1,1,1
        font_size: sp(12)
        halign: "center"




<AktWpis@GridLayout>:
    akt: akt
    im: im
    te: te    
    cols: 1
    cl: 1,1,1,1
    size_hint: (1, 1) if self.height > self.minimum_height else (1,None)
    #size_hint: 1,1
    #size_hint: 1,None
    height: self.height if self.height > self.minimum_height else self.minimum_height
    Label:
        id: akt
        size_hint: 1,None
        height: app.wy/30
        #text: "Aktywnosc"
        font_size: sp(15) 
    GridLayout:
        #size_hint: (1, 1) if root.minimum_height < app.wy/9 else (1,None)
        #height: max(self.minimum_height, app.wy/4/2.7/1.6)
        #size_hint: (1, 1)
        #size_hint: (1,1) if root.height > root.minimum_height else (1,None)
        size_hint: (1,1) if self.height > self.minimum_height else (1,None)
        height: self.minimum_height if self.height < self.minimum_height else self.height
        #height: app.wy/4
        cols: 2
        Image:
            id: im
            size_hint: 0.2,0.2
            #source: "5P.png"
            canvas.before:
                Color:
                    rgba: root.cl
                Line:
                    width: 1.5
                    rectangle: (self.x, self.y, self.width, self.height)  
        TextInput:
            id: te
            background_color: (1,1,1,0) if self.focus else (1,1,1,0)
            canvas.before:
                Color:
                    rgba: root.cl
                Line:
                    width: 1.5
                    rectangle: (self.x, self.y, self.width, self.height)  
            #text: " SDFSDFSDFADSDASDSASDASDASS SDFSDFSDFADSDASDSASDASDASSDASDASDnikt sie, Szlachetne zdrowie nikt sie, Szlachetne zdrowie nikt sie  "
            #text: "    sie, Szlachetne zdrowie nikt sie, Szlachetne zdrowie nikt sie "
            #size_hint: ((1,None) if self.minimum_height > self.parent.height else (1,1)) if self.text != "" else (None,None) 
            size_hint: (1,1) if self.height > self.minimum_height else (1,None)
            width: 0
            height: self.minimum_height if self.height < self.minimum_height else self.height
            #height: 0 if self.text == "" else max(app.wy/25, self.minimum_height)
            cursor_color: 0,0,0,0
            selection_color: 0,0,0,0
            readonly: True
            background_active: ""
            auto_indent: True
            allow_copy: False
            foreground_color: 1,1,1,1
            font_size: sp(12)
            halign: "center"


<Lab@Label>:
    size_hint: 1,None
    height: app.wy/13
    text: "NazwaNazwa"
    canvas.before:
        Color:
            rgba: 1,1,1, 0.5
        Line:
            width: 1.5
            rectangle: (self.x, self.y, self.width, self.height)
            

<Grid3@GridLayout>:
    size_hint: 1,None
    height: app.wy/13
    rows: 1
    canvas.before:
        Color:
            rgba: 1,1,1, 0.5
        Line:
            width: 1.5
            rectangle: (self.x, self.y, self.width, self.height)    
            
""")



def ZnajdzMinMax():
    try:
        a = sorted(list(map(int, list(store["daty"]))))
        b = sorted(list(map(int, list(store["daty"][str(a[0])]))))
        c = sorted(list(map(int, list(store["daty"][str(a[-1])]))))
        min = b[0]
        max = c[-1]
        return a[0], min, a[-1], max
    except Exception as e:
        print(e)


# Ekran początkowy, wpisy
class S1(Screen):
    scroll = ObjectProperty()
    mies = StringProperty()

    czas = StringProperty()
    czas2 = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.jasnadupa = 0
        #self.Test2()
        self.StworzPuste()
        global today
        try:
            a, b, c, d = ZnajdzMinMax()
            today = datetime.date(c,d,1)
        except:
            today = datetime.date.today()

        try:
            self.ZmienWpisy(today.year, today.month)
        except Exception as e:
            print(e, "S1 INIT")

        global wpis #Flaga do tego czy zostal dany wpis
        global edit #Chyba do usuniecia
        edit = 0
        wpis = 0
        self.fla = 0
        self.left_arrow = ArrowButton(text="<", on_press=self.Cof,
                                      pos_hint={"top": 1, "left": 0})

        self.right_arrow = ArrowButton(text=">", on_press=self.Nast,
                                       pos_hint={"top": 1, "right": 1})

        self.add_widget(self.left_arrow)

        self.add_widget(self.right_arrow)
        self.mies = str(calendar.month_name[today.month]) + ", " + str(today.year) #Label górny
        Window.bind(on_keyboard=self.Android_back_click)

    def on_pre_enter(self, *args):
        global wpis
        if wpis == 1:
            self.ZmienWpisy(today.year, today.month)
            wpis  = 0
        else:
            pass
        try:
            a,b,c,d = ZnajdzMinMax()
        except:
            a = today.year
            b = today.month
            c = today.year
            d = today.month

        if (today - relativedelta(months=1)).year <= a and (today - relativedelta(months=1)).month < b or ((today).year == a and (today).month == b):
            self.left_arrow.bold = False
            self.left_arrow.disabled = True
            self.strzalka = self.left_arrow
        else:
            self.left_arrow.bold = True
            self.left_arrow.disabled = False

        if ((today + relativedelta(months=1)).year >= c and (today + relativedelta(months=1)).month > d) or ((today).year == c and (today).month == d):
            self.right_arrow.bold = False
            self.right_arrow.disabled = True
            self.strzalka = self.right_arrow
        else:
            self.right_arrow.bold = True
            self.right_arrow.disabled = False


    def Edit(self, el): #Edytuje wpis
        global edit
        global d
        edit = 1
        try:
            d = str(el.data["dzien"]) + "/" + str(el.data["miesiac"]) + "/" + str(el.data["rok"])
        except:
            pass
        global dzis #przekazuje dalej informacje o wpisie do S7
        dzis = datetime.date(int(el.data["rok"]), int(el.data["miesiac"]), int(el.data["dzien"]))
        self.manager.current = "7"
        #Ustawia nazwe dnia

        self.lis = list(store["aktywnosci"])

        for i in list(store["daty"][str(el.data["rok"])][str(el.data["miesiac"])][str(el.data["dzien"])]): #Idziemy po aktywnosciach
            if i != "dzien": # Triggerujemy wszystkie aktywnosci oprocz dnia
                a = self.lis.index(str(i))
                slowniczek[str(store["daty"][str(el.data["rok"])][str(el.data["miesiac"])][str(el.data["dzien"])][str(i)]["ocena"]) + "P.png" + str(a)].trigger_action(0)
                try:
                    slowniczek["text" + str(a)].text = str(store["daty"][str(el.data["rok"])][str(el.data["miesiac"])][str(el.data["dzien"])][str(i)]["komentarz"])
                except:
                    pass
                try:
                    store["tymczasowe"][str(i)]["komentarz"] = str(store["daty"][str(el.data["rok"])][str(el.data["miesiac"])][str(el.data["dzien"])][str(i)]["komentarz"])
                except Exception as e:
                    print(e)
        slowniczek[str(el.im2.source) + str(len(self.lis))].trigger_action(0) #Triggerujemy dzien
        slowniczek["text" + str(len(self.lis))].text = el.te.text
        store["tymczasowe"]["dzien"]["komentarz"] = el.te.text


    def Usun(self, el): # Usuwa Wpis
        self.pom = el
        self.content = BoxLayout()

        self.popup = Popup(title='Czy na pewno chcesz usunąć ten wpis?',
                           content=self.content,
                           size_hint=(None, None), size=(Window.width / 1.5, Window.height / 5))
        self.b1 = Button(text="Tak")
        self.b2 = Button(text="Nie")
        self.b1.bind(on_press=self.UsunKlik)
        self.b2.bind(on_press=self.popup.dismiss)
        self.content.add_widget(self.b1)
        self.content.add_widget(self.b2)
        self.popup.open()


    def UsunKlik(self, el): #Do popupa od Usuwania
        self.sc.remove_widget(self.pom)
        sm.get_screen("6").Usuniecie(self.pom) # TO JEST ABY USUWALO w S6
        del store["daty"][str(self.pom.data["rok"])][str(self.pom.data["miesiac"])][str(self.pom.data["dzien"])]
        store["daty"] = store["daty"]
        self.popup.dismiss()
        self.ZmienWpisy(today.year, today.month)

    def move(self): #Do scrolla podczas poruszania nim
        try:
            self.remove_widget(self.l) #Próbujemy usunąć labela informacyjnego
        except Exception as e:
            #print(e, "MOVE s1")
            pass
        if self.scroll.scroll_y < 0: #Label informacyjny
            self.l = Label(text = "Przesuń w dół, aż napis zmieni się na 'PUSC', aby wyświetlić poprzedni miesiąc", size_hint = (1,None), pos_hint = {"top": 0.2}, font_size = sp(10))
            self.add_widget(self.l)

        if self.scroll.scroll_y < -((self.scroll.height/2.2)/self.sc.height): #Wyliczenie, tak aby mneij więcej overscroll po połowie ekranu zmieniał miesiąc
            self.jasnadupa = 1 #Flaga do zmiany miesiąca
            try:
                self.l.text = "PUŚC" #Label informacyjny
            except:
                pass
        if self.scroll.scroll_y > 1: #Label informacyjny, można zmienić na jednego ifa
            self.l = Label(text = "Przesuń w górę, aż napis zmieni się na 'PUSC', aby wyświetlić następny miesiąc", size_hint = (1,None), pos_hint = {"top": 0.92},font_size = sp(10))
            self.add_widget(self.l)

        if self.scroll.scroll_y > (1+ (self.scroll.height/2.6)/self.sc.height):
            self.jasnadupa = 2
            try:
                self.l.text = "PUŚC"
            except:
                pass

    def stop(self): #Jak zatrzyma sie scroll
        try:
            self.remove_widget(self.l) #Próba usunięcia labela informacyjnego
        except Exception as e:
            #print(e, "STOP s1")
            pass
        if self.jasnadupa == 1: #jeżeli flaga odpowiednia to cofamy
            if self.left_arrow.disabled == False:
                Clock.schedule_once(self.scrollwgore, 0)
                self.Cof(self.left_arrow)
            self.jasnadupa = 0

        if self.jasnadupa == 2: #Idziemy dalej
            if self.right_arrow.disabled == False:
                Clock.schedule_once(self.scrollwdol, 0)
                self.Nast(self.right_arrow)
            self.jasnadupa = 0

    def scrollwdol(self, czas):
        self.scroll.scroll_y = 0

    def scrollwgore(self, czas):
        self.scroll.scroll_y = 1


    def Nast(self, el): #Klik do strzalki prawej, zmienia miesiąc
        global today
        today = today + relativedelta(months=1)
        self.ZmienWpisy(today.year, today.month)
        self.mies = str(calendar.month_name[today.month]) + ", " + str(today.year)
        try: #zapamiętana strzalka, zeby móc cofać disable
            self.strzalka.bold = True
            self.strzalka.disabled = False
            self.strzalka = None
        except:
            pass
        a,b,c,d = ZnajdzMinMax()
        if (today + relativedelta(months=1)).year >= c and (today + relativedelta(months=1)).month > d or ((today).year == c and (today).month == d):
            self.strzalka = el
            el.bold = False
            el.disabled = True



    def Cof(self, el): #Do lewej strzałki
        global today
        today = today - relativedelta(months=1)
        self.ZmienWpisy(today.year, today.month)
        self.mies  = str(calendar.month_name[today.month]) + ", " + str(today.year)
        try:
            self.strzalka.bold = True
            self.strzalka.disabled = False
            self.strzalka = None
        except:
            pass

        a,b,c,d = ZnajdzMinMax()
        if (today - relativedelta(months=1)).year <= a and (today - relativedelta(months=1)).month < b or (today).year == a and (today).month == b :
            self.strzalka = el
            el.bold = False
            el.disabled = True


    def StworzPuste(self): # Tworzy puste wpisy tak, aby potem nimi manipulowac
        czas = time.time()
        try: #żeby na starcie przy tworzeniu aktywnosci
            self.sl = {} # slownik w ktorym sa przechowywane widgety
            store["aktywnosci"] = store["aktywnosci"]
            for i in range(1,32):
                self.a = PodstawaWpisu()
                self.sl[str(i)] = {}
                self.sl[str(i)]["dzien"] = self.a
                try:
                    for l in list(store["aktywnosci"]):
                        self.b = AktWpis()
                        self.sl[str(i)][str(l)] = self.b
                except:
                    pass
        except:
            pass
        self.czas2 = str(time.time() - czas)
        #print(time.time() - czas, "StworzPuste")

    def ZmienWpisy(self, rok, miesiac):
        czas = time.time()
        self.sc.clear_widgets()
        self.licznik = 0 # licznik do pominietych dni
        try:
            for i in range(calendar.monthrange(int(rok), int(miesiac))[1], 0, -1):
                if str(i) in list(store["daty"][str(rok)][str(miesiac)]):
                    try:
                        if self.licznik != 0: #Tworzy Label z informacja ile dni jest pominietych
                            self.label = Label(text=str(self.licznik) + " dni pominiętych", size_hint=(1, None),
                                               height=Window.height / 40)
                            self.sc.add_widget(self.label)
                            self.licznik = 0
                    except:
                        pass

                    self.a2 = self.sl[str(i)]["dzien"] # Zmieniamy PodstaweWpisu
                    self.fl = 0
                    self.a2.gr.clear_widgets()
                    self.a2.gr.clear_widgets()
                    self.a2.data["dzien"] = i #Zapamietuje date dla widgetu, przyda sie przy edicie
                    self.a2.data["miesiac"] = miesiac
                    self.a2.data["rok"] = rok
                    self.a2.te.text = ""
                else:
                    self.licznik += 1
                    if int(i) == 1: # jezeli to koniec pętli niech stworzy ostatni label o pominietch dniach
                        if self.licznik != 0:
                            self.label = Label(text=str(self.licznik) + " dni pominiętych", size_hint=(1, None),
                                               height=Window.height / 40)
                            self.sc.add_widget(self.label)
                            continue
                    else:
                        continue

                try: # Komentarz dla Dnia
                    self.a2.te.text = str(store['daty'][str(rok)][str(miesiac)][str(i)]["dzien"]['komentarz'])
                except:
                    pass
                #Ustawiamy Nazwe dnia
                self.a2.dzien.text = calendar.day_name[
                                         int(datetime.date(int(rok), int(miesiac), int(i)).weekday())] + ", " + str(
                    i) + " " + str(calendar.month_name[int(miesiac)]) + " " + str(int(rok))

                self.a2.im2.source = f"{store['daty'][str(rok)][str(miesiac)][str(i)]['dzien']['ocena']}P.png"
                #Ustawiamy Kolor oraz emotke
                if int(store["daty"][str(rok)][str(miesiac)][str(i)]["dzien"]["ocena"]) in range(1, 3):
                    self.a2.im1.source = "bsadP.png"
                    self.a2.cl = (120 / 255, 144 / 255, 156 / 255, 1)
                elif int(store["daty"][str(rok)][str(miesiac)][str(i)]["dzien"]["ocena"]) in range(3, 5):
                    self.a2.im1.source = "sadP.png"
                    self.a2.cl = (69 / 255, 99 / 255, 137 / 255, 1)
                elif int(store["daty"][str(rok)][str(miesiac)][str(i)]["dzien"]["ocena"]) in range(5, 7):
                    self.a2.im1.source = "takseP.png"
                    self.a2.cl = (119 / 255, 71 / 255, 131 / 255, 1)
                elif int(store["daty"][str(rok)][str(miesiac)][str(i)]["dzien"]["ocena"]) in range(7, 9):
                    self.a2.im1.source = "happyP.png"
                    self.a2.cl = (53 / 255, 138 / 255, 83 / 255, 1)
                elif int(store["daty"][str(rok)][str(miesiac)][str(i)]["dzien"]["ocena"]) in range(9, 11):
                    self.a2.im1.source = "bhappyP.png"
                    self.a2.cl = (203 / 255, 155 / 255, 25 / 255, 1)

                for l in list(store["daty"][str(rok)][str(miesiac)][str(i)]): #Tworzymy aktywnosci
                    if l != "dzien": # dzien stworzylismy wczeiej
                        if str(l) in list(self.sl[str(i)]):
                            self.b2 = self.sl[str(i)][str(l)]
                        else: # TO jest sytuacja, że nie stworzyla sie jakas aktywnosc, moze sie zdarzyc.
                            self.b2 = AktWpis()
                            self.sl[str(i)][str(l)] = self.b2

                        self.b2.akt.text = str(l)
                        self.b2.cl = self.a2.cl
                        if int(store["daty"][str(rok)][str(miesiac)][str(i)][str(l)]["ocena"]) in range(1, 3):
                            self.b2.akt.color = (120 / 255, 144 / 255, 156 / 255, 1)
                        elif int(store["daty"][str(rok)][str(miesiac)][str(i)][str(l)]["ocena"]) in range(3, 5):
                            self.b2.akt.color = (69 / 255, 99 / 255, 137 / 255, 1)
                        elif int(store["daty"][str(rok)][str(miesiac)][str(i)][str(l)]["ocena"]) in range(5, 7):
                            self.b2.akt.color = (119 / 255, 71 / 255, 131 / 255, 1)
                        elif int(store["daty"][str(rok)][str(miesiac)][str(i)][str(l)]["ocena"]) in range(7, 9):
                            self.b2.akt.color = (53 / 255, 138 / 255, 83 / 255, 1)
                        elif int(store["daty"][str(rok)][str(miesiac)][str(i)][str(l)]["ocena"]) in range(9, 11):
                            self.b2.akt.color = (203 / 255, 155 / 255, 25 / 255, 1)
                        self.b2.im.source = f"{store['daty'][str(rok)][str(miesiac)][str(i)][str(l)]['ocena']}P.png"
                        self.b2.te.text = ""
                        try:
                            self.b2.te.text = str(store['daty'][str(rok)][str(miesiac)][str(i)][str(l)]['komentarz'])
                        except:
                            pass
                        self.a2.gr.add_widget(self.b2)

                self.sc.add_widget(self.a2)

            self.w = Widget(size_hint=(1, None), height=Window.height / 3.5)
            self.sc.add_widget(self.w)
            self.czas = str(time.time() - czas)
            #print(time.time() - czas, "ZmianaWpisu")
        except:
            self.brak = Label(text = "BRAK WPISÓW", size_hint = (1,None), height = Window.height/15, font_size = sp(18))
            self.sc.add_widget(self.brak)


    def Test(self): #Wszystkie i wszystko
        self.a = list(store["aktywnosci"])
        store["daty"] = {}
        store["daty"]["2021"] = {}
        for i in range(1,4):
            store["daty"]["2021"][str(i)] = {}
            for j in range(1, calendar.monthrange(2021, int(i))[1] + 1):
                store["daty"]["2021"][str(i)][str(j)] = {}
                store["daty"]["2021"][str(i)][str(j)]["dzien"] = {}
                store["daty"]["2021"][str(i)][str(j)]["dzien"]["ocena"] = str(random.randint(1,10))
                for k in self.a:
                    store["daty"]["2021"][str(i)][str(j)][str(k)] = {}
                    store["daty"]["2021"][str(i)][str(j)][str(k)]["ocena"] = str(random.randint(1,10))

    def Test2(self): #Wszystko i losowo aktynowsci
        self.a = list(store["aktywnosci"])
        store["daty"] = {}
        store["daty"]["2021"] = {}
        for i in range(1,13):
            store["daty"]["2021"][str(i)] = {}
            for j in range(1, calendar.monthrange(2021, int(i))[1] + 1):
                store["daty"]["2021"][str(i)][str(j)] = {}
                store["daty"]["2021"][str(i)][str(j)]["dzien"] = {}
                store["daty"]["2021"][str(i)][str(j)]["dzien"]["ocena"] = str(random.randint(1,10))
                self.am = random.randint(1,len(self.a))
                self.licznik = 1
                for k in self.a:
                    if self.licznik <= self.am:
                        store["daty"]["2021"][str(i)][str(j)][str(k)] = {}
                        store["daty"]["2021"][str(i)][str(j)][str(k)]["ocena"] = str(random.randint(1,10))
                        self.licznik += 1

    def Test3(self): #Co jakis odstep
        self.a = list(store["aktywnosci"])
        store["daty"] = {}
        store["daty"]["2021"] = {}
        for i in range(1,13):
            store["daty"]["2021"][str(i)] = {}
            for j in range(1, calendar.monthrange(2021, int(i))[1] + 1, 4):
                store["daty"]["2021"][str(i)][str(j)] = {}
                store["daty"]["2021"][str(i)][str(j)]["dzien"] = {}
                store["daty"]["2021"][str(i)][str(j)]["dzien"]["ocena"] = str(random.randint(1,10))
                self.am = random.randint(1,len(self.a))
                self.licznik = 1
                for k in self.a:
                    if self.licznik <= self.am:
                        store["daty"]["2021"][str(i)][str(j)][str(k)] = {}
                        store["daty"]["2021"][str(i)][str(j)][str(k)]["ocena"] = str(random.randint(1,10))
                        self.licznik += 1


    def Android_back_click(self, window, key, *largs):
        if key == 27:
            if self.manager.current != "1":
                if self.manager.current == "2":
                    self.manager.current = "1"
                elif self.manager.current == "3":
                    self.manager.current = "2"
                elif self.manager.current == "4":
                    self.manager.current = "3"
                elif self.manager.current == "5":
                    self.manager.current = "4"
                elif self.manager.current == "6":
                    self.manager.current = "2"
                elif self.manager.current == "7":
                    if store["tymczasowe"] == {}:
                        self.manager.current = "6"
                    else:
                        self.content = BoxLayout()
                        self.popup = Popup(title='Czy na chcesz opuścić ten ekran?',
                                           content=self.content,
                                           size_hint=(None, None), size=(Window.width / 1.5, Window.height / 5))
                        self.b1 = Button(text="Tak")
                        self.b2 = Button(text="Nie")
                        self.b1.bind(on_press= self.naszybko)
                        self.b2.bind(on_press=self.popup.dismiss)
                        self.content.add_widget(self.b1)
                        self.content.add_widget(self.b2)
                        self.popup.open()
                elif self.manager.current == "8":
                    self.manager.current = "4"

        return True

    def naszybko(self,el): #Do callback Android
        self.manager.current = "6"
        self.popup.dismiss()


#Kalendarz
class S2(Screen):
    kal = ObjectProperty(None)
    zm = ObjectProperty(None)
    zobaczmy = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global dzien
        global dzis
        self.Generuj()

        self.flaga = 0

        self.left_arrow = ArrowButton(text="<", on_press=self.Cofnij,
                                      pos_hint={"top": 1, "left": 0})

        self.right_arrow = ArrowButton(text=">", on_press=self.Dalej,
                                       pos_hint={"top": 1, "right": 1})
        self.add_widget(self.left_arrow)
        self.add_widget(self.right_arrow)

        self.today = datetime.date.today()
        self.zobaczmy = str(calendar.month_name[self.today.month]) + ", " + str(self.today.year)
        self.ZmianaAktywnosci()


    def on_pre_enter(self, *args): #ZMIENIC NA GLOBALNA FLAGA == 1
        self.ZmienKalendarz(self.today) #Zeby robilo sie tylko po wpisie


    def WpisDzis(self): #Wpis dzisiaj
        global dzis
        global edit
        edit = 1
        dzis = datetime.date.today()
        global d
        d = str(dzis.day) + "/" + str(dzis.month) + "/" + str(dzis.year)
        self.manager.current = "7"

        try:
            self.lis = list(store["aktywnosci"])
            print(slowniczek)
            for i in list(store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)]):  # Idziemy po aktywnosciach
                if i != "dzien":  # Triggerujemy wszystkie aktywnosci oprocz dnia
                    a = self.lis.index(str(i))
                    slowniczek[str(store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)][str(i)]["ocena"]) + "P.png" + str(a)].trigger_action(0)
                    try:
                        slowniczek["text" + str(a)].text = str(store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)][str(i)]["komentarz"])
                        store["tymczasowe"][str(i)]["komentarz"] = str(store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)][str(i)]["komentarz"])
                    except:
                        pass
            slowniczek[str(store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)]["dzien"]["ocena"]) + "P.png" + str(len(self.lis))].trigger_action(0)  # Triggerujemy dzien
            slowniczek["text" + str(len(self.lis))].text = str(store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)]["dzien"]["komentarz"])
            try:
                store["tymczasowe"]["dzien"]["komentarz"] = str(store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)]["dzien"]["komentarz"])
            except:
                pass
        except:
            pass

    def WpisWczoraj(self):
        global edit
        edit = 1
        global dzis
        dzis = datetime.date.today() - relativedelta(days=1)
        global d
        d = str(dzis.day) + "/" + str(dzis.month) + "/" + str(dzis.year)

        self.manager.current = "7"

        try:
            self.lis = list(store["aktywnosci"])
            print(slowniczek)
            for i in list(store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)]):  # Idziemy po aktywnosciach
                if i != "dzien":  # Triggerujemy wszystkie aktywnosci oprocz dnia
                    a = self.lis.index(str(i))
                    slowniczek[str(store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)][str(i)]["ocena"]) + "P.png" + str(a)].trigger_action(0)
                    try:
                        slowniczek["text" + str(a)].text = str(store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)][str(i)]["komentarz"])
                        store["tymczasowe"][str(i)]["komentarz"] = str(
                            store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)][str(i)]["komentarz"])
                    except:
                        pass
            slowniczek[str(store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)]["dzien"]["ocena"]) + "P.png" + str(len(self.lis))].trigger_action(0)  # Triggerujemy dzien
            slowniczek["text" + str(len(self.lis))].text = str(store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)]["dzien"]["komentarz"])
            try:
                store["tymczasowe"]["dzien"]["komentarz"] = str(
                    store["daty"][str(dzis.year)][str(dzis.month)][str(dzis.day)]["dzien"]["komentarz"])
            except:
                pass
        except:
            pass
    def ZmianaAktywnosci(self): #Generuje Spinnera
        try:
            self.b = list(store["aktywnosci"])
            self.value = []
            self.value.append("Oceny dnia")
            for i in self.b:
                self.value.append("Oceny " + str(i))
            self.spin = Spin(text = "Oceny Dnia", values = self.value, size_hint = (None,None), size = (Window.width/2,Window.height/22), pos_hint={'center_x': .5, 'top': 0.91})
            self.spin.option_cls = SpinnerOptions
            self.spin.bind(text = self.KlikKalendarz)
            self.add_widget(self.spin)
        except Exception as e:
            print(e, "ZMIANAKALENDARZA")

    def Generuj(self): #Tworzy 42 widgety, aby potem je tylko zmieniac
        self.sl = {}
        #czas = time.time()
        for i in range(1, 43):
            self.kolko = Kolko()
            self.sl[str(i)] = self.kolko
        #print(time.time() - czas, "GENERUJ KALENDARZ")

    def ZmienKalendarz(self, data):
        #czas = time.time()

        self.kal.clear_widgets()
        global dzis #Srednio potrzebne, ale niech zostanie
        dzis = data

        zakres_biezacy = calendar.monthrange(dzis.year, dzis.month)
        if dzis.month == 1: #Tworzymy zakresy miesięcy
            zakres_wczesniejszy = calendar.monthrange(dzis.year - 1, 12)
            zakres_pozniejszy = calendar.monthrange(dzis.year, dzis.month + 1)
        elif dzis.month == 12:
            zakres_wczesniejszy = calendar.monthrange(dzis.year, dzis.month - 1)
            zakres_pozniejszy = calendar.monthrange(dzis.year + 1, 1)
        else:
            zakres_wczesniejszy = calendar.monthrange(dzis.year, dzis.month - 1)
            zakres_pozniejszy = calendar.monthrange(dzis.year, dzis.month + 1)

        for i in range(1,math.ceil((zakres_biezacy[0] + zakres_biezacy[1]) / 7) * 7 + 1):

            if i in range(zakres_biezacy[0] + 1): #Tworzymy dni PRZED miesiącem
                self.b = self.sl[str(i)]
                self.b.la.text = str(zakres_wczesniejszy[1] - zakres_biezacy[0] + i)
                self.b.la.color = (128 / 255, 128 / 255, 128 / 255, 1)
                self.b.t = (0,0,0,0)
                try:
                    self.b.unbind(on_press = self.press)
                except:
                    pass
                self.kal.add_widget(self.b)

            elif i >= zakres_biezacy[0] + zakres_biezacy[1] + 1: #Tworzymy dni PO miesiącu
                self.b = self.sl[str(i)]
                self.b.la.text = str(i - zakres_biezacy[1] - zakres_biezacy[0])
                self.b.la.color = (128 / 255, 128 / 255, 128 / 255, 1)
                self.b.t = (0, 0, 0, 0)
                try:
                    self.b.unbind(on_press = self.press)
                except:
                    pass
                self.kal.add_widget(self.b)
            else: #Tworzymy wlasciwy miesiac

                self.b = self.sl[str(i)]
                self.b.bind(on_press = self.press)
                self.b.la.text = str(i - zakres_biezacy[0])
                self.b.la.color = (1,1,1,1)
                self.b.t = (0, 0, 0, 0)

                if dzis.year == datetime.date.today().year and dzis.month == datetime.date.today().month and self.b.la.text == str(datetime.date.today().day):
                    #Aktualny dzien bedzie na czerwono
                    self.b.la.color = (1, 0, 0, 1)
                    self.b.la.bold = True
                if self.flaga == 0: #flaga = 0 oznacza, że chcemy oceny z DNIA, konkretniej kolory
                    try:
                        if int(store["daty"][str(dzis.year)][str(dzis.month)][str(self.b.la.text)]["dzien"][
                                   "ocena"]) in range(1, 3):
                            self.b.t = (120 / 255, 144 / 255, 156 / 255, 1)
                        elif int(store["daty"][str(dzis.year)][str(dzis.month)][str(self.b.la.text)]["dzien"][
                                     "ocena"]) in range(3, 5):
                            self.b.t = (69 / 255, 99 / 255, 137 / 255, 1)
                        elif int(store["daty"][str(dzis.year)][str(dzis.month)][str(self.b.la.text)]["dzien"][
                                     "ocena"]) in range(5, 7):
                            self.b.t = (119 / 255, 71 / 255, 131 / 255, 1)
                        elif int(store["daty"][str(dzis.year)][str(dzis.month)][str(self.b.la.text)]["dzien"][
                                     "ocena"]) in range(7, 9):
                            self.b.t = (53 / 255, 138 / 255, 83 / 255, 1)
                        elif int(store["daty"][str(dzis.year)][str(dzis.month)][str(self.b.la.text)]["dzien"][
                                     "ocena"]) in range(9, 11):
                            self.b.t = (203 / 255, 155 / 255, 25 / 255, 1)
                    except:
                        pass
                else: #To do aktywności
                    try:
                        if int(store["daty"][str(dzis.year)][str(dzis.month)][str(self.b.la.text)][str(self.flaga)][
                                   "ocena"]) in range(1, 3):
                            self.b.t = (120 / 255, 144 / 255, 156 / 255, 1)
                        elif int(store["daty"][str(dzis.year)][str(dzis.month)][str(self.b.la.text)][str(self.flaga)][
                                     "ocena"]) in range(3, 5):
                            self.b.t = (69 / 255, 99 / 255, 137 / 255, 1)

                        elif int(store["daty"][str(dzis.year)][str(dzis.month)][str(self.b.la.text)][str(self.flaga)][
                                     "ocena"]) in range(5, 7):
                            self.b.t = (119 / 255, 71 / 255, 131 / 255, 1)
                        elif int(store["daty"][str(dzis.year)][str(dzis.month)][str(self.b.la.text)][str(self.flaga)][
                                     "ocena"]) in range(7, 9):
                            self.b.t = (53 / 255, 138 / 255, 83 / 255, 1)
                        elif int(store["daty"][str(dzis.year)][str(dzis.month)][str(self.b.la.text)][str(self.flaga)][
                                     "ocena"]) in range(9, 11):
                            self.b.t = (203 / 255, 155 / 255, 25 / 255, 1)
                    except:
                        pass
                self.kal.add_widget(self.b)
        #print(time.time() - czas, "ZMIANA KALENDARZ")

    def KlikKalendarz(self, el, text): #Zmiana między aktywnosciami
        if text.split(" ")[1] == "dnia":
            self.flaga = 0
        else:
            self.flaga = text.split(" ")[1]
        self.ZmienKalendarz(self.today)

    def Dalej(self, ccos): #strzalka dalej
        self.ZmienKalendarz(self.today + relativedelta(months=1))
        self.today = self.today + relativedelta(months=1)
        self.zobaczmy = str(calendar.month_name[dzis.month]) + ", " + str(dzis.year)

    def Cofnij(self, JD): #strzalka wstecz
        self.ZmienKalendarz(self.today - relativedelta(months=1))
        self.today = self.today - relativedelta(months=1)
        self.zobaczmy = str(calendar.month_name[dzis.month]) + ", " + str(dzis.year)

    def press(self, el): #Kliknięcie na przycisk w kalendarzu
        global dzien
        dzien = el
        self.manager.current = "6"

#Statystyki
class S3(Screen):
    #@@@@@@@@@@@@@@@@@@ DODAC ZEBY W PRE ENTERZE SIE AKTUALIZOWAL PO WPISIE
    jeden = StringProperty()
    dwa = StringProperty()
    trzy = StringProperty()
    cztery = StringProperty()
    piec = StringProperty()
    czas1 = StringProperty()
    czas2 = StringProperty()
    czas3 = StringProperty()
    mies = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            a,b,c,d = ZnajdzMinMax()
            self.today = datetime.date(c,d,1)
        except:
            self.today = datetime.date.today()

        self.slownik = {}
        self.strzalka = None
        global wykres
        wykres = 0

        self.NastrojeINIT(self.today.year, self.today.month)
        self.BarINIT(self.today.year, self.today.month, "dzien")
        self.Pasek(self.today.year, self.today.month, "dzien")
        self.Stworz(self.today.year, self.today.month,4)


        self.left_arrow = ArrowButton(text="<", on_press=self.Cof,
                                      pos_hint={"top": 1, "left": 0})

        self.right_arrow = ArrowButton(text=">", on_press=self.Nast,
                                       pos_hint={"top": 1, "right": 1})

        self.add_widget(self.left_arrow)

        self.add_widget(self.right_arrow)

        self.mies = str(calendar.month_name[self.today.month]) + ", " + str(self.today.year)  # Label górny

        try:
            self.b = list(store["aktywnosci"])
        except:
            self.b = []
        self.value = []
        self.value.append("Oceny dnia")

        for i in self.b:
            self.value.append("Oceny " + str(i))

        self.spin = Spin(text="Oceny Dnia", values=self.value, size_hint=(None, None),
                            size=(Window.width / 2, Window.height / 18), pos_hint= {"center_x": 0.5})
        self.spin.option_cls = SpinnerOptions
        self.spin.bind(text = self.NastrojeZMIANA)
        self.box.add_widget(self.spin)

        self.spin2 = Spin(text="Oceny Dnia", values=self.value, size_hint=(None, None),
                            size=(Window.width / 2, Window.height / 18), pos_hint= {"center_x": 0.5})
        self.spin2.option_cls = SpinnerOptions
        self.spin2.bind(text = self.BarZMIANA)
        self.box2.add_widget(self.spin2)

        self.spin3 = Spin(text="Oceny Dnia", values=self.value, size_hint=(None, None),
                            size=(Window.width / 2, Window.height / 18), pos_hint= {"center_x": 0.5})
        self.spin3.option_cls = SpinnerOptions
        self.spin3.bind(text = self.PasekZmiana)
        self.box3.add_widget(self.spin3)

    def on_pre_enter(self, *args):
        self.b = list(store["aktywnosci"])
        self.value = []
        self.value.append("Oceny dnia")
        for i in self.b:
            self.value.append("Oceny " + str(i))
        self.spin.values = self.value
        self.spin2.values = self.value
        self.spin3.values = self.value

        try:
            a, b, c, d = ZnajdzMinMax()
        except:
            a = today.year
            b = today.month
            c = today.year
            d = today.month

        if (self.today - relativedelta(months=1)).year <= a and (self.today - relativedelta(months=1)).month < b or ((self.today).year == a and (self.today).month == b):
            self.left_arrow.bold = False
            self.left_arrow.disabled = True
            self.strzalka = self.left_arrow
        else:
            self.left_arrow.bold = True
            self.left_arrow.disabled = False

        if ((self.today + relativedelta(months=1)).year >= c and (self.today + relativedelta(months=1)).month > d) or ((self.today).year == c and (self.today).month == d):
            self.right_arrow.bold = False
            self.right_arrow.disabled = True
            self.strzalka = self.right_arrow
        else:
            self.right_arrow.bold = True
            self.right_arrow.disabled = False

        global wykres

        if wykres == 1:
            self.NastrojeZMIEN(self.today.year, self.today.month, "dzien")
            self.BarINIT(self.today.year, self.today.month, "dzien")
            self.Pasek(self.today.year, self.today.month, "dzien")
            self.Stworz(self.today.year, self.today.month, 4)
            self.spin.text = "Oceny Dnia"
            self.spin2.text = "Oceny Dnia"
            self.spin3.text = "Oceny Dnia"
            wykres = 0

    def Cof(self, el):
        self.today = self.today - relativedelta(months=1)
        self.mies = str(calendar.month_name[self.today.month]) + ", " + str(self.today.year)
        self.NastrojeZMIEN(self.today.year, self.today.month, "dzien")
        self.BarINIT(self.today.year, self.today.month, "dzien")
        self.Pasek(self.today.year, self.today.month, "dzien")
        self.Stworz(self.today.year, self.today.month, 4)
        self.spin.text = "Oceny Dnia"
        self.spin2.text = "Oceny Dnia"
        self.spin3.text = "Oceny Dnia"
        self.gl.background_normal = "happyP.png"

        try:  # zapamiętana strzalka, zeby móc cofać disable
            self.strzalka.bold = True
            self.strzalka.disabled = False
            self.strzalka = None
        except:
            pass
        a, b, c, d = ZnajdzMinMax()
        if (self.today - relativedelta(months=1)).year <= a and (self.today - relativedelta(months=1)).month < b or ((self.today).year == a and (self.today).month == b):
            self.strzalka = el
            el.bold = False
            el.disabled = True

    def Nast(self, el): #Klik do strzalki prawej, zmienia miesiąc
        self.today = self.today + relativedelta(months=1)
        self.mies = str(calendar.month_name[self.today.month]) + ", " + str(self.today.year)
        self.NastrojeZMIEN(self.today.year, self.today.month, "dzien")
        self.BarINIT(self.today.year, self.today.month, "dzien")
        self.Pasek(self.today.year, self.today.month, "dzien")
        self.Stworz(self.today.year, self.today.month, 4)
        self.spin.text = "Oceny Dnia"
        self.spin2.text = "Oceny Dnia"
        self.spin3.text = "Oceny Dnia"
        self.gl.background_normal = "happyP.png"

        try: #zapamiętana strzalka, zeby móc cofać disable
            self.strzalka.bold = True
            self.strzalka.disabled = False
            self.strzalka = None
        except:
            pass
        a,b,c,d = ZnajdzMinMax()
        if ((self.today + relativedelta(months=1)).year >= c and (self.today + relativedelta(months=1)).month > d) or ((self.today).year == c and (self.today).month == d):
            self.strzalka = el
            el.bold = False
            el.disabled = True

    def NastrojeINIT(self, rok, miesiac):
        czas = time.time()
        try:
            self.iksy = []
            self.igreki = []

            for i in sorted(list(map(int, list(store["daty"][str(rok)][str(miesiac)])))):
                try:
                    self.igreki.append(int(store["daty"][str(rok)][str(miesiac)][str(i)]["dzien"]["ocena"]))
                    self.iksy.append(int(i))
                except Exception as e:
                    print(e)

            fig, ax = plt.subplots(figsize=(8.5, 5)) # Tworzymy baze pod wykresy
            plt.tight_layout() #Żeby figsize był mniejszy


            ax.tick_params(axis='x', colors='white', labelsize= sp(11)) #Zmieniamy wielkość iksów i igreków
            ax.tick_params(axis='y', colors='white', labelsize= sp(11))

            #ax.spines['top'].set_color('white')
            #ax.spines['bottom'].set_color('white')
            #ax.spines['left'].set_color('white')
            #ax.spines['right'].set_color('white')

            ax.spines['right'].set_visible(False) #Wywalamy wszystkie osie
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)

            ax.axhline(0, color=(1,1,1 ,1), linewidth=2) #Linie na y
            ax.axhline(2, color=(120 / 255, 144 / 255, 156 / 255, 1), linewidth=1)
            ax.axhline(4, color=(69 / 255, 99 / 255, 137 / 255, 1), linewidth=1)
            ax.axhline(6, color=(119 / 255, 71 / 255, 131 / 255, 1), linewidth=1)
            ax.axhline(8, color=(53 / 255, 138 / 255, 83 / 255, 1), linewidth=1)
            ax.axhline(10, color=(203 / 255, 155 / 255, 25 / 255, 1), linewidth=1)

            ax.set_xlim([-1.5, self.iksy[-1] + 1]) #Granice iksow i igrekow
            ax.set_ylim([0, 10.5])

            yticks = ax.yaxis.get_major_ticks() #Zgarniamy wszystkie iksy i igreki
            xticks = ax.xaxis.get_major_ticks()

            fig.patch.set_alpha(0)
            ax.patch.set_alpha(0)

            if self.iksy[-1] + 1 < 10:
                liczba = 1
            elif self.iksy[-1] + 1 in range(10, 20):
                liczba = 2
            elif self.iksy[-1] + 1 > 20:
                liczba = 3

            plt.yticks(np.arange(2, 12, 2))
            plt.xticks(np.arange(1, self.iksy[-1] + 1, liczba))

            X = []
            Y = []
            X.append(self.iksy[0])
            Y.append(self.igreki[0])
            #Malujemy pierwsze markery
            rects = ax.plot(self.iksy[0], self.igreki[0], "o", markerfacecolor=self.klasyk(self.igreki[0]), markersize=Window.height/125, zorder=2, markeredgecolor = self.klasyk(self.igreki[0]), clip_on = True)
            for i in range(1, len(self.iksy)):

                rects = ax.plot(self.iksy[i], self.igreki[i], "o", markerfacecolor= self.klasyk(self.igreki[i]), markersize=Window.height/125, zorder=2, markeredgecolor = self.klasyk(self.igreki[i]), clip_on = True)

                if self.sprawdzamy(self.iksy, self.igreki, i) == 1:
                    X.append(self.iksy[i])
                    Y.append((self.igreki[i]))
                else:
                    rects = ax.plot(X, Y, linewidth= 4, color=self.klasyk(self.igreki[i-1]), zorder=1)
                    Y = []
                    X = []
                    if math.fabs(self.iksy[i - 1] - self.iksy[i]) == 1:
                        X.append(self.iksy[i-1])
                        Y.append((self.igreki[i-1]))

                    X.append(self.iksy[i])
                    Y.append((self.igreki[i]))
            try:
                rects = ax.plot(X, Y, '-', linewidth=4, color=self.klasyk(self.igreki[i-1]), zorder=1)
            except:
                pass

            canvas = FigureCanvasKivyAgg(figure=plt.gcf())
            self.liniowy.add_widget(canvas)
            #Zapamiętujemy na potem
            self.slownik["fig"] = fig
            self.slownik["ax"] = ax
            self.slownik["canvas"] = canvas
            self.czas = str(time.time() - czas)
            print(time.time() - czas, "WYKRES LINIOWY")
        except Exception as e:
            print(e, "LINIOWY INIT")

    def NastrojeZMIEN(self, rok, miesiac, akt): #Zmienia wykres na inna aktywnosc
        czas = time.time()

        try:
            try:
                self.liniowy.remove_widget(self.slownik["canvas"])
                self.slownik["ax"].cla()
            except:
                pass
            self.iksy = []
            self.igreki = []

            for i in sorted(list(map(int, list(store["daty"][str(rok)][str(miesiac)])))):
                try:
                    self.igreki.append(int(store["daty"][str(rok)][str(miesiac)][str(i)][str(akt)]["ocena"]))
                    self.iksy.append(int(i))
                except Exception as e:
                    #print(e, "NASTROJEZMIEN")
                    pass



            fig, ax = plt.subplots(figsize=(8.5, 5)) #To jest do zmiany nie


            plt.tight_layout() #to trzeba zeby bylo bez tego



            ax.tick_params(axis='x', colors='white', labelsize=sp(11))
            ax.tick_params(axis='y', colors='white', labelsize=sp(11))

            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.axhline(0, color=(1,1,1 ,1), linewidth=2) #Linie na y
            ax.axhline(2, color=(120 / 255, 144 / 255, 156 / 255, 1), linewidth=1)
            ax.axhline(4, color=(69 / 255, 99 / 255, 137 / 255, 1), linewidth=1)
            ax.axhline(6, color=(119 / 255, 71 / 255, 131 / 255, 1), linewidth=1)
            ax.axhline(8, color=(53 / 255, 138 / 255, 83 / 255, 1), linewidth=1)
            ax.axhline(10, color=(203 / 255, 155 / 255, 25 / 255, 1), linewidth=1)
            ax.set_xlim([-1.5, self.iksy[-1] + 1])
            ax.set_ylim([0, 10.5])
            yticks = ax.yaxis.get_major_ticks()
            xticks = ax.xaxis.get_major_ticks()

            fig.patch.set_alpha(0)
            ax.patch.set_alpha(0)
            if self.iksy[-1] + 1 < 10:
                liczba = 1
            elif self.iksy[-1] + 1 in range(10, 20):
                liczba = 2
            elif self.iksy[-1] + 1 > 20:
                liczba = 3

            plt.yticks(np.arange(2, 12, 2))
            plt.xticks(np.arange(1, self.iksy[-1] + 1, liczba))

            X = []
            Y = []
            X.append(self.iksy[0])
            Y.append(self.igreki[0])

            rects = ax.plot(self.iksy[0], self.igreki[0], "o", markerfacecolor=self.klasyk(self.igreki[0]), markersize=Window.height/125,
                            zorder=2, markeredgecolor=self.klasyk(self.igreki[0]), clip_on=True)
            for i in range(1, len(self.iksy)):

                rects = ax.plot(self.iksy[i], self.igreki[i], "o", markerfacecolor=self.klasyk(self.igreki[i]),
                                markersize=Window.height/125, zorder=2, markeredgecolor=self.klasyk(self.igreki[i]), clip_on=True)

                if self.sprawdzamy(self.iksy, self.igreki, i) == 1:
                    X.append(self.iksy[i])
                    Y.append((self.igreki[i]))
                else:
                    rects = ax.plot(X, Y, linewidth=4, color=self.klasyk(self.igreki[i - 1]), zorder=1)
                    Y = []
                    X = []
                    if math.fabs(self.iksy[i - 1] - self.iksy[i]) == 1:
                        X.append(self.iksy[i - 1])
                        Y.append((self.igreki[i - 1]))

                    X.append(self.iksy[i])
                    Y.append((self.igreki[i]))
            try:
                rects = ax.plot(X, Y, '-', linewidth=4, color=self.klasyk(self.igreki[i - 1]), zorder=1)
            except:
                pass

            canvas = FigureCanvasKivyAgg(figure=plt.gcf())
            self.liniowy.add_widget(canvas)
            self.slownik["fig"] = fig
            self.slownik["ax"] = ax
            self.slownik["canvas"] = canvas
            self.czas = str(time.time() - czas)
            #print(time.time() - czas, "WYKRES LINIOWY TYPU ZMIENIONY")
        except Exception as e:
            print(e, "Liniowy ZMIEN")
            pass


    def NastrojeZMIANA(self, el, text):

        if text.split(" ")[1] == "Dnia":
            return
        if text.split(" ")[1] == "dnia":
            self.NastrojeZMIEN(self.today.year, self.today.month, "dzien")
        else:
            self.NastrojeZMIEN(self.today.year, self.today.month, str(text.split(" ")[1]))


    def BarINIT(self, rok, miesiac, akt): #poprawic zeby uzywal starego wykresu(Nie da sie raczej eh)
        czas = time.time()
        try:
            try:
                self.bar.remove_widget(self.slownik["bar"])
            except:
                pass
            ss = {}
            for i in calendar.day_name:
                ss[str(i)] = []
            for i in sorted(list(map(int, list(store["daty"][str(rok)][str(miesiac)])))):
                try:
                    ss[str(calendar.day_name[int(datetime.date(int(rok), int(miesiac), int(i)).weekday())])].append(int(store["daty"][str(rok)][str(miesiac)][str(i)][str(akt)]["ocena"]))
                except Exception as e:
                    #print(e)
                    pass

            for i in list(ss):
                suma = 0
                for j in ss[str(i)]:
                    suma += j
                try:
                    suma = suma/len(ss[str(i)])
                except:
                    pass
                ss[str(i)] = suma
            x = []
            for i in list(ss):
                x.append(i[0:2])

            fig, ax = plt.subplots(figsize=(8.5, 4.5))
            plt.tight_layout()

            igreki = list(ss.values())

            ax.bar(x, igreki, color=(self.klasyk(math.ceil(igreki[0])), self.klasyk(math.ceil(igreki[1])), self.klasyk(math.ceil(igreki[2])),self.klasyk(math.ceil(igreki[3])) ,self.klasyk(math.ceil(igreki[4])) ,self.klasyk(math.ceil(igreki[5])), self.klasyk(math.ceil(igreki[6])) ))
            ax.set_ylim([0, 10.5])
            fig.patch.set_alpha(0)
            ax.patch.set_alpha(0)

            plt.yticks(np.arange(2, 12, 2))


            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)

            ax.spines['left'].set_visible(False)

            ax.spines['bottom'].set_color('white')


            ax.axhline(2, color=(120 / 255, 144 / 255, 156 / 255, 1), linewidth=1)
            ax.axhline(4, color=(69 / 255, 99 / 255, 137 / 255, 1), linewidth=1)
            ax.axhline(6, color=(119 / 255, 71 / 255, 131 / 255, 1), linewidth=1)
            ax.axhline(8, color=(53 / 255, 138 / 255, 83 / 255, 1), linewidth=1)
            ax.axhline(10, color=(203 / 255, 155 / 255, 25 / 255, 1), linewidth=1)

            ax.tick_params(axis='x', colors='white', labelsize=sp(9))
            ax.tick_params(axis='y', colors='white', labelsize=sp(9))



            canvas = FigureCanvasKivyAgg(figure=plt.gcf())
            self.bar.add_widget(canvas)
            self.slownik["bar"] = canvas
            self.czas2 = str(time.time() - czas)

        except:
            pass

    def BarZMIANA(self, el, text):
        if text.split(" ")[1] == "Dnia":
            return
        if text.split(" ")[1] == "dnia":
            self.BarINIT(self.today.year, self.today.month, "dzien")
        else:
            self.BarINIT(self.today.year, self.today.month, str(text.split(" ")[1]))


    def Pasek(self,rok ,miesiac, akt):
        try:
            try:
                self.pas.remove_widget(self.slownik["pasek"])
            except:
                pass
            czas = time.time()
            slowniczek = {}
            for i in range(1,6):
                slowniczek[str(i)] = 0
            for i in sorted(list(map(int, list(store["daty"][str(rok)][str(miesiac)])))):
                try:
                    slowniczek[str(self.klasyk2(int(store["daty"][str(rok)][str(miesiac)][str(i)][str(akt)]["ocena"])))] += 1
                except:
                    pass
            start = 0
            suma = 0
            for i in list(slowniczek):
                suma += slowniczek[str(i)]
            fig, ax = plt.subplots(figsize=(7, 3))
            ax.set_ylim(0, 1)
            ax.set_xlim(0, suma)
            ax.broken_barh([(start, slowniczek["1"]), (slowniczek["1"], slowniczek["1"] + slowniczek["2"]), (slowniczek["1"] + slowniczek["2"], slowniczek["1"] + slowniczek["2"] + slowniczek["3"]), (slowniczek["1"] + slowniczek["2"] + slowniczek["3"], slowniczek["1"] + slowniczek["2"] + slowniczek["3"] + slowniczek["4"]), (slowniczek["1"] + slowniczek["2"] + slowniczek["3"] + slowniczek["4"], slowniczek["1"] + slowniczek["2"] + slowniczek["3"] + slowniczek["4"] + slowniczek["5"])], [0, 1],
                           facecolors=((120 / 255, 144 / 255, 156 / 255, 1), (69 / 255, 99 / 255, 137 / 255, 1), (119 / 255, 71 / 255, 131 / 255, 1),(53 / 255, 138 / 255, 83 / 255, 1), (203 / 255, 155 / 255, 25 / 255, 1)))
            ax.text(slowniczek["1"]/3, 0.5, str(round(100*slowniczek["1"]/suma, 1)) + "%", fontsize=sp(8))
            ax.text(((slowniczek["1"] + slowniczek["2"]/3)), 0.5, str(round(100*slowniczek["2"]/suma,1))+ "%", fontsize=sp(8))
            ax.text(((slowniczek["1"] + slowniczek["2"] + slowniczek["3"]/3)), 0.5, str(round(100*slowniczek["3"]/suma,1))+ "%", fontsize=sp(8))
            ax.text(((slowniczek["1"] + slowniczek["2"] + slowniczek["3"] + slowniczek["4"]/ 3)), 0.5, str(round(100*slowniczek["4"]/suma,1))+ "%", fontsize=sp(8))
            ax.text(((slowniczek["1"] + slowniczek["2"] + slowniczek["3"] + slowniczek["4"] + slowniczek["5"]/ 3)), 0.5, str(round(100*slowniczek["5"]/suma,1))+ "%", fontsize=sp(8))



            ax.tick_params(axis='x', colors='white', labelsize=sp(11))
            ax.tick_params(axis='y', colors='white', labelsize=sp(11))


            self.jeden = str(slowniczek["1"])
            self.dwa = str(slowniczek["2"])
            self.trzy = str(slowniczek["3"])
            self.cztery =str(slowniczek["4"])
            self.piec = str(slowniczek["5"])

            ax.set_xticks([])
            ax.set_yticks([])

            fig.patch.set_alpha(0)
            ax.patch.set_alpha(0)

            plt.tight_layout()


            canvas = FigureCanvasKivyAgg(figure=plt.gcf())
            self.pas.add_widget(canvas)
            #print(time.time() - czas, "PASEK")
            self.slownik["pasek"] = canvas
            self.czas3 = str(time.time() - czas)
        except:
            pass

    def PasekZmiana(self, el, text):
        if text.split(" ")[1] == "Dnia":
            return
        if text.split(" ")[1] == "dnia":
            self.Pasek(self.today.year, self.today.month,"dzien")
        else:
            self.Pasek(self.today.year, self.today.month, str(text.split(" ")[1]))


    def Stworz(self, rok ,miesiac, numerek):
        try:
            try:
                self.labs.clear_widgets()
                self.emotes.clear_widgets()
            except:
                pass

            slownik = {}
            lista = list(store["aktywnosci"])
            for i in range(1,6):
                slownik[str(i)] = {}
                for j in lista:
                    slownik[str(i)][str(j)] = []

            for i in sorted(list(map(int, list(store["daty"][str(rok)][str(miesiac)])))):
                try:
                    flaga = self.klasyk2(int(store["daty"][str(rok)][str(miesiac)][str(i)]["dzien"]["ocena"]))
                    for j in list(slownik[str(flaga)]):
                        try:
                            slownik[str(flaga)][str(j)].append(int(store["daty"][str(rok)][str(miesiac)][str(i)][str(j)]["ocena"]))
                        except:
                            pass
                except:
                    pass
            #print(slownik)
            for i in list(slownik):

                for j in list(slownik[str(i)]):

                    max = 0
                    dalej = []
                    for k in list(set(slownik[str(i)][str(j)])):  # unikalne zeby szybciej hehehe

                        if slownik[str(i)][str(j)].count(k) == max:
                            max = slownik[str(i)][str(j)].count(k)
                            dalej.append(k)
                        elif slownik[str(i)][str(j)].count(k) > max:
                            max = slownik[str(i)][str(j)].count(k)
                            dalej = []
                            dalej.append(k)


                    slownik[str(i)][str(j)] = dalej

            for i in list(slownik[str(numerek)]):
                self.l = Lab(text = str(i))
                self.labs.add_widget(self.l)

                self.g = Grid3()
                for j in slownik[str(numerek)][str(i)]:
                    self.i = Image(source = f"{j}P.png")
                    self.g.add_widget(self.i)
                if len(slownik[str(numerek)][str(i)]) == 0:
                    self.w = Widget()
                    self.g.add_widget(self.w)

                self.emotes.add_widget(self.g)
        except:
            pass


    def sprawdzamy(self,x,y,i): # Chcemy sprawdzic czy x i y nalezą do tej samej emotki

        if math.fabs(x[i - 1] - x[i]) == 1:  # sprawdzamy czy jest ciągłość
            if math.fabs(y[i - 1] - y[i]) == 1:  # muszą się różnic o 1 zeby byc z tego samego przedzialu
                if y[i - 1] % 2 == 0: # sprawdzamy parzystosc
                    if y[i - 1] > y[i]: # jezeli jest parzysta to musi byc mniejsza, bo to koniec przedzialu
                        return 1
                    else:
                        return 0
                else:
                    if y[i - 1] < y[i]: # tu odwrotnie
                        return 1
                    else:
                        return 0
            if y[i] == y[i-1]:
                return 1

    def klasyk(self, w): #Zwraca kolor w zaleznosci od wartosci
        if w in range(0, 3):
            return (120 / 255, 144 / 255, 156 / 255, 1)
        elif w in range(3, 5):
            return  (69 / 255, 99 / 255, 137 / 255, 1)
        elif w in range(5, 7):
            return (119 / 255, 71 / 255, 131 / 255, 1)
        elif w in range(7, 9):
            return (53 / 255, 138 / 255, 83 / 255, 1)
        elif w in range(9, 11):
            return (203 / 255, 155 / 255, 25 / 255, 1)

    def klasyk2(self, w): #Zwraca indeks minki
        if w in range(0, 3):
            return 1
        elif w in range(3, 5):
            return  2
        elif w in range(5, 7):
            return 3
        elif w in range(7, 9):
            return 4
        elif w in range(9, 11):
            return 5



#Ustawienia
class S4(Screen):
    pass

#Ustawienia Aktywności
class S5(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flaga = 0 # Flaga do stworzenia na nowo Pustych Wpisów
        try:
            for i in list(store["aktywnosci"]):
                self.b = Aktywa()
                self.b.textt  = str(i)
                self.aktyw.add_widget(self.b)
        except Exception as e:
            print(e, "USTAWIENIA AKTYWNOSCI1")

        try:
            for i in list(store["archiwizowane"]):
                if i != "daty":
                    self.b = Archiwa()
                    self.b.textt = str(i)
                    self.arch.add_widget(self.b)
        except Exception as e:
            print(e, "USTAWIENIA AKTYWNOSCI2")

    def on_leave(self, *args):
        if self.flaga == 1:
            Clock.schedule_once(self.on_leavePOM, 0.2)
            self.flaga = 0

    def on_leavePOM(self, czas):
        sm.get_screen("1").StworzPuste()

    def dodaj(self): #Dodaje aktywnosc do store
        try:
            store.get("aktywnosci")
        except:
            store["aktywnosci"] = {}
        try:
            store.get("archiwizowane")
        except:
            store["archiwizowane"] = {}

        if self.text.text != "" and self.text.text not in list(store["aktywnosci"]) and self.text.text not in list(store["archiwizowane"]):
            store["aktywnosci"][str(self.text.text)] = {}
            store["aktywnosci"] = store["aktywnosci"]
            self.b = Aktywa()
            self.b.textt = str(self.text.text)
            self.aktyw.add_widget(self.b)
            self.text.text = ""
        if self.text.text in list(store["aktywnosci"]) or self.text.text in list(store["archiwizowane"]):
            self.l = Label(text = "Istnieje już taka aktywność", size_hint = (1,None), font_size = sp(20), pos_hint = {"top": 0.72})
            self.add_widget(self.l)
            Clock.schedule_once(self.dodajPom, 1.75)
        self.flaga = 1

    def dodajPom(self, el): #usuwa labela po czasie
        self.remove_widget(self.l)

    def UsunAkt(self, el): #Usuwa Aktywnosc
        self.pom = el
        self.content = BoxLayout()
        self.popup = Popup(title='Czy na pewno chcesz usunąć ' + str(self.pom.textt) + "?",
                           content=self.content,
                           size_hint=(None, None), size=(Window.width / 1.5, Window.height / 6))
        self.b1 = Button(text="Tak")
        self.b2 = Button(text="Nie")
        self.b1.bind(on_press=self.UsunAktPom)
        self.b2.bind(on_press=self.popup.dismiss)
        self.content.add_widget(self.b1)
        self.content.add_widget(self.b2)
        self.popup.open()


    def UsunAktPom(self, el):
        self.aktyw.remove_widget(self.pom)
        del store["aktywnosci"][str(self.pom.textt)]
        try:
            for i in list(store["daty"]):
                for j in list(store["daty"][str(i)]):
                    for k in list(store["daty"][str(i)][str(j)]):
                        try:
                            del store["daty"][str(i)][str(j)][str(k)][str(self.pom.textt)]
                        except:
                            pass
            store["daty"] = store["daty"]
        except:
            pass
        store["aktywnosci"] = store["aktywnosci"]
        self.popup.dismiss()
        self.flaga = 1

    def UsunArch(self, el): #Usuwa archiwum
        self.pom = el
        self.content = BoxLayout()
        self.popup = Popup(title='Czy na pewno chcesz usunąć ' + str(self.pom.textt) + "?",
                           content=self.content,
                           size_hint=(None, None), size=(Window.width / 1.5, Window.height / 6))
        self.b1 = Button(text="Tak")
        self.b2 = Button(text="Nie")
        self.b1.bind(on_press=self.UsunArchPom)
        self.b2.bind(on_press=self.popup.dismiss)
        self.content.add_widget(self.b1)
        self.content.add_widget(self.b2)
        self.popup.open()

    def UsunArchPom(self, el):
        self.arch.remove_widget(self.pom)
        del store["archiwizowane"][str(self.pom.textt)]
        try:
            for i in list(store["archiwizowane"]["daty"]):
                for j in list(store["archiwizowane"]["daty"][str(i)]):
                    for k in list(store["archiwizowane"]["daty"][str(i)][str(j)]):
                        try:
                            del store["archiwizowane"]["daty"][str(i)][str(j)][str(k)][str(self.pom.textt)]
                        except:
                            pass

            store["archiwizowane"] = store["archiwizowane"]
        except:
            pass
        self.popup.dismiss()

    def Archiwizuj(self, el): #Archwizuje Aktywnosc
        try:
            store.get("archiwizowane")
        except:
            store["archiwizowane"] = {}
        self.b = Archiwa()
        self.b.textt = str(el.textt)
        self.arch.add_widget(self.b)
        self.aktyw.remove_widget(el)
        store["archiwizowane"][str(el.textt)] = store["aktywnosci"][str(el.textt)]
        del store["aktywnosci"][str(el.textt)]
        store["aktywnosci"] = store["aktywnosci"]
        try:
            store["archiwizowane"]["daty"]
        except:
            store["archiwizowane"]["daty"] = {}
        for i in list(store["daty"]):
            try:
                store["archiwizowane"]["daty"][str(i)]
            except:
                store["archiwizowane"]["daty"][str(i)] = {}

            for j in list(store["daty"][str(i)]):
                try:
                    store["archiwizowane"]["daty"][str(i)][str(j)]
                except:
                    store["archiwizowane"]["daty"][str(i)][str(j)] = {}

                for k in list(store["daty"][str(i)][str(j)]):

                    try:
                        store["daty"][str(i)][str(j)][str(k)][str(el.textt)]
                        try:
                            store["archiwizowane"]["daty"][str(i)][str(j)][str(k)]
                        except:
                            store["archiwizowane"]["daty"][str(i)][str(j)][str(k)] = {}
                        store["archiwizowane"]["daty"][str(i)][str(j)][str(k)][str(el.textt)] = store["daty"][str(i)][str(j)][str(k)][str(el.textt)]
                        del store["daty"][str(i)][str(j)][str(k)][str(el.textt)]
                    except Exception as e:
                        pass
        store["archiwizowane"] = store["archiwizowane"]
        self.flaga = 1


    def Przywroc(self, el): #Przywraca Aktywnosc
        self.b = Aktywa()
        self.b.textt = str(el.textt)
        self.aktyw.add_widget(self.b)
        self.arch.remove_widget(el)
        store["aktywnosci"][str(el.textt)] = store["archiwizowane"][str(el.textt)]
        del store["archiwizowane"][str(el.textt)]
        for i in list(store["archiwizowane"]["daty"]):
            try:
                store["daty"][str(i)]
            except:
                store["daty"][str(i)] = {}
            for j in list(store["archiwizowane"]["daty"][str(i)]):
                try:
                    store["daty"][str(i)][str(j)]
                except:
                    store["daty"][str(i)][str(j)] = {}

                for k in list(store["archiwizowane"]["daty"][str(i)][str(j)]):
                    try:
                        store["archiwizowane"]["daty"][str(i)][str(j)][str(k)][str(el.textt)]
                        try:
                            store["daty"][str(i)][str(j)][str(k)]
                        except:
                            store["daty"][str(i)][str(j)][str(k)] = {}

                        store["daty"][str(i)][str(j)][str(k)][str(el.textt)] = store["archiwizowane"]["daty"][str(i)][str(j)][str(k)][str(el.textt)]
                        del store["archiwizowane"]["daty"][str(i)][str(j)][str(k)][str(el.textt)]
                    except Exception as e:
                        print(e)
        store["aktywnosci"] = store["aktywnosci"]
        store["archiwizowane"] = store["archiwizowane"]
        print(store["daty"])
        self.flaga = 1

#Ekran po kalendarzu
class S6(Screen):

    def klik(self, el): #Klikniecie do dodania wpisu
        self.manager.current = "7"

    def on_pre_enter(self, *args):
        try:
            try:
                self.remove_widget(self.a2)
            except:
                pass
            self.a2 = PodstawaWpisu(pos_hint = {"top":0.95, "x": 0})

            global edit

            if edit == 1:
                try:
                    self.a2.data["dzien"] = dzis.day
                    dziala = dzis.day
                    edit = 0
                except:
                    pass
            else:
                try:
                    self.a2.data["dzien"] = dzien.la.text  # Zapamietuje date dla widgetu, przyda sie przy edicie
                    dziala = dzien.la.text #Cyferka dnia, zalezy czy od edita czy od kalendarza, no i to wylapuje mam nadzieje, ehh
                except:
                    pass

            try:
                self.a2.te.text = str(store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)]["dzien"]['komentarz'])
            except:
                pass


            self.a2.data["miesiac"] = dzis.month
            self.a2.data["rok"] = dzis.year
            self.a2.dzien.text = calendar.day_name[int(datetime.date(int(dzis.year), int(dzis.month), int(dziala)).weekday())] + ", " + str(dziala) + " " + str(calendar.month_name[int(dzis.month)]) + " " + str(int(dzis.year))

            self.a2.im2.source = f"{store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)]['dzien']['ocena']}P.png"

            if int(store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)]["dzien"]["ocena"]) in range(1, 3):
                self.a2.im1.source = "bsadP.png"
                self.a2.cl = (120 / 255, 144 / 255, 156 / 255, 1)
            elif int(store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)]["dzien"]["ocena"]) in range(3, 5):
                self.a2.im1.source = "sadP.png"
                self.a2.cl = (69 / 255, 99 / 255, 137 / 255, 1)
            elif int(store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)]["dzien"]["ocena"]) in range(5, 7):
                self.a2.im1.source = "takseP.png"
                self.a2.cl = (119 / 255, 71 / 255, 131 / 255, 1)
            elif int(store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)]["dzien"]["ocena"]) in range(7, 9):
                self.a2.im1.source = "happyP.png"
                self.a2.cl = (53 / 255, 138 / 255, 83 / 255, 1)
            elif int(store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)]["dzien"]["ocena"]) in range(9, 11):
                self.a2.im1.source = "bhappyP.png"
                self.a2.cl = (203 / 255, 155 / 255, 25 / 255, 1)

            for l in list(store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)]):
                if l != "dzien":
                    self.b2 = AktWpis()

                    self.b2.akt.text = str(l)
                    self.b2.cl = self.a2.cl
                    if int(store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)][str(l)]["ocena"]) in range(1, 3):
                        self.b2.akt.color = (120 / 255, 144 / 255, 156 / 255, 1)
                    elif int(store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)][str(l)]["ocena"]) in range(3, 5):
                        self.b2.akt.color = (69 / 255, 99 / 255, 137 / 255, 1)
                    elif int(store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)][str(l)]["ocena"]) in range(5, 7):
                        self.b2.akt.color = (119 / 255, 71 / 255, 131 / 255, 1)
                    elif int(store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)][str(l)]["ocena"]) in range(7, 9):
                        self.b2.akt.color = (53 / 255, 138 / 255, 83 / 255, 1)
                    elif int(store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)][str(l)]["ocena"]) in range(9, 11):
                        self.b2.akt.color = (203 / 255, 155 / 255, 25 / 255, 1)
                    self.b2.im.source = f"{store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)][str(l)]['ocena']}P.png"
                    try:
                        self.b2.te.text = str(store['daty'][str(dzis.year)][str(dzis.month)][str(dziala)][str(l)]['komentarz'])
                    except:
                        pass
                    self.a2.gr.add_widget(self.b2)
            self.add_widget(self.a2)
        except Exception as e:
            print(e)
            pass

    def Usuniecie(self, el):
        try:
            self.remove_widget(el)
        except:
            pass


#Dodaj Wpis
class S7(Screen):
    ok = NumericProperty()
    moze = NumericProperty()
    wys = NumericProperty()
    szer = NumericProperty()
    stack = ObjectProperty(None)
    elo = StringProperty()
    jas = NumericProperty()
    cos = StringProperty()
    dz = ObjectProperty()
    wp = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ok = Window.width / 8
        self.moze = Window.width / 6.5
        self.wys = int(Window.height)
        self.szer = int(Window.width)
        self.elo = str(Window.size)
        self.jas = Window.height / Window.width
        self.cos = str(Window.dpi)
        self.edit = 0 #Mowi czy to jest w edicie

    def on_leave(self):
        self.stack.clear_widgets()

    def on_pre_enter(self):
        try:
            self.scrolek.scroll_y = 1
        except Exception as e:
            print(e, "SCROLEK")

        self.liczba = -1
        store["tymczasowe"] = {}

        global edit
        global d
        if edit == 1:
            try:
                self.wp = d
            except Exception as e:
                print(e, "EDIT")
        else:
            try:
                self.wp = str(dzien.la.text) + "/" + str(dzis.month) + "/" + str(dzis.year)
            except:
                pass

        """ #nie wiem czy jest git to wyzej
        try: # dz to jest label ktory mowi ktory dzien jest wpisywany
            self.dz.text = str(dzien.la.text) +"/" + str(dzis.month) + "/"+ str(dzis.year)
        except Exception as e: #to jest do EDITA
            #print(e, "WPIS PRENTER1")
            global d
            d = self.dz
        """

        #START GLOWNEGO DODAWANIA
        try:
            self.list = list(store["aktywnosci"])

            self.slownik = {}
            for i in self.list:
                self.liczba = self.liczba + 1 # do ID
                self.w = Widget(size_hint=(1, None), height=self.wys / 16) #żeby zrobic se elegancko odstęp
                self.stack.add_widget(self.w)
                self.l = Label(size_hint=(1, None), font_size=dp(20), text=str(i), height=self.szer / 10) #Nazwa aktywnosci
                self.stack.add_widget(self.l)
                self.grid = Grid1()
                #Tworzymy se emotki usmiechy przyciski
                self.b = Button(background_normal="bsadP.png", background_down="bsadW.png", size_hint=(None, None),
                                 size=(self.ok, self.ok))
                self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
                self.b.ids = {"A": self.liczba}
                self.grid.add_widget(self.b)

                self.b = Button(background_normal="sadP.png", background_down="sadW.png", size_hint=(None, None),
                                 size=(self.ok, self.ok))
                self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
                self.b.ids = {"A": self.liczba}
                self.grid.add_widget(self.b)

                self.b = Button(background_normal="takseP.png", background_down="takseW.png", size_hint=(None, None),
                                 size=(self.ok, self.ok))
                self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
                self.b.ids = {"A": self.liczba}
                self.grid.add_widget(self.b)

                self.b = Button(background_normal="happyP.png", background_down="happyW.png", size_hint=(None, None),
                                 size=(self.ok, self.ok))
                self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
                self.b.ids = {"A": self.liczba}
                self.grid.add_widget(self.b)

                self.b = Button(background_normal="bhappyP.png", background_down="bhappyW.png", size_hint=(None, None),
                                 size=(self.ok, self.ok))
                self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
                self.b.ids = {"A": self.liczba}
                self.grid.add_widget(self.b)

                self.stack.add_widget(self.grid)
                self.w = Widget(size_hint=(1, None), height=self.szer / 20)
                self.stack.add_widget(self.w)
                self.stackk = Stackk()

                self.grid = Grid2()
                #Tworzymy pierwszy rzad cyferek
                for i in range(1, 11, 2):
                    self.b = Button(background_normal=f"{str(i)}P.png", background_down=f"{str(i)}W.png",
                                    size_hint=(None, None), size=(self.moze, self.moze), on_press=self.klik)
                    self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
                    self.b.ids = {"A": self.liczba}
                    self.grid.add_widget(self.b)
                #Tworzymy drugi rzad cyferek
                for i in range(2, 11, 2):
                    self.b = Button(background_normal=f"{str(i)}P.png", background_down=f"{str(i)}W.png",
                                    size_hint=(None, None), size=(self.moze, self.moze), on_press=self.klik)
                    self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
                    self.b.ids = {"A": self.liczba}
                    self.grid.add_widget(self.b)

                self.stackk.add_widget(self.grid)
                self.slownik["stack" + str(self.liczba)] = self.stackk
                self.stack.add_widget(self.stackk)

            #ROBIMY TERAZ DZIEN

            self.liczba = self.liczba + 1
            self.w = Widget(size_hint=(1, None), height=self.wys / 16)
            self.stack.add_widget(self.w)
            self.l = Label(size_hint=(1, None), font_size=dp(20), text="Ocena Dnia", height=self.szer / 10)
            self.stack.add_widget(self.l)

            self.grid = Grid1()

            self.b = Button(background_normal="bsadP.png", background_down="bsadW.png", size_hint=(None, None),
                            size=(self.ok, self.ok))
            self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
            self.b.ids = {"A": self.liczba}
            self.grid.add_widget(self.b)

            self.b = Button(background_normal="sadP.png", background_down="sadW.png", size_hint=(None, None),
                            size=(self.ok, self.ok))
            self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
            self.b.ids = {"A": self.liczba}
            self.grid.add_widget(self.b)

            self.b = Button(background_normal="takseP.png", background_down="takseW.png", size_hint=(None, None),
                            size=(self.ok, self.ok))
            self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
            self.b.ids = {"A": self.liczba}
            self.grid.add_widget(self.b)

            self.b = Button(background_normal="happyP.png", background_down="happyW.png", size_hint=(None, None),
                            size=(self.ok, self.ok))
            self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
            self.b.ids = {"A": self.liczba}
            self.grid.add_widget(self.b)

            self.b = Button(background_normal="bhappyP.png", background_down="bhappyW.png", size_hint=(None, None),
                            size=(self.ok, self.ok))
            self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
            self.b.ids = {"A": self.liczba}
            self.grid.add_widget(self.b)

            self.stack.add_widget(self.grid)
            self.w = Widget(size_hint=(1, None), height=self.szer / 20)
            self.stack.add_widget(self.w)
            self.stackk = Stackk()

            self.grid = Grid2()

            for i in range(1, 11, 2):
                self.b = Button(background_normal=f"{str(i)}P.png", background_down=f"{str(i)}W.png",
                                size_hint=(None, None), size=(self.moze, self.moze), on_press=self.klik)
                self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
                self.b.ids = {"A": self.liczba}
                self.grid.add_widget(self.b)
            for i in range(2, 11, 2):
                self.b = Button(background_normal=f"{str(i)}P.png", background_down=f"{str(i)}W.png",
                                size_hint=(None, None), size=(self.moze, self.moze), on_press=self.klik)
                self.slownik[str(self.b.background_normal) + str(self.liczba)] = self.b
                self.b.ids = {"A": self.liczba}
                self.grid.add_widget(self.b)
            self.stackk.add_widget(self.grid)


            self.slownik["stack" + str(self.liczba)] = self.stackk

            self.stack.add_widget(self.stackk)
            self.w = Widget(size_hint=(1, None), height=self.wys /36)
            self.stack.add_widget(self.w)
            self.w = Widget(size_hint=(None, None), height=self.wys /36, width = Window.width/2.5)
            self.stack.add_widget(self.w)
            # DODANIE PRZYCISKU AKCEPTACJI
            self.b = Button(background_normal="checkW.png", background_down= "checkW.png",
                            size_hint=(None, None), size=(1.2*self.moze, 1.2*self.moze), on_press=self.koniec)

            self.stack.add_widget(self.b)

            self.w = Label(size_hint=(1, None), height=self.wys / 20, pos_hint = {"top": 1}, font_size = dp(20)) #Label do ostrzezenia ze treba dodac dzien
            self.stack.add_widget(self.w)
            self.ww = Widget(size_hint = (1,None), height = self.wys/10)
            self.stack.add_widget(self.ww)

            global slowniczek #to do edycji, pomaga ogarniac temat
            slowniczek = self.slownik

        except Exception as e:
            print(e, "PREENTEr s7")
            pass

    def koniec(self, el): #Przycisk do akceptacji
        try:
            global wyl
            wyl.focus = False
            Clock.schedule_once(self.pom2, 0)# wylaczamy focus dla textinputa, zeby tekst sie zapamietal
            #TEN CLOCK RACZEJ NIEPOTRZEBNY ALE
            #print(store["tymczasowe"])
            #print(wyl.text)
        except Exception as e:
            print(e, "FOCUS")
            pass
        try:
            global dzis # to tak asekuracyjnie, zeby nie wywalilo, ze nie zdefiniowany dzis jest
            store["tymczasowe"]["dzien"] #próbujemy, czy jest ocena dnia
            try:
                store["daty"]
            except:
                store["daty"] = {} #tworzymy miejsce w store
            try:
                store.get("daty")[str(dzis.year)]
            except:
                store["daty"][str(dzis.year)] = {}
            try:
                store.get("daty")[str(dzis.year)][str(dzis.month)]
            except:
                store.get("daty")[str(dzis.year)][str(dzis.month)] = {}
            try:
                store.get("daty")[str(dzis.year)][str(dzis.month)][str(dzien.la.text)]
            except:
                try:
                    store.get("daty")[str(dzis.year)][str(dzis.month)][str(dzien.la.text)] = {}
                except: #to do edita
                    try:
                        store.get("daty")[str(dzis.year)][str(dzis.month)][str(dzis.day)]
                    except:
                        store.get("daty")[str(dzis.year)][str(dzis.month)][str(dzis.day)] = {}

            lista = list(store["tymczasowe"])



            try: #wpisujemy do store z tymczasowego
                for i in lista:
                    store.get("daty")[str(dzis.year)][str(dzis.month)][str(dzien.la.text)][str(i)] = {}
                    store.get("daty")[str(dzis.year)][str(dzis.month)][str(dzien.la.text)][str(i)]["ocena"] = \
                    store["tymczasowe"][str(i)]["ocena"]
                    try:
                        store.get("daty")[str(dzis.year)][str(dzis.month)][str(dzien.la.text)][str(i)]["komentarz"] = \
                        store["tymczasowe"][str(i)]["komentarz"]
                    except:
                        pass
            except: #to do edita, wpisujemy do store rzeczy z tymczasowego slownika
                for i in lista:
                    store.get("daty")[str(dzis.year)][str(dzis.month)][str(dzis.day)][str(i)] = {}

                    store.get("daty")[str(dzis.year)][str(dzis.month)][str(dzis.day)][str(i)]["ocena"] = \
                    store["tymczasowe"][str(i)]["ocena"]
                    try:
                        store.get("daty")[str(dzis.year)][str(dzis.month)][str(dzis.day)][str(i)]["komentarz"] = \
                        store["tymczasowe"][str(i)]["komentarz"]
                    except:
                        pass

            store["daty"] = store["daty"]
            global wpis
            wpis = 1
            global wykres
            wykres = 1
            self.manager.current = "6"

        except Exception as e:
            print(e)
            self.w.text = "Aby dodać wpis musisz ocenić swój dzień"
            Clock.schedule_once(self.pom, 3.5)

    def pom(self, el):
        self.w.text = ""

    def pom2(self, el):
        global wyl
        wyl.focus = False

    def klik(self, el): #Klikniecie w cyferke
        p = list(el.ids.values())[0]
        lista = list(store["aktywnosci"])

        try: #Zmieniamy wypelnienie emotki i cyferki na wczesniejsze, odkliknięcie
            self.slownik[str(p)].background_normal = self.slownik["zapk" + str(p)]
            self.slownik["em" + str(p)].background_normal = self.slownik["emb" + str(p)]
        except:
            pass

        #Zapamiętujemy se
        self.slownik[str(p)] = el
        self.slownik["zapk" + str(p)] = el.background_normal

        el.background_normal = el.background_down

        if self.slownik["stack" + str(p)] != "": # == "" bo zmieniamy stacka na "" jak juz jest dodane, zeby nie dodawac kilka razy
            #Dodanie textinputa po kliknieciu
            self.t = Textt(multiline=True, width=self.szer / 1.5)
            self.t.ids = {"A": str(p)}
            self.w3 = Widget(size_hint=(1, None), height=self.wys / 25)
            self.w2 = Widget(size_hint=(None, None), size=(0, 0), width=self.szer / 6, height=self.wys / 15)
            self.slownik["text" + str(p)] = self.t
            self.slownik["stack" + str(p)].add_widget(self.w3)
            self.slownik["stack" + str(p)].add_widget(self.w2)
            self.slownik["stack" + str(p)].add_widget(self.t)

            #Pzykładowe komentarze
            if int(p) in range(len(list(store["aktywnosci"]))):
                self.kom = Komentarz()
                self.kom.b.ids = {"A": str(p)}
                self.slownik["kom" + str(p)] = self.kom
                self.kom.b.bind(on_press = self.pruba)
                try:
                    for i in store["aktywnosci"][str(lista[int(p)])]["przykladowe"]:
                        self.tekst = tekscik()
                        self.tekst.ids = {"A": str(p)}
                        self.tekst.bind(focus=self.popupklik)
                        self.tekst.hint_text = str(i)
                        self.kom.g.add_widget(self.tekst)
                except:
                    pass
                self.slownik["stack" + str(p)].add_widget(self.kom)
            self.slownik["stack" + str(p)] = "" #zmiana zeby sie nie powtarzal stack
            slowniczek = self.slownik

        a = el.background_normal.split("P") #chcemy tylko nazwe emotki

        if len(a[0]) == len(el.background_normal): #gdyby było emotkaW zamiast emotkaP
            a = el.background_normal.split("W")

        #Ustawiamy emotke i zapamietujemy ja tez
        if int(a[0]) in range(1, 3):
            self.slownik["emb" + str(p)] = "bsadP.png"
            self.slownik["em" + str(p)] = self.slownik["bsadP.png" + str(p)]
        elif int(a[0]) in range(3, 5):
            self.slownik["emb" + str(p)] = "sadP.png"
            self.slownik["em" + str(p)] = self.slownik["sadP.png" + str(p)]
        elif int(a[0]) in range(5, 7):
            self.slownik["emb" + str(p)] = "takseP.png"
            self.slownik["em" + str(p)] = self.slownik["takseP.png" + str(p)]
        elif int(a[0]) in range(7, 9):
            self.slownik["emb" + str(p)] = "happyP.png"
            self.slownik["em" + str(p)] = self.slownik["happyP.png" + str(p)]
        elif int(a[0]) in range(9, 11):
            self.slownik["emb" + str(p)] = "bhappyP.png"
            self.slownik["em" + str(p)] = self.slownik["bhappyP.png" + str(p)]

        self.slownik["em" + str(p)].background_normal = self.slownik["em" + str(p)].background_down #Zmiana na wypelniona

        if int(p) < len(lista): #Dodanie do tymczasowego, jak za duzy indeks to znaczy ze to jest dzien
            store.get("tymczasowe")[str(lista[p])] = {}
            store.get("tymczasowe")[str(lista[p])]["ocena"] = str(a[0])
        else:
            store.get("tymczasowe")["dzien"] = {}
            store.get("tymczasowe")["dzien"]["ocena"] = str(a[0])

    def pruba(self, el): #Tworzymy popupa
        self.numerek = list(el.ids.values())[0]
        self.content = BoxLayout(orientation = "vertical")
        self.popup = Popup(title='Dodaj przykładowy komentarz',
                           content=self.content,
                           size_hint=(None, None), size=(Window.width / 1.5, Window.height / 3.5))
        self.b3 = TextInput(size_hint = (1,None), height = Window.height / 10)
        self.b1 = Button(text="Akceptuj")
        self.b2 = Button(text="Odrzuć")
        self.b1.bind(on_press=self.popup1)
        self.b2.bind(on_press=self.popup.dismiss)
        self.content.add_widget(self.b3)
        self.content.add_widget(self.b1)
        self.content.add_widget(self.b2)
        self.popup.open()

    def popup1(self, el): #Bind do przycisku zeby otworzyc popupa
        lista = list(store["aktywnosci"])
        try:
            store["aktywnosci"][str(lista[int(self.numerek)])]["przykladowe"]
        except:
            store["aktywnosci"][str(lista[int(self.numerek)])]["przykladowe"] = []
        try:
            self.tekst = tekscik()
            self.slownik["kom" + str(self.numerek)].g.add_widget(self.tekst)
            self.tekst.ids = {"A": str(self.numerek)}
            self.tekst.bind(focus = self.popupklik)
            self.tekst.hint_text = self.b3.text
            store["aktywnosci"][str(lista[int(self.numerek)])]["przykladowe"].append(self.b3.text)
            store["aktywnosci"] = store["aktywnosci"]
        except:
            #print("Maksymalnie 4 komentarze")
            self.slownik["kom" + str(self.numerek)].g.remove_widget(self.tekst)
            pass
        self.popup.dismiss()

    def popupklik(self, el, ee): #Bind do przycisku z popupa
        if el.focus == True:
            p = list(el.ids.values())[0]

            lista = list(store["aktywnosci"])
            self.content = BoxLayout(orientation = "vertical", size_hint = (1,None), spacing = Window.height/80)
            self.content.height = self.content.minimum_height
            self.popup = Popup(title='Akceptuj lub usun komenatrz',
                               content=self.content,
                               size_hint=(None, None), width = Window.width / 1.5)
            #self.popup.height = self.popup.minimum_height
            self.t = tekscik(size_hint = (1,None))
            self.t.text = str(el.hint_text)
            self.t.height = self.t.minimum_height
            self.box = BoxLayout(size_hint = (1,None))
            self.box.height = Window.height/30
            self.b1 = Button(text="Akceptuj", size_hint = (1, 1), height = (Window.height/30))
            self.b2 = Button(text="Usun", size_hint = (1, 1), height = Window.height/30)
            self.b3 = Button(text="Anuluj", size_hint = (1, 1), height = Window.height/30)
            self.b1.bind(on_press = partial(self.bind1, el, p))
            self.b2.bind(on_press = partial(self.bind2, el, p))
            self.b3.bind(on_press=self.popup.dismiss)
            self.content.add_widget(self.t)
            self.box.add_widget(self.b1)
            self.box.add_widget(self.b2)
            self.box.add_widget(self.b3)
            self.content.add_widget(self.box)
            self.popup.open()
            el.focus = False
            Clock.schedule_once(self.Test, 0)

    def Test(self, czas): #zeby ustawic wysokosc popupa bo sie inaczej nei da ehh
        self.popup.height = self.content.minimum_height + Window.height/11

    def bind1(self, el, p, el2): #bind do przycisku przycisku z popupa
        self.slownik["text" + str(p)].text = el.hint_text
        store["tymczasowe"][list(store["aktywnosci"])[int(p)]]["komentarz"] = el.hint_text
        self.popup.dismiss()

    def bind2(self, el, p, el2): #bind do przycisku przycisku z popupa
        lista = list(store["aktywnosci"])
        store["aktywnosci"][str(lista[int(p)])]["przykladowe"].remove(el.hint_text)
        store["aktywnosci"] = store["aktywnosci"]
        self.slownik["kom" + str(p)].g.remove_widget(el)
        self.popup.dismiss()



class S8(Screen): #Screen Informacyjny
    dens = StringProperty()
    dpi = StringProperty()
    rounded = StringProperty()
    font = StringProperty()
    czas = StringProperty()
    czas2 = StringProperty()
    czas3 = StringProperty()
    czas4 = StringProperty()
    czas5 = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dens = str(Metrics.density)
        self.dpi = str(Metrics.dpi)
        self.rounded = str(Metrics.dpi_rounded)
        self.font = str(Metrics.fontscale)

    def on_pre_enter(self, *args):
        try:
            self.czas = str(sm.get_screen("1").czas)
            self.czas2 = str(sm.get_screen("1").czas2)
            self.czas3 = str(sm.get_screen("3").czas)
            self.czas4 = str(sm.get_screen("3").czas2)
            self.czas5 = str(sm.get_screen("3").czas3)
        except:
            pass

class Kolko2(Button):
    pass

class Aktywa(BoxLayout):
    pass

class Archiwa(BoxLayout):
    pass

class ArrowButton(Button):
    pass

class Kolko(Button):
    pass

class SpinnerOptions(SpinnerOption):
    def __init__(self, **kwargs):
        super(SpinnerOptions, self).__init__(**kwargs)
        #self.background_normal = ''
        self.background_color = (119/255,71/255,131/255,1)
        self.height = Window.height/20

class Spin(Spinner):
    pass

class ScrollWpis(ScrollView):
    pass


class Textt(TextInput):

    def pom(self, el, inst):
        global wyl
        wyl = el
        #print(el.text)

    def on_text(self, instance, value):
        try:
            global wyl
            if wyl != instance:
                wyl = instance
         #       print("WCHODZE")
        except:
            pass
    def on_focus(self, instance, value):
        Clock.schedule_once(partial(self.pom,instance), 0)
        p = list(self.ids.values())[0]
        lista = list(store["aktywnosci"])

         # zapamiętujemy ktory textinput jest odwiedzony,
        #zeby go potem unfocusowac, bo inaczej nie zapamieta textu

        if value: #jezeli jest w focusie, zmianiamy na pisanie od lewej, oraz usuwamy hint texta
            self.zap = self.hint_text
            self.hint_text = ""
            self.halign = "left"
        else:
            self.hint_text = self.zap
            if self.text == "": #jezeli jest puste to znowu na srodek hint text
                self.halign = "center"
            else: # jak nie to dodajemy do slownika tymczasowego, jak za dluga lista to znaczy ze to jest dzien
                if int(p) < len(lista):
                    store.get("tymczasowe")[str(lista[int(p)])]["komentarz"] = self.text
                else:
                    store.get("tymczasowe")["dzien"]["komentarz"] = self.text
        try:
            store["tymczasowe"] = store["tymczasowe"]
        except:
            pass

class Grid1(GridLayout):
    pass

class Stackk(StackLayout):
    pass

class Grid2(GridLayout):
    pass

class Komentarz(GridLayout):
    pass

class tekscik(TextInput):
    pass


class AktWpis(GridLayout):
    pass

class PodstawaWpisu(GridLayout):
    pass

class Lab(Label):
    pass

class Grid3(GridLayout):
    pass


class TestApp(App):
    sz = NumericProperty()
    wy = NumericProperty()
    open = StringProperty()
    def build(self):
        self.czas = time.time()
        self.sz = Window.width
        self.wy = Window.height
        try:
            store["daty"]
        except:
            store["daty"] = {}
        try:
            store["aktywnosci"]
        except:
            store["aktywnosci"] = {}
        global sm
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(S1(name='1'))
        sm.add_widget(S2(name='2'))
        sm.add_widget(S3(name='3'))
        sm.add_widget(S4(name='4'))
        sm.add_widget(S5(name='5'))
        sm.add_widget(S6(name='6'))
        sm.add_widget(S7(name='7'))
        sm.add_widget(S8(name='8'))
        return sm

    def on_start(self, **kwargs):
        self.open = str(time.time() - self.czas)
        #print(time.time() - self.czas, "CZAS APKI")

if __name__ == '__main__':
    TestApp().run()