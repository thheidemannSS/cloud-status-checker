from flask import Flask, jsonify
import requests
import feedparser

app = Flask(__name__)

def check_sophos():
    try:
        r = requests.get("https://status.sophos.com/api/v2/summary.json", timeout=5)
        data = r.json()
        return data.get("status", "unknown").lower()
    except:
        return "error"

def check_adobe():
    try:
        feed = feedparser.parse("https://status.adobe.com/rss/all.rss")
        if feed.entries:
            entry = feed.entries[0]
            if "degraded" in entry.title.lower() or "incident" in entry.title.lower():
                return "degraded"
        return "operational"
    except:
        return "error"

def check_teamviewer():
    try:
        feed = feedparser.parse("https://status.teamviewer.com/history.rss")
        if feed.entries:
            entry = feed.entries[0]
            if "incident" in entry.title.lower() or "degraded" in entry.title.lower():
                return "degraded"
        return "operational"
    except:
        return "error"

def check_m365():
    try:
        r = requests.get("https://status.office.com", timeout=5)
        return "reachable" if r.status_code == 200 else "unreachable"
    except:
        return "error"

def check_basecamp_components():
    try:
        r = requests.get("https://37status.com/api/v2/components.json", timeout=5)
        components = r.json().get("components", [])
        result = {}
        for comp in components:
            name = comp.get("name", "unknown").lower().replace(" ", "_").replace("-", "_")
            status = comp.get("status", "unknown")
            result[name] = status
        return result
    except:
        return {"basecamp_components": "error"}

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "sophos": check_sophos(),
        "adobe": check_adobe(),
        "teamviewer": check_teamviewer(),
        "ms365": check_m365(),
        "basecamp": check_basecamp_components()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)
