import requests

cont = 0
while cont < 70:
    r = requests.get('http://localhost:5000/weather/{}'.format(cont))
    if r.status_code == 200:
        print(r.json())
    elif r.status_code == 429:
        print("Limite Rate")

    cont += 1
