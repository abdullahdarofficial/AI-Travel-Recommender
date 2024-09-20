import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
import tkintermapview as map
from HybridRecommender import HybridRecommender
import pandas as pd
import requests, threading, re, pickle
from openai import OpenAI
import json, time
from tkGIF import gifplay

r = 0

def geo_code(place):
    url = f"https://api.geoapify.com/v1/geocode/search?text={place}&limit=1&type=country&format=json&apiKey=d76f029b27e04a9cb47a5356a7bf2a87"
    response = requests.get(url)

    response = response.json()
    latitude = response['results'][0]['lat']
    longitude = response['results'][0]['lon']

    return latitude, longitude


def get_places(geo_id, lat, lon, place=True):
    ID_url = f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lon}&format=json&apiKey=d76f029b27e04a9cb47a5356a7bf2a87"

    if place:
        response = requests.get(ID_url)
        id = response.json()
        id = id['results'][0]['place_id']
        print(id)
        url = f"https://api.geoapify.com/v2/places?categories=accommodation.hotel,accommodation.hut,activity,sport,heritage,ski,tourism,leisure,natural,rental.bicycle,rental.ski,entertainment&conditions=named&filter=place:{id}&limit=10&apiKey=d76f029b27e04a9cb47a5356a7bf2a87"
        result = requests.get(url)

    else:
        iso = get_iso(lat, lon)
        iso_id = iso['properties']['id']
        url = f"https://api.geoapify.com/v2/places?categories=accommodation.hotel,accommodation.hut,activity,sport,heritage,ski,tourism,leisure,natural,rental.bicycle,rental.ski,entertainment&conditions=named&filter=geometry:{iso_id}&limit=10&apiKey=d76f029b27e04a9cb47a5356a7bf2a87"
        result = requests.get(url)

    return result.json()

def get_iso(lat, lon):
    url_iso = f'https://api.geoapify.com/v1/isoline?lat={lat}&lon={lon}&type=time&mode=drive&range=900&apiKey=d76f029b27e04a9cb47a5356a7bf2a87'
    result = requests.get(url_iso)
    return result.json()


convo_history = []


special_cases = {'Greenland': 'Kalaallit Nunaat', 'Bangladesh': 'Dhaka,Bangladesh', 'Jordan': 'Amman,Jordan', 'Lebanon': 'Beirut,Lebanon',
                'palau': 'Ngerulmud,palau', 'Armenia': 'Yerevan,Armenia', 'Sudan':'Khartoum,Sudan'}


