# 🚀 Outreach Automation System
This is a cold outreach automation system designed to scrape UAE-based textile companies, generate personalized cold emails using AI, and populate the results in a Google Sheet.

---

## 🧰 Features
- Scrapes UAE textile company websites using SerpAPI
- Generates personalized cold emails using Groq-hosted LLMs (e.g., llama-3.3-70b-versatile)
- Populates data into Google Sheets automatically

---

## 🚀 How It Works
- Scraping : Uses SerpAPI to search for "textile company UAE official website"
- Domain Extraction : Parses domains from URLs using tldextract
- Email Drafting : Uses Groq's hosted LLM (llama-3.3-70b-versatile) to write cold emails
- Sheet Population : Uploads the scraped companies and generated emails to a Google Sheet

---

## 🛠️ Setup Instructions
1. Get API Keys
 - SerpAPI : https://serpapi.com/manage-api-key
 - Groq API Key : https://console.groq.com/keys
2. Set Up Google Sheets Access
 - Go to Google Cloud Console
 - Create a new project or use an existing one
 - Enable Google Sheets API
 - Create a Service Account and download the .json key
 - Share your Google Sheet with the service account email
 - Save the JSON file as service_account.json in your project root
3. Create Your Google Sheet
 - Create a blank Google Sheet and copy its ID from the URL:
   - Example URL:
   - https://docs.google.com/spreadsheets/d/1aBcD.../edit#gid=0
 - Use only the ID part: 1aBcD...
 - Update .env with the correct sheet ID

---

## 📌 Google sheet link
- [link here](https://docs.google.com/spreadsheets/d/e/2PACX-1vR1oh2rL0KzDbM80m4k7_Bx0kxLlPk7-G6AoCOwOgNpehyWnzad0ZvvCqN3Jf2X1D_P76pnVntUG9vz/pubhtml)
