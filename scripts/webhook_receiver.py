from flask import Flask, request
import requests
import datetime
import json

app = Flask(__name__)

# ⚠️ SECURITY WARNING: Replace with your actual keys before running!
SLACK_WEBHOOK_URL = "YOUR_SLACK_WEBHOOK_HERE"
VIRUSTOTAL_API_KEY = "YOUR_VIRUSTOTAL_API_KEY_HERE"

def check_virustotal(ip_address):
    """Queries VirusTotal to check the reputation of an IP address."""
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            stats = data['data']['attributes']['last_analysis_stats']
            return f"Malicious: {stats.get('malicious', 0)} | Suspicious: {stats.get('suspicious', 0)} | Harmless: {stats.get('harmless', 0)}"
        return f"VirusTotal lookup failed (Status: {response.status_code})"
    except Exception as e:
        return f"VirusTotal error: {str(e)}"

def block_ip(ip_address):
    """Simulates automated containment by blocking the attacker's IP."""
    print(f"[*] INITIATING AUTOMATED CONTAINMENT: Blocking IP {ip_address}...")
    print(f"[+] SUCCESS: IP {ip_address} blocked at firewall.")

def send_slack_alert(message):
    """Sends the formatted alert to the Slack channel."""
    payload = {"text": message, "username": "SOC-Automation-Bot", "icon_emoji": ":rotating_light:"}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload)
        print("[+] Slack Alert Sent.")
    except Exception as e:
        print(f"[-] Slack Error: {e}")

def create_ticket(alert_data, vt_result, attacker_ip, attack_type):
    """Generates a formal incident ticket on the D drive."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"D:\\ultimate-soc-lab\\INC-{timestamp}.md"
    content = f"""# INCIDENT TICKET: {timestamp}
**Severity:** HIGH
**Status:** Contained
**Attack Type:** {attack_type}
**Assigned To:** Tier 1 SOC Analyst

## Alert Details
{alert_data}

## Threat Intelligence (VirusTotal)
{vt_result}

## Automated Response Action
- [x] Attacker IP `{attacker_ip}` blocked at the firewall.
- [x] Slack alert sent to SOC team.

## Recommended Actions
1. Verify the block was successful.
2. Patch the vulnerability.
3. Monitor for re-entry attempts.
"""
    with open(filename, "w") as f:
        f.write(content)
    print(f"[+] Ticket generated: {filename}")

@app.route('/alert', methods=['POST'])
def receive_alert():
    """Receives the alert from Splunk and triggers the SOAR pipeline."""
    data = request.json
    print(f"[*] Received alert: {json.dumps(data)[:200]}")
    
    # Extract attack type from Splunk's search name
    search_name = data.get("search_name", "Security Alert")
    attack_type = search_name.replace(" Detected", "").replace(" Attack", "")
    
    # Default attacker IP (Kali in our lab)
    attacker_ip = "192.168.31.188"
    
    # Build a readable log summary from the alert metadata
    raw_log = f"Search: {search_name}\nSearch ID: {data.get('sid', 'N/A')}\nOwner: {data.get('owner', 'N/A')}"
    
    # 1. Enrich with VirusTotal
    vt_result = check_virustotal(attacker_ip)
    
    # 2. Automated Containment
    block_ip(attacker_ip)
    
    # 3. Send Slack Alert
    msg = f"""
🚨 *SECURITY ALERT DETECTED & CONTAINED* 🚨

*Time:* {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
*Attack Type:* {attack_type}
*Source IP:* {attacker_ip}
*Target Host:* Ubuntu (192.168.31.46)

*🦠 VirusTotal Enrichment:*
{vt_result}

*🛡️ Automated Action Taken:*
- Attacker IP blocked at the firewall.

*Alert Details:*
{raw_log}
"""
    send_slack_alert(msg)
    
    # 4. Create Ticket
    create_ticket(raw_log, vt_result, attacker_ip, attack_type)
    
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)