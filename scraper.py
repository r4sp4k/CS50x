from bs4 import BeautifulSoup
import requests
import cloudscraper
import re
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import squarify
import scraper_helpers

base_url = "https://www.profesia.sk"
search_url = "https://www.profesia.sk/praca/bratislava/?positions[]=740&positions[]=89&radius=radius30&search_anywhere=linux+engineer%2C+linux+admin&sort_by=relevance"
search_suffix = "&page_num="
headers = scraper_helpers.headers


def main():
    print("Scraping web, this may take a while...")
    scraped_data = scrape_jobs(search_url, search_suffix, base_url, headers)
    parsed_skillsets = parse_job_skills(scraped_data)
    parsed_salaries = parse_job_salary(parsed_skillsets)
    parsed_locations = parse_job_location(parsed_salaries)
    write_csv(parsed_locations)
    print("Scraped data written to CSV file :)")
    print("Rendering treemap...")
    generate_treemap()
    

def scrape_jobs(search_url, search_suffix, base_url, headers):
    all_jobs = []
    scraper = cloudscraper.create_scraper()

    # loop over search_url result pages
    for page_number in range(1,7):
        print(f"Fetching job offers from page {page_number}...")
        response = scraper.get(f"{search_url}{search_suffix}{page_number}",headers = headers)
        soup = BeautifulSoup(response.text, "html.parser")
        if page_number > 1:
            scraper_helpers.wait_a_sec(1, 3)
        job_offers = soup.find_all("li", class_="list-row")
        for idx, offer in enumerate(job_offers):
            #print(f"Scraping job offer {idx + 1} on page {page_number}...")
            if idx > 1:
                scraper_helpers.wait_a_sec(2, 4)

            # Find <span> containing the title, employer, location information
            job_title = offer.find("span", class_="title").text.strip() if offer.find("span", class_="title") else "N/A"
            if job_title.startswith("Pracovné ponuky e-mailom"):
                continue
            employer = offer.find("span", class_="employer").text.strip() if offer.find("span", class_="employer") else "N/A"
            job_location = offer.find("span", class_="job-location").text.strip() if offer.find("span", class_="job-location") else "N/A"
            
            # Find <span> containing the salary information
            salary_span = offer.find("span", class_="label label-bordered green half-margin-on-top")
            salary = salary_span.text.strip() if salary_span else "N/A"
            
            # Get link from the <a> tag
            link_tag = offer.find("a", href=True, id=True)
            link = link_tag["href"] if link_tag else "N/A"

            # Get details from the link
            job_url = f"{base_url}{link}"
            response_details = requests.get(f"{job_url}", headers=headers)
            soup_details = BeautifulSoup(response_details.text, "html.parser")

            job_details = None
            if employer.startswith("ESET"):
                job_details = soup_details.find("div", class_="mb-3s mb-md-5 mb-lg-8").text.lower().strip()
            elif employer.startswith("GoHealth"):
                job_details = soup_details.find("div", class_="gh-container").text.lower().strip()
            elif employer.startswith("Raiffeisen Informatik"):
                job_details = soup_details.find("section", class_="raiffeisen-informatik-container").text.lower().strip()
            elif employer.startswith("Erste Digital"):
                job_details = soup_details.find("div", class_="card card-content").text.lower().strip()
            else:
                try:
                    job_details = soup_details.find("div", attrs={"class": "details", "itemprop": "description"}).text.lower().strip()
                except AttributeError:
                    # Find all div tags with class "details-section"
                    details_sections = soup_details.find_all("div", class_="details-section")
                    # Concatenate text content from all "details-section" divs
                    job_details = ""
                    for section in details_sections:
                        
                        # Add space between sections for readability
                        job_details += section.text.lower().strip() + " "  

            job_details = re.sub(r"•\s+\w+|^\s*$", "", job_details, flags=re.MULTILINE) 
            job_details = re.sub(r"(\n\s*\n)+", "\n", job_details).strip()

            # Store scraped details for each job
            job_data = {
                "Job Title": job_title,
                "Employer": employer,
                "Location": job_location,
                "Salary": salary,
                "Link": job_url,
                "Skills": job_details
            }
            all_jobs.append(job_data)
            
    return all_jobs


def parse_job_skills(jobs_skills):
    for job in jobs_skills:
        text = job['Skills']
        
        # Substring matched skills
        escaped_skills = (re.escape(word) for word in scraper_helpers.skills)
        skills_pattern = r'(?:' + '|'.join(escaped_skills) + r')'
        skills_regex = re.compile(skills_pattern, re.IGNORECASE)
        
        # Whole-word matched skills
        escaped_skills_ww = (re.escape(word) for word in scraper_helpers.skills_ww)
        skills_ww_pattern = r'\b(?:' + '|'.join(escaped_skills_ww) + r')\b'
        skills_ww_regex = re.compile(skills_ww_pattern, re.IGNORECASE)

        # Find matches for substring matched skills
        skills_matches = skills_regex.findall(text)
        
        # Some words post processing / category inclusion
        for replacement, terms in scraper_helpers.replacement_map.items():
            skills_matches = [replacement if skill in terms else skill for skill in skills_matches]
       
        skills_matches = set(skills_matches)

        skills_ww_matches = skills_ww_regex.findall(text)
        
        # Some whole words post processing / category inclusion
        for replacement_ww, terms_ww in scraper_helpers.replacement_ww_map.items():
            skills_ww_matches = [replacement_ww if skill_ww in terms_ww else skill_ww for skill_ww in skills_ww_matches]

        skills_ww_matches = set(skills_ww_matches)
          
        job['Skills'] = sorted(skills_matches | skills_ww_matches)

    return jobs_skills


