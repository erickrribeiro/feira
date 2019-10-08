# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction


# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message("Hello World!")
#
#         return []

class WeatherForm(FormAction):

    def name(self):
        return "weather_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print('required_slots')
        """A list of required slots that the form has to fill"""

        return ["location"]

    def slot_mappings(self):
        print('slot_mappings')
        return {"location":
                self.from_entity(entity="location"),
                # "again": [
                #     self.from_intent(intent='affirm', value=True),
                #     self.from_intent(intent='deny', value=False)
                # ]
                }

    def validate_location(self,
                          value: Text,
                          dispatcher: CollectingDispatcher,
                          tracker: Tracker,
                          domain: Dict[Text, Any]) -> Dict[Text, Any]:
            dispatcher.utter_message('validate location', tracker)
            return {"location": value}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        print('submit')
        # utter submit template
        self._activate_if_required(dispatcher, tracker, domain)
        dispatcher.utter_template('utter_submit', tracker)
        dispatcher.utter_template('utter_ask_again', tracker)

        return [SlotSet("location", None)]