class Card(ctk.CTkFrame):
    def __init__(self, *args, title=None, width: int = 250, height: int = 275, cr: int = 19, image=None, **kwargs):
        super().__init__(*args, corner_radius=cr, width=width, height=height, **kwargs)

        self.image_dim = (width-32, (height*0.45)-7)
        self.places = None
        if image is None:
            self.image = ctk.CTkImage(dark_image=Image.open('Images/no image d.png'),
                                    light_image=Image.open('Images/no image l.png'),
                                    size=self.image_dim)
            self.image_label = ctk.CTkLabel(self, image=self.image, text='', corner_radius=cr)
            self.image_label.grid(row=0, column=0, columnspan=3, padx=16, pady=(5, 2), sticky="ewn")

        else:
            self.image = ctk.CTkImage(dark_image=Image.open('Images/' + image),
                                    light_image=Image.open('Images/' + image),
                                    size=self.image_dim)
            self.image_label = ctk.CTkLabel(self, image=self.image, text='', corner_radius=cr)
            self.image_label.grid(row=0, column=0, columnspan=3, padx=16, pady=(5, 2), sticky="ewn")

        self.body_dim = (width-16, height*0.6)
        self.body = ctk.CTkFrame(self, width=self.body_dim[0], height=self.body_dim[1], corner_radius=cr, border_width=3)
        self.body.grid(row=1, column=0, columnspan=3, pady=(5, 8), padx=8, sticky="ews")

        self.body.grid_columnconfigure((0,7), weight=1)

        self.title = ctk.CTkLabel(self.body, text=title, corner_radius=cr, font=('Arial', 14, 'bold'))
        self.title.grid(row=0, column=3, pady=5, padx=5)

        self.button_detail = ctk.CTkButton(self.body, text='View Detail', corner_radius=cr, command=lambda: self.view_detail(title))
        self.button_detail.grid(row=1, column=3, pady=(8,13), padx=5)


    def search(self):
        self.map_widget.delete_all_marker()
        if self.search_entry.get() == '':
            return

        try:

            url = f"https://api.geoapify.com/v1/geocode/search?text={self.search_entry.get()}&limit=20&format=json&apiKey=d76f029b27e04a9cb47a5356a7bf2a87"
            response = requests.get(url)

            response = response.json()

            highest_confidence = 0
            best_result = None

            for result in response['results']:
                if result['rank']['confidence'] > highest_confidence:
                    highest_confidence = result['rank']['confidence']
                    best_result = result

            if best_result is not None:
                text = best_result['formatted']
                latitude = best_result['lat']
                longitude = best_result['lon']

                self.map_widget.set_position(latitude, longitude, marker=True, text=text)

            # self.map_widget.set_address(self.search_entry.get(), marker=True)
            # self.map_widget.set_zoom(10)
            self.map_widget.update()

        except Exception as e:
            tk.messagebox.showerror('Error', str(e))

    def satelite_tile(self):
        if self.map_widget.tile_server != "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga")
            self.map_widget.update()

    def default_tile(self):
        if self.map_widget.tile_server != "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
            self.map_widget.update()

    def get_spots(self, country, map, fr):

        def patani(str):
            print(str)
            map.delete_all_marker()

            # using different api to get the geo code as i am blocked by the previous api :(
            lat, lng = geo_code(country)
            map.set_position(lat, lng, marker=True, text=country)

            # map.set_address(country, marker=True)

            x, y = self.places[self.places['name'] == str][['lat', 'lng']].values[0]
            map.set_marker(x, y, str)

            place = get_places(None, x, y, place=False)

            map.set_position(x, y)
            map.set_zoom(13)
            print(place)

            for pl in place['features']:
                map.set_marker(pl['geometry']['coordinates'][1], pl['geometry']['coordinates'][0], pl['properties']['name'])
            map.update()

        def patani_wrapper(name):
            th = threading.Thread(target=patani, args=(name,), daemon=True)
            th.start()

            top = ctk.CTkToplevel()
            top.title('Please Wait...')
            top.geometry('300x150')
            top.grab_set()
            top.resizable(False, False)
            top.columnconfigure((0,5), weight=1)
            top.rowconfigure((0,5), weight=1)


            icon_lbl = ctk.CTkLabel(top, text='')
            icon_lbl.grid(row=1, column=1, padx=10, pady=10)

            ctk.CTkLabel(top, text='Please wait while the little elves draw your map', wraplength=150, font=('Arial', 13)).grid(row=2, column=1, padx=10, pady=5)

            gif = gifplay(icon_lbl,'./Images/loading.gif', 0.01)
            gif.play()

            while th.is_alive():
                top.update()
                time.sleep(0.01)

            top.destroy()
            top.mainloop()

        df = pd.read_csv('world-cities.csv')
        self.places = df[df['country'] == country][['name', 'lat', 'lng']]

        if len(self.places) == 0:
            ctk.CTkLabel(fr, text='No Cities Data Available for this Country!!', font=('Arial', 14, 'bold')).grid(row=1, column=1, padx=10, pady=10)

        if len(self.places) > 4:
            top_three = self.places.iloc[:3]

            remaining = self.places.iloc[3:]
            remaining = remaining.sample(n=min(5, len(remaining)))
            self.places = pd.concat([top_three, remaining])

        for i in range(len(self.places)):
            btn = ctk.CTkButton(fr, text=self.places.iloc[i]['name'], corner_radius=19, fg_color='#1A1A1A', width=170, height=90,
                                hover_color='#373737', command=lambda name=self.places.iloc[i]['name']: patani_wrapper(name))
            btn.grid(row=1+i//3, column=1+i%3, padx=10, pady=10)

        map.update()

    def view_detail(self, country):
        global special_cases

        top = ctk.CTkToplevel()
        top.title('Details')
        top.geometry('900x700')
        top.grab_set()
        top.resizable(False, False)
        top.columnconfigure((0,6), weight=1)

        search_frame = ctk.CTkFrame(top, width=400, height=40, corner_radius=19, fg_color='transparent')
        search_frame.grid(row=0, column=1, padx=10, pady=(10,5), columnspan=3)
        search_frame.columnconfigure((0,7), weight=1)

        self.search_entry = ctk.CTkEntry(search_frame, width=400, height=30, corner_radius=19)
        self.search_entry.grid(row=0, column=1)
        self.search_entry.bind('<Return>', lambda e: self.search())

        search_button = ctk.CTkButton(search_frame, text='', width=20, height=30, fg_color='#1A1A1A',
                                    corner_radius=19, command=self.search, hover_color='#373737',
                                    image=ctk.CTkImage(dark_image=Image.open('Images/search.png'),size=(15,15)))
        search_button.grid(row=0, column=2, padx=5)

        map_frame = ctk.CTkFrame(top, width=800, height=500)
        map_frame.grid(row=1, column=1, padx=10, pady=10)
        map_frame.columnconfigure((0,7), weight=1)

        self.map_widget = map.TkinterMapView(map_frame, width=750, height=450, corner_radius=19)
        self.map_widget.grid(row=0, column=1, padx=1, pady=1)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")


        lat, lng = geo_code(country)
        self.map_widget.set_position(lat, lng, marker=True, text=country)

        # try:
        #    a = self.map_widget.set_address(special_cases.get(country)if special_cases.get(country)else country,marker=True,text=country)
        #    if not a:
        #         tk.messagebox.showerror('Error', str('Check Internet Connection\n Connection Time Out!!'))

        # except Exception as e:
        #     if '403' in str(e):
        #         tk.messagebox.showerror('Error-403', str('request blocked by the server\nTry again later!!'))
        #     else:
        #         tk.messagebox.showerror('Error', str('Check Internet Connection\n Connection Time Out!!'))


        sat_but = ctk.CTkButton(self.map_widget, text='', width=26, height=26, command=self.satelite_tile,
                                image=ctk.CTkImage(dark_image=Image.open('Images/satellite.png'), size=(20,20)),
                                corner_radius=2, fg_color='#333333', hover_color='#555555'
                                )
        sat_but.place(x=15, y=81, anchor='nw')

        def_but = ctk.CTkButton(self.map_widget, text='', width=26, height=26, command=self.default_tile,
                                image=ctk.CTkImage(dark_image=Image.open('Images/default.png'), size=(20,20)),
                                corner_radius=2, fg_color='#333333', hover_color='#555555'
                                )
        def_but.place(x=15, y=114, anchor='nw')

        detail = ctk.CTkScrollableFrame(top, width=650, height=200, corner_radius=19, fg_color='black')
        detail.grid(row=2, column=1, padx=10, pady=10)
        detail.columnconfigure((0,7), weight=1)
        detail.rowconfigure((0,9), weight=1)

        threading.Thread(target=self.get_spots(country, self.map_widget, detail), daemon=True).start()
        top.mainloop()


def load_more(cur, cards, btn_fr, home, recommendation):

    btn_fr.grid_forget()
    total = cur + 12
    if total > 222:
        total = 222

    rec = recommendation.recommend(top_n=total)
    for i in range(cur, total):
        card = Card(home, title=rec['Country'].iloc[i], cr=19, fg_color='gray29', border_width=5)
        card.grid(row=1+i//4, column=i%4, padx=(40, 0), pady=(40, 0))
        cards.append(card)

    if total < 222:
        btn_fr.grid(row=2+len(cards)//4, column=0, columnspan=4, pady=30, sticky='ew')
    else:
        ctk.CTkLabel(home, text='', fg_color='transparent').grid(row=2+len(cards)//4, column=0, columnspan=4, pady=20)


def home_page(fr):

    home = ctk.CTkScrollableFrame(fr, corner_radius=19, fg_color='transparent', width=1310, height=640)
