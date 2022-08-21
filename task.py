import requests
import re
import json
from bs4 import BeautifulSoup


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


url = "https://www.hyperia.sk/kariera/"
main_page = requests.get(url)

main_soup = BeautifulSoup(main_page.content, "html.parser")
jobs_links = main_soup.find(id="positions").find_all("a")

contract_types = ["TPP", "živnosť", "dohoda", "skrátený úväzok"]
result = []
for job_link in jobs_links:
    job = Job()

    job_page = requests.get("https://www.hyperia.sk" + job_link["href"])
    job_soup = BeautifulSoup(job_page.content, "html.parser")

    jobs_inf = job_soup.find(id="__nuxt").find_all("p")

    job.set_title(job_soup.find(id="__nuxt").find("h1").text)

    for job_inf in jobs_inf:
        ji_t = job_inf.text

        if "Miesto výkonu práce:" in ji_t:
            job.set_place(ji_t.split(":")[-1])

        if "Platové ohodnotenie" in ji_t:
            job.set_salary(ji_t[ji_t.find("Platové ohodnotenie"):ji_t.find(",")].replace("Platové ohodnotenie", ""))

        if "Typ pracového pomeru" in ji_t:
            contract_type_set = set(contract_type for contract_type in contract_types if contract_type in ji_t)
            job.set_contract_type(" ,".join(contract_type_set))

        if "@" in ji_t:
            job.set_contact_email("".join(re.findall(r"[\w.]+@[\w.]+", ji_t)))

    result.append(job.to_json())
print(result)
