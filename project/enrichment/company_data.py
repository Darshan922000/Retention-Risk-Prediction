import os
from dotenv import load_dotenv
load_dotenv()
from project.logging.logger import logging

os.environ["REVERSE_API_KEY"] = os.getenv("REVERSE_API_KEY")

import requests

def get_company_data(linkedin_url):
    logging.info(f"Fetching company data for LinkedIn URL: {linkedin_url}")
    url = "https://api.reversecontact.com/enrichment/company"

    # Your API key
    api_key = os.environ["REVERSE_API_KEY"]

    # LinkedIn URL of the company you want information about
    linkedin_url = linkedin_url
    # "https://www.linkedin.com/company/digy4official/"
    #"https://www.linkedin.com/company/yelp-com/"
    # "https://www.linkedin.com/company/microsoft/"

    # Prepare query parameters
    params = {
        "apikey": api_key,
        "linkedInUrl": linkedin_url
    }

    # Send GET request
    response = requests.get(url, params=params)

    # Print the company data
    if response.status_code == 200:
        company_data = response.json()
        company = company_data["company"]
        print(company)
        logging.info(f"Successfully received company data from API: {company}")

    elif response.status_code == 429:
            print("Rate limit hit. Waiting before retry...")
            # time.sleep(60)  # wait for 60 seconds before retry
    else:
        print("Error:", response.status_code, response.text)

    
    # Parse the important company fields
    company_name = company.get("name", "N/A")
    industry = company.get("industry", "N/A")
    employee_count = company.get("employeeCount", "N/A")
    website_url = company.get("websiteUrl", "N/A")
    follower_count = company.get("followerCount", "N/A")

    # Handle fundingData safely
    funding_data = company.get('fundingData')

    if funding_data is None:
        funding_rounds = "N/A"
        lead_investors = "N/A"
        lead_investors_url = "N/A"
    else:
    
        funding_rounds = funding_data.get('numberOfFundingRounds', "N/A")
        lead_investors_list = funding_data.get("lastFundingRound", {}).get("leadInvestors", [])
        
        lead_investors = lead_investors_list[0].get('name', "N/A")
        lead_investors_url = lead_investors_list[0].get('url', "N/A")


    # Create the company data dictionary
    company_data = {
        'company_name': company_name,
        'industry': industry,
        'employee_count': employee_count,
        'website_url': website_url,
        'follower_count': follower_count,
        'funding_rounds': funding_rounds,
        'lead_investor': lead_investors,
        'lead_investor_url': lead_investors_url
        }
    
    return company_data


