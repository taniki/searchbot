from rasa_core_sdk import Action
from rasa_core_sdk.forms import FormAction
from rasa_core_sdk.events import SlotSet
import requests

class ActionSetQuery(Action):
    def name(self):
        return "action_set_query"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("query", tracker.latest_message.text)
        ]


class ActionCheckResults(Action):
    def name(self):
        return "action_check_results"

    def run(self, dispatcher, tracker, domain):
        url = "https://www.data.gouv.fr/api/1/datasets/"

        #print(tracker.latest_message)
        message = tracker.latest_message['text']
        # "q": tracker.get_slot("query")
        params = {
            "q": message
        }

        data = requests.get(url, params=params).json()

        results = data["data"][0:5]
        total = data['total']

        if(total > 0):
            for r in results:
                dispatcher.utter_message(r['page'])

        dispatcher.utter_message("résultats: {}".format(total))

        return [
            SlotSet("results", results),
            SlotSet("total", data["total"])
        ]


class ActionGiveResults(Action):
    def name(self):
        return "action_give_results"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_victory", tracker)
        # dispatcher.utter_response(tracker.get_slot("results"))
        # return [ SlotSet("results", []) ]

        return [ ]

class SearchForm(FormAction):
   def name(self):
       return "search_form"

   @staticmethod
   def required_slots(tracker):
       # type: () -> List[Text]
       """A list of required slots that the form has to fill"""

       return ["query"]

   def submit(self, dispatcher, tracker, domain):
       # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict]
       """Define what the form has to do
           after all required slots are filled"""

       # utter submit template
       dispatcher.utter_template('utter_submit', tracker)
       return []
