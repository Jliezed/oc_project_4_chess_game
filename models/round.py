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
            self.start_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            return self.start_date
        else:
            self.start_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            return self.start_date

    def define_end_date(self):
        self.end_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        return self.end_date

    def round_to_dict(self):
        round_dict = {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "matches": self.matches,
        }
        return round_dict
