import requests
import re
from bs4 import BeautifulSoup

URL = "https://www.hyperia.sk/kariera/"
CONTRACT_TYPES = ["TPP", "živnosť", "dohoda o brig. práci študenta", "skrátený úväzok"]


def get_jobs_links():
    main_page = requests.get(URL)

    main_soup = BeautifulSoup(main_page.content, "html.parser")
    jobs_links = main_soup.find(id="positions").find_all("a")

    return jobs_links


def get_job_detail(job_link):
    job_page = requests.get("https://www.hyperia.sk" + job_link["href"])
    job_soup = BeautifulSoup(job_page.content, "html.parser")

    return job_soup


def parse_job_informations(ji_t, job):
    if "Miesto výkonu práce:" in ji_t:
        job.set_place(ji_t.split(":")[-1])

    if "Platové ohodnotenie" in ji_t:
        job.set_salary(ji_t[ji_t.find("Platové ohodnotenie"):ji_t.find(",")].replace("Platové ohodnotenie", ""))

    if "Typ pracového pomeru" in ji_t:
        contract_type_set = set(contract_type for contract_type in CONTRACT_TYPES if contract_type in ji_t)
        job.set_contract_type(" ,".join(contract_type_set))

    if "@" in ji_t:
        job.set_contact_email("".join(re.findall(r"[\w.]+@[\w.]+", ji_t)))

    return job
