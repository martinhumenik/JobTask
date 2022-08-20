import requests
import re
import json
from bs4 import BeautifulSoup

url = "https://www.hyperia.sk/kariera/"
main_page = requests.get(url)

main_soup = BeautifulSoup(main_page.content, "html.parser")
jobs_links = main_soup.find(id="positions").find_all("a")

contract_types = ["TPP", "živnosť", "dohoda", "skrátený úväzok"]
result = []
for job_link in jobs_links:
    job_page = requests.get("https://www.hyperia.sk" + job_link["href"])
    job_soup = BeautifulSoup(job_page.content, "html.parser")

    jobs_inf = job_soup.find(id="__nuxt").find_all("p")

    job_title = job_soup.find(id="__nuxt").find("h1").text
    job_place = ""
    job_salary = ''
    contract_type_str = ''
    contact_email = ''
    for job_inf in jobs_inf:
        ji_t = job_inf.text

        if "Miesto výkonu práce:" in ji_t:
            job_place = ji_t.split(":")[-1]

        elif "Platové ohodnotenie" in ji_t:
            job_salary = ji_t[ji_t.find("Platové ohodnotenie"):ji_t.find(",")].replace("Platové ohodnotenie", "")

        elif "Typ pracového pomeru" in ji_t:
            contract_type_set = set(contract_type for contract_type in contract_types if contract_type in ji_t)
            contract_type_str = " ,".join(contract_type_set)

        elif "@" in ji_t:
            contact_email = "".join(re.findall(r'[\w.]+@[\w.]+', ji_t))

    result.append(json.dumps({"title": job_title,
                              "place": job_place,
                              "salary": job_salary,
                              "contract_type": contract_type_str,
                              "contact_email": contact_email},
                             ensure_ascii=False))
print(result)
