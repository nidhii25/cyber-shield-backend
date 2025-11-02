from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
import requests, os, time
# from dotenv import load_dotenv

# load_dotenv()

router = APIRouter(prefix="/phishing", tags=["Phishing Detection"])

class PhishingDetectionRequest(BaseModel):
    url: str        

API_KEY = "dc563939964e2e36636a3a12c62825d9c213d37f49eb32323497080cba14b341"
API_URL = "https://www.virustotal.com/api/v3/urls"

@router.post("/predict")
def detect_phishing(request: PhishingDetectionRequest):
    try:
        url = request.url
        headers = {"x-apikey": API_KEY}

        # Submit URL for scanning
        response = requests.post(API_URL, headers=headers, data={"url": url})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        scan_id = response.json()["data"]["id"]

        # Wait briefly for the analysis to complete
        time.sleep(5)

        # Retrieve scan result
        result = requests.get(f"https://www.virustotal.com/api/v3/analyses/{scan_id}", headers=headers)
        if result.status_code != 200:
            raise HTTPException(status_code=result.status_code, detail="Error fetching analysis from VirusTotal API")

        analysis = result.json()["data"]["attributes"]["stats"]
        malicious = analysis.get("malicious", 0)
        suspicious = analysis.get("suspicious", 0)

        if malicious > 0:
            verdict = "Phishing"
            is_phishing = True
        elif suspicious > 0:
            verdict = "Suspicious"
            is_phishing = True
        else:
            verdict = "Legitimate"
            is_phishing = False

        return {
            "url": url,
            "verdict": verdict,
            "is_phishing": is_phishing
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))