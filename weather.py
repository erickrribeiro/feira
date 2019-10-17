import os
import requests
import datetime


class Weather(object):
    def __init__(self, token):
        self._token = token

    def _kelvin2celsius(self, K):
        return int(K - 273.15)

    def fetch(self, city_id, date):
        url = 'http://api.openweathermap.org/data/2.5/forecast?id={city_id}&appid={token}&lang=pt'
        url = url.format(city_id=city_id, token=self._token)

        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()

            result = 'As informações climáticas para {}'.format(
                data['city']['name'])
            result += ' no dia {} são: \n'.format(date.strftime('%d-%m-%Y'))

            for day in data['list']:
                dt = datetime.datetime.strptime(
                    day['dt_txt'], '%Y-%m-%d %H:%M:%S')
                temp_max = float(day['main']['temp_max'])
                temp_max = self._kelvin2celsius(temp_max)

                temp_min = float(day['main']['temp_min'])
                temp_min = self._kelvin2celsius(temp_min)

                description = day['weather'][0]['description']

                if date.day == dt.day and date.month == dt.month and date.year == dt.year:
                    result += '* {}\n'.format(description)
                    result += '\tÀs {} máxima de {}°C e mínima {}°C\n'.format(
                        dt.strftime('%H:%M'),
                        temp_max,
                        temp_min
                    )
            return result
        elif r.status_code == 404:
            return "A cidade não foi encontrada na API."


if __name__ == "__main__":
    w = Weather()
    w.fetch(city_id=3663517, date=datetime.datetime.now())
