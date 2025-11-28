import requests
import xmltodict
import json

FLEXOFFERS_API_KEY = "beb20686-606a-4e92-8c71-bfa967317ddc"
FLEXOFFERS_BASE_URL = "https://api.flexoffers.com/v3"

def test_flexoffers():
    print("Testing FlexOffers API...")
    try:
        url = f"{FLEXOFFERS_BASE_URL}/domains"
        headers = {
            "accept": "application/xml",
            "apiKey": FLEXOFFERS_API_KEY
        }
        
        print(f"Sending request to {url}")
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = xmltodict.parse(response.text)
            # print(json.dumps(data, indent=2))
            domains = data.get("domains", {}).get("domain", [])
            count = len(domains) if isinstance(domains, list) else 1
            print(f"Success! Found {count} domains.")
            if count > 0:
                print("First domain sample:")
                print(json.dumps(domains[0] if isinstance(domains, list) else domains, indent=2))
        else:
            print(f"Failed. Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_flexoffers()
