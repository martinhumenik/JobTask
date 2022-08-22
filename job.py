import json


class Job:
    def __init__(self):
        self.title = None
        self.place = None
        self.salary = None
        self.contract_type = None
        self.contact_email = None

    def set_title(self, value):
        self.title = value

    def set_place(self, value):
        self.place = value

    def set_salary(self, value):
        self.salary = value

    def set_contract_type(self, value):
        self.contract_type = value

    def set_contact_email(self, value):
        self.contact_email = value

    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)