def parse_job_salary(jobs_salary):
    salary_regex = re.compile(r"^(?:Od\s+)?(\d[\d ]+)(?:\s*-\s*(\d[\d ]+))?\s*(EUR/(?:mesiac|hodinu|hour|hod))?$", re.IGNORECASE)
    for job in jobs_salary:
        text = job['Salary']
        match = salary_regex.match(text)
        if match:
            if "hod" in match.group(3) or "hour" in match.group(3):
                job['Salary'] = "Hourly rate"
                break
            else:
                
                # Extract min and max values
                min_salary = int(match.group(1).replace(" ", ""))
                max_salary = int(match.group(2).replace(" ", "")) if match.group(2) else min_salary
                
                # Calculate the average if range, else return the single value
                average_salary = round((min_salary + max_salary) / 2)
                job['Salary'] = average_salary
        else:
            # when job salary listed in other currency
            job['Salary'] = "Unknown format"

    return jobs_salary    


def parse_job_location(jobs_locations):
    
    # Define standard location patterns
    remote_patterns = [r"Prác[ae] z domu", r"Remote work"]
    bratislava_ho_patterns = [r"Bratislava.*\(Pozícia umožňuje občasnú prácu z domu\)", r"Bratislava.*\(Job with occasional home office\)"]
    bratislava_pattern = r"Bratislava"
    ho_patterns = [r"\(Pozícia umožňuje občasnú prácu z domu\)", r"\(Job with occasional home office\)"]

    # Compile patterns
    remote_regex = re.compile("|".join(remote_patterns))
    bratislava_ho_regex = re.compile("|".join(bratislava_ho_patterns))
    bratislava_regex = re.compile(bratislava_pattern)
    ho_regex = re.compile("|".join(ho_patterns))
    for job in jobs_locations:
        text = job["Location"]
        if remote_regex.search(text):
            job["Location"] = "Remote"
        elif bratislava_ho_regex.search(text):
            job["Location"] = "Bratislava HO"
        elif bratislava_regex.search(text):
            job["Location"] = "Bratislava"
        elif ho_regex.search(text):
            
            # Replace the ho_pattern with "HO"
            job["Location"] = re.sub(ho_regex, "HO", text)
    return jobs_locations


def write_csv(parsed_jobs):
    with open("jobs.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Job Title", "Employer", "Location", "Salary", "Link", "Skills"])
        writer.writeheader()
        for job in parsed_jobs:
            writer.writerow({
                "Job Title": job["Job Title"],
                "Employer": job["Employer"],
                "Location": job["Location"],
                "Salary": job["Salary"],
                "Link": job["Link"],
                "Skills": ", ".join(job["Skills"])
            })


def generate_treemap():
    data = pd.read_csv("jobs.csv", usecols=["Salary", "Skills"])
    data = data[data['Salary'] != 'Unknown format']
    data['Salary'] = pd.to_numeric(data['Salary'])

    # Split skills list into individual entries
    skills_expanded = data['Skills'].str.split(', ').explode()

    # Create skills salaries DataFrame
    skills_salary = pd.DataFrame({
        'Skill': skills_expanded,
        'Salary': data.loc[skills_expanded.index, 'Salary']
    })

    # Group by skill to calculate demand and salary
    skill_data = skills_salary.groupby('Skill').agg(
        frequency=('Skill', 'size'),  # Count occurrences of each skill
        avg_salary=('Salary', 'mean') # Calculate average salary for each skill
    ).reset_index()

    # Salary for colormap
    norm = matplotlib.colors.Normalize(vmin=skill_data['avg_salary'].min(), vmax=skill_data['avg_salary'].max())
    colors = [matplotlib.cm.Greens(norm(value)) for value in skill_data['avg_salary']]

    # Create treemap
    plt.figure(figsize=(12, 8))
    squarify.plot(
        sizes = skill_data['frequency'], # Size by demand
        label = skill_data['Skill'],     # Skill names as labels
        color = colors,                  # Colors by average salary
        alpha = 0.8,                     # Transparency
    )

    # Add a colorbar to indicate salary
    ax = plt.gca()  
    sm = plt.cm.ScalarMappable(cmap='Greens', norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)  

    # Axis for the colorbar
    cbar.set_label('Average Monthly Salary in Euros', rotation=270, labelpad=15)
    plt.title('Linux-Related Skills Demand (Higher Salary Is Greener)', fontsize=14)
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    main()