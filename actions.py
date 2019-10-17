# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
import requests
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction


class WeatherAction(Action):

    def name(self) -> Text:
        return "weather_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        has_location = True
        if 'entities' in tracker.latest_message:
            entities = [
                entity['value'] for entity in tracker.latest_message['entities'] if entity['entity'] == 'location'
            ]

            print(entities)
            if len(entities) > 0:
                name = ' '.join(entities)
                r = requests.get(
                    'http://localhost:5000/weather/{}'.format(name))
                data = r.json()
                dispatcher.utter_message(data['message'])
            else:
                has_location = False
        else:
            has_location = False

        if not has_location:
            dispatcher.utter_message(
                'Informe o nome de uma cidade ou estado situado no Brasil.'
            )

        return [UserUtteranceReverted()]
