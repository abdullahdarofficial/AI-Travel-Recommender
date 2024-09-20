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

