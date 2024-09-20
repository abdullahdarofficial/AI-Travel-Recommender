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
