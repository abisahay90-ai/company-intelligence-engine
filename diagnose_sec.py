import requests, json

USER_AGENT = "CompanyIntelligenceEngine abi.sahay90@gmail.com"
cik        = "0001318605"
cik_short  = "1318605"

# Get Tesla's latest 10-K
url  = f"https://data.sec.gov/submissions/CIK{cik}.json"
data = requests.get(url, headers={"User-Agent": USER_AGENT}).json()

forms        = data["filings"]["recent"]["form"]
accessions   = data["filings"]["recent"]["accessionNumber"]
primary_docs = data["filings"]["recent"]["primaryDocument"]

for i, form in enumerate(forms):
    if form == "10-K":
        acc = accessions[i].replace("-", "")
        doc = primary_docs[i]
        print(f"10-K accession : {acc}")
        print(f"Primary doc    : {doc}")

        idx_url = f"https://www.sec.gov/Archives/edgar/data/{cik_short}/{acc}/index.json"
        r2      = requests.get(idx_url, headers={"User-Agent": USER_AGENT})

        if r2.status_code == 200:
            files = r2.json().get("directory", {}).get("item", [])
            print(f"\nFiles in filing ({len(files)} total):")
            for f in files[:20]:
                name = f.get("name", "")
                size = f.get("size", "?")
                print(f"  {name:50s} {size} bytes")
        break