from http.server import BaseHTTPRequestHandler
import json
import phonenumbers
from phonenumbers import geocoder, carrier
import urllib.parse as urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query = urlparse.urlparse(self.path).query
            params = urlparse.parse_qs(query)

            number = params.get("number", [""])[0]

            parsed = phonenumbers.parse(number)

            data = {
                "number": number,
                "valid": phonenumbers.is_valid_number(parsed),
                "country": geocoder.description_for_number(parsed, "en"),
                "carrier": carrier.name_for_number(parsed, "en")
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        except:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid Number"}).encode())