import os
import tldextract
from dotenv import load_dotenv

from langchain_community.utilities import SerpAPIWrapper

from langchain_groq import ChatGroq

import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

# ── Configure your tools ───────

# Search (will pull top 5 results)
search = SerpAPIWrapper(
    serpapi_api_key=os.getenv("SERPAPI_API_KEY"),
    params={"num_results": 5, "engine": "google"},
)

# LLM 
llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
)


# Sheets init
def init_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        [
            "https://spreadsheets.google.com/feeds ",  
            "https://www.googleapis.com/auth/drive ",  
        ],
    )
    sheet = gspread.authorize(creds).open_by_key(os.getenv("SHEET_ID")).sheet1
    sheet.clear()
    sheet.append_row(["Name", "Website", "Email", "Cold Email"])
    return sheet


# ── Pipeline steps ─────────


def scrape_uae_textile_companies():
    """
    Run a Google-powered search for 'textile company UAE official website'
    and return up to 5 companies as dicts with name, website, and domain.
    """
    query = "textile company UAE official website"
    raw_results = search.results(query)

    # Extract organic results list
    results = raw_results.get("organic_results", [])

    if not results:
        raise RuntimeError("No search results—check your SERPAPI_API_KEY or quota.")

    companies = []
    for item in results[:5]:  
        url = item.get("link")
        if not url:
            continue
        ext = tldextract.extract(url)
        domain = f"{ext.domain}.{ext.suffix}"
        name = ext.domain.replace("-", " ").title()
        companies.append(
            {"name": name, "website": f"https://{domain}", "domain": domain}
        )
    return companies


def draft_email(name: str, site: str) -> str:
    """
    Use llama via Groq to draft your cold outreach email.
    """
    prompt = f"""
You are a sales outreach assistant.
Draft a concise, personalized cold email to the decision maker at {name} ({site}) in the textile industry, offering our cutting‑edge fabric sourcing platform.
Include:
- A friendly opening line
- One sentence explaining our USP
- A clear call to action
Keep it under 120 words.
"""
    resp = llm.invoke(prompt)
    return resp.content.strip()


def guess_email(domain: str) -> str:
    """Naïvely guess an email address."""
    return f"info@{domain}"


def main():
    # 1. Scrape
    companies = scrape_uae_textile_companies()

    # 2. Init Sheet
    sheet = init_sheet()

    # 3. Loop & populate
    for comp in companies:
        email = guess_email(comp["domain"])
        cold = draft_email(comp["name"], comp["website"])
        sheet.append_row([comp["name"], comp["website"], email, cold])
        print("→ Added:", comp["name"])


if __name__ == "__main__":
    main()
