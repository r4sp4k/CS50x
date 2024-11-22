# Skills Visualizer
#### Video Demo: https://youtu.be/Fa1AWXxVpSo
#### Description:
For people working in the field of information technology, learning new skills is crucial as IT is constantly evolving at a rapid pace. Considering a person working in the field that is keen on learning new technologies and adding new skills into his or hers arsenal, the complication may arise when prioritizing on what to add next to that person's skillset. There might be various kinds of motivation from the sheer necessity of gaining new skill in order to be able carry out newly emerging day to day tasks in the current workplace or simply wanting to learn something new. There might be another approach to let the market decide which skills are the most demanded and highly valued. This is where the skills visualizer comes to the rescue. 

## The script overview
Skills visualizer script sends a get request to a pre-defined url (set to query a popular job portal in Slovakia), scrapes related job offers and parses them. Parsed details including job title, employer, salary, job details hyperlink and filtered skills (based on the skills list) are saved into a CSV file which can serve as a concise overview of current job offers. A saved csv is then further processed (only salary and skills columns) and a treemap is created visualising the most demanded skills in the field and also their valuation on the market. A helper script file is used to provide a randomized requests and headers, the file also contains lists of skills to be matched.

## The treemap
The treemap is the final output of the script. It shows most demanded skills (larger square means more demand) and the average salary for that skill (greener field means higher salary).

## Modules used:

Modules that are part of Python's standard library:

- **csv:** Provides functionality to read from and write to CSV files.<br />
- **random:** Provides functions for generating random numbers.<br /> 
- **re:** Provides regular expression matching operations.<br />
- **time:** Provides time-related functions, such as pausing the execution of a program.<br />


Third-party libraries that need to be pip installed:
- **beautifulsoup4:** Used for web scraping and parsing HTML/XML<br />
- **cloudscraper:** Handles bypassing anti-bot measures for Cloudflare-protected sites.<br />
- **matplotlib** Used for creating visualizations.<br />
- **pandas:** Provides data manipulation and analysis.<br />
- **requests:** For making HTTP requests.<br />
- **squarify:** Generates treemaps for data visualization.

## Functions used:
**1. main():** <br />Orchestrates the script workflow by invoking scraping, parsing, saving data to a CSV, and generating a treemap visualization.<br />
**2. scrape_jobs():**<br /> Scrapes job listings from specified pages of a job portal. Collects job title, employer, location, salary, link, and skills details.<br />
**3. parse_job_skills():**<br /> Extracts and standardizes skills from job descriptions using regex patterns and predefined skill lists.<br />
**4. parse_job_salary():**<br /> Extracts and processes salary details. It computes average salaries for ranges and handles rates in unknown formats (e.g. other currencies).<br />
**5. parse_job_location():**<br /> Classifies job locations into categories like "Remote," "Bratislava HO" when working from home is possible or "Bratislava" using regex patterns.<br />
**6. write_csv():**<br /> Saves parsed job data (title, employer, location, salary, link, and skills) into a CSV file.<br />
**7. generate_treemap():**<br /> Creates a treemap visualization. It shows the demand (size of blocks) and average salary (color intensity) for each skill.<br />
**8. wait_a_sec():**<br /> A helper function used while scraping to randomize delays between get requests in seconds as we don't want to hammer the website with unhumanly high cadence.<br />


### Flow of Execution
1, Display a message indicating the start of web scraping.<br />
2, Fetch job listings from a job portal.<br />
3, Extract details into list of dictionaries (dict keys: job title, employer, location, salary, link, skills).<br />
4, Parse Skills - Extract and filter skills using predefined patterns.<br />
5, Parse Salary - Process salary data, calculating averages and handling special cases.<br />
6, Categorize job locations according to possibility of remote work.<br />
7, Write the cleaned and structured data into a CSV file.
8, Display a message to notify csv has been written.<br />
8, Generate Visualization in the form of a treemap.<br />
9, Display a completion message and show the treemap.