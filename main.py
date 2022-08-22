from parsing import get_jobs_links, get_job_description, parse_text
from job import Job

jobs_links = get_jobs_links()

result = []
for job_link in jobs_links:
    job = Job()

    job_soup = get_job_description(job_link)

    jobs_inf = job_soup.find(id="__nuxt").find_all("p")

    job.set_title(job_soup.find(id="__nuxt").find("h1").text)

    for job_inf in jobs_inf:
        job = parse_text(job_inf.text, job)

    result.append(job.to_json())
print(result)
