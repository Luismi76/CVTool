from app import create_app
import json
import sys

try:
    app = create_app('testing')
    client = app.test_client()
    
    # Mock data for the request
    data = {
        "selection": {
            "include_summary": True,
            "skills": {"selected": [0], "order": [0]}
        }
    }

    print("Sending POST request to /preview/fragment...")
    response = client.post('/preview/fragment', 
                          data=json.dumps(data),
                          content_type='application/json')
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        json_response = response.get_json()
        if not json_response:
             print("ERROR: Empty JSON response")
        elif 'html' in json_response:
             html = json_response['html']
             print(f"Success! HTML Length: {len(html)}")
             print("HTML Preview (first 200 chars):")
             print(html[:200])
        elif 'error' in json_response:
             print(f"Backend returned error: {json_response['error']}")
        else:
             print(f"Unexpected JSON structure: {json_response.keys()}")
    else:
        print("Request failed!")
        print(response.get_data(as_text=True))

except Exception as e:
    print(f"\nCRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
