import requests
import re, json
from openai import OpenAI

prompt = 'i like a place with high skyscrappers and culture and some food and i also like places with beaches and nice and warm weather and my budegt perday is 152'


def askAI():
    response = requests.post('https://fumes-api.onrender.com/llama3',
    json={
   'prompt': [
     {"role": "system", "content": "You have to analyse the user prompt and suggest them more than 5 countries based on their preferences. you only have to suggest them countries based on their preferences and write the standard Name for the countries. You Have to Follow a specific format to suggest them countries in all cases no exception. The format is: [country Name1, Country Name2, Country Name3, ...., country Name N]"},
     {"role": "user", "content": f"{prompt}"}
    ],
      "temperature":0.5,
      "topP":0.3,
      "lengthPenality":0.3,
       "maxTokens": 2000
    }, stream=True)

    text = ''
    buffer = ''
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            print(chunk.decode('utf-8'))
            buffer += chunk.decode('utf-8')
            try:
                data = json.loads(buffer)
                content = data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                text += content
                buffer = ''  # Clear the buffer once we've successfully parsed it
            except json.JSONDecodeError:
                # If a JSONDecodeError is raised, it means that the buffer does not contain a complete JSON object
                # So we just continue accumulating chunks in the buffer
                pass

    return text



def extract_data(text):
    matches = re.findall(r'\[([^]]*)\]', text)
    countries = [country.strip() for country in matches[0].split(',')]
    return countries

def ask():
        import pickle
c