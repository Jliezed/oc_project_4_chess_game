from models.match import Match
from datetime import datetime

class Round:
    def __init__(self, name="", start_date="", end_date=""):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.matches = []

    # def __repr__(self):
    #     """ Better representation of a tournament instance"""
    #     return (
    #         f"Name: {self.name} - Start Date: {self.start_date} - End Date: {self.end_date} - Matches: {self.matches}"
    #     )

    def define_start_date(self):
        if self.start_date == "":
            today = datetime.now().strftime("%d/%m/%Y")
            self.start_date = today
            return self.start_date
        else:
            self.start_date = datetime.now()
            return self.start_date

    def insert_matches(self, matches):
        self.matches = matches
        return self.matches

    def round_to_dict(self, round_obj):
        round_dict = {
            "name": round_obj.name,
            "start_date": round_obj.start_date,
            "end_date": round_obj.end_date,
            "matches": round_obj.matches,
        }
        return round_dict
