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
