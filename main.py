from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from project.system.graph import email
from project.enrichment.company_data import get_company_data
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the absolute path to the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Print current directory for debugging
print(f"Current directory: {current_dir}")

# Set correct paths for static files
css_dir = os.path.join(current_dir, "css")
js_dir = os.path.join(current_dir, "js")

# Ensure directories exist
print(f"CSS directory exists: {os.path.exists(css_dir)}")
print(f"JS directory exists: {os.path.exists(js_dir)}")

# Mount static files
app.mount("/css", StaticFiles(directory=css_dir), name="css")
app.mount("/js", StaticFiles(directory=js_dir), name="js")

class EmailRequest(BaseModel):
    client_name: str
    policy_type: str
    policy_start_date: str
    annual_premium: float
    claims_last_3_years: int
    communication_frequency: str
    client_tenure_years: int
    industry: str
    region: str
    risk_score: str

class EnrichmentRequest(BaseModel):
    company_linkedin_url: str

@app.post("/generate_email")
async def generate_email(data: EmailRequest):
    result = email.invoke({"input_data": data})
    return result["response"].content

@app.post("/enrich_company")
async def enrich_company(data: EnrichmentRequest):
    linkedin_url = data.company_linkedin_url
    company_data = get_company_data(linkedin_url)
    return company_data

@app.get("/")
async def read_index():
    index_path = os.path.join(current_dir, "index.html")
    print(f"Index path: {index_path}")
    print(f"Index file exists: {os.path.exists(index_path)}")
    return FileResponse(index_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

  
    

# {
#   "client_name": "darshan",
#   "policy_type": "car",
#   "policy_start_date": "last month",
#   "annual_premium": 5000,
#   "claims_last_3_years": 2,
#   "communication_frequency": "monthly",
#   "client_tenure_years": 3,
#   "industry": "auto",
#   "region": "durham",
#   "risk_score": "medium"
# }