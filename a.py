import requests

prompt = 'i like a place with beautiful nature and culture and some food and i also like places with beaches and nice and warm weather and my budegt perday is 152'#input('Prompt: ')

# keywords = ['europe', 'history', 'mountain', 'cold', 'skyscrapper', 'desert', 'beach',
#  'asia', 'hot', 'food', 'culture', 'island', 'northamerica', 'southamerica',
#  'africa', 'plain', 'wildlife', 'australia', 'forest']



def askAI():
    response = requests.post('https://fumes-api.onrender.com/llama3',
    json={
    f'prompt': """{
    'systemPrompt': 'You have to analyse the user prompt and generate keywords for the following keywords that most accurately describes 
    users preferences for a travel destination. The keywords are: ['europe', 'history', 'mountain', 'cold', 'skyscrapper', 'desert', 'beach',
    'asia', 'hot', 'food', 'culture', 'island', 'northamerica', 'southamerica',
    'africa', 'plain', 'wildlife', 'australia', 'forest'].',
    'Assistant': 'keywords are: keyword0,keyword1,keyword2,keyword3... - budget per day (if given)',
    'user': 'i like a place with beautiful nature and culture and some food and i also like places with beaches and nice and warm weather',
    }""",
      "temperature":0,
      "topP":0.3,
      "lengthPenality":0.3,
       "maxTokens": 200
    }, stream=True)
      # str = response.text
      # print(str)