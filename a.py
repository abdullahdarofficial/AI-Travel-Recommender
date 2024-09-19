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
    text = ''
    for chunk in response.iter_content(chunk_size=1024):  
        if chunk:
            text += chunk.decode('utf-8')
    #print(text)
    return text

#while True:
#try:
text = askAI()
text = text.replace('YOU CAN BUY ME COFFE! https://buymeacoffee.com/mygx', '')
text = text.replace("Based on the user's prompt, the keywords that most accurately describe their preferences for a travel destination are: ", '')

#_, budget = text.split('$')

print('Llama3:',text)#, budget)
# keywords_and_budget = []
# # Split the text on the colon to separate the keywords and budget from the rest of the text
# keywords_and_budget.append(text.split(':'))