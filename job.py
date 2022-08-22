import json


class Job:
    def __init__(self):
        self.title = None
        self.place = None
        self.salary = None
        self.contract_type = None
        self.contact_email = None

    def set_attribute(self, name, value):
        setattr(self, name, value)

    def to_json(self):
        return json.dumps(vars(self), ensure_ascii=False)
