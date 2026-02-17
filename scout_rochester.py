import requests
import urllib3

# Mutes the security warning
urllib3.disable_warnings()

def scout_property(address):
    url = "https://maps.cityofrochester.gov/server/rest/services/Open_Data/Tax_Parcels_Open_Data/FeatureServer/0/query"
    
    # IMPROVEMENT: We use '%' as a wildcard so 'Church' matches '30 CHURCH ST'
    clean_address = address.upper().strip()
    
    params = {
        'where': f"SITEADDRESS LIKE '%{clean_address}%'",
        'outFields': 'SITEADDRESS,OWNERNME1,CURRENT_TOTAL_VALUE,SALE_PRICE,ZONING',
        'f': 'json',
        'returnGeometry': 'false',
        'resultRecordCount': 5  # Show up to 5 matches if the search is broad
    }

    try:
        response = requests.get(url, params=params, verify=False)
        data = response.json()
        
        features = data.get('features', [])
        if not features:
            print(f"❌ No property found for '{address}'. Try just the street name.")
            return

        print(f"\n✅ Found {len(features)} match(es):")
        for item in features:
            props = item['attributes']
            print(f"---")
            print(f"📍 Address: {props['SITEADDRESS']}")
            print(f"👤 Owner:   {props['OWNERNME1']}")
            print(f"💰 Value:   ${props['CURRENT_TOTAL_VALUE']:,}")
            print(f"🏷️ Sale:    ${props['SALE_PRICE']:,}")
            print(f"🏗️ Zoning:  {props['ZONING']}")
        print("---\n")

    except Exception as e:
        print(f"⚠️ Connection Error: {e}")

if __name__ == "__main__":
    target = input("Enter Address (or part of one): ")
    scout_property(target)
