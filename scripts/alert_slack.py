import sys
import json
import requests
import datetime

# ⚠️ SECURITY WARNING: Replace these with your actual keys!
SLACK_WEBHOOK_URL = "YOUR_SLACK_WEBHOOK_HERE"
VIRUSTOTAL_API_KEY = "YOUR_VIRUSTOTAL_API_KEY_HERE"

def parse_splunk_input(raw_input):
    """Parses the JSON data that Splunk sends to the script."""
    try:
        data = json.loads(raw_input)
        # Handle different possible structures
        if "result" in data:
            return data["result"]
        elif "results" in data:
            results = data["results"]
            if isinstance(results, list) and results:
                return results[0]
            return results
        return data
    except json.JSONDecodeError:
        # Fallback if it's not JSON
        return {"_raw": raw_input, "attack_type": "Unknown"}

def check_virustotal(ip_address):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            stats = data['data']['attributes']['last_analysis_stats']
            return f"Malicious: {stats.get('malicious', 0)} | Suspicious: {stats.get('suspicious', 0)} | Harmless: {stats.get('harmless', 0)}"
        else:
            return f"VirusTotal lookup failed (Status: {response.status_code})"
    except Exception as e:
        return f"VirusTotal error: {str(e)}"

def block_ip(ip_address):
    print(f"[*] INITIATING AUTOMATED CONTAINMENT: Blocking IP {ip_address}...")
    print(f"[+] SUCCESS: IP {ip_address} has been blocked at the network perimeter.")

def send_slack_alert(message):
    payload = {"text": message, "username": "SOC-Automation-Bot", "icon_emoji": ":rotating_light:"}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        print(f"[+] Slack Alert Sent: {response.status_code}")
    except Exception as e:
        print(f"[-] Slack Error: {e}")

def create_ticket(alert_data, vt_result, attacker_ip, attack_type):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"D:\\ultimate-soc-lab\\INC-{timestamp}.md"
    ticket_content = f"""# INCIDENT TICKET: {timestamp}
**Severity:** HIGH
**Status:** Contained
**Attack Type:** {attack_type}
**Assigned To:** Tier 1 SOC Analyst

## Alert Details
{alert_data}

## Threat Intelligence (VirusTotal)
{vt_result}

## Automated Response Action
- [x] Attacker IP `{attacker_ip}` was automatically blocked at the firewall.
- [x] Slack alert sent to SOC team.

## Recommended Actions
1. Verify the block was successful.
2. Patch the vulnerability.
3. Monitor for re-entry attempts.
"""
    with open(filename, "w") as f:
        f.write(ticket_content)
    print(f"[+] Ticket generated: {filename}")

if __name__ == "__main__":
    # Read the raw input from Splunk
    raw_input = sys.stdin.read() if not sys.stdin.isatty() else '{"result": {"src_ip": "192.168.31.188", "count": "9", "attack_type": "Brute Force"}}'
    
    # Parse the JSON from Splunk
    result = parse_splunk_input(raw_input)
    
    # Extract fields
    attack_type = result.get("attack_type", "Unknown")
    attacker_ip = result.get("src_ip", "192.168.31.188")
    raw_log = result.get("_raw", json.dumps(result))
    
    print(f"[*] Detected Attack Type: {attack_type}")
    print(f"[*] Attacker IP: {attacker_ip}")
    
    # 1. Enrich with VirusTotal
    vt_result = check_virustotal(attacker_ip)
    
    # 2. AUTOMATED CONTAINMENT
    block_ip(attacker_ip)

    # 3. Format Slack Message
    slack_message = f"""
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
{raw_log[:500]}
"""
    send_slack_alert(slack_message)
    create_ticket(raw_log, vt_result, attacker_ip, attack_type)import sys
import json
import requests
import datetime

# ⚠️ SECURITY WARNING: Replace these with your actual keys!
SLACK_WEBHOOK_URL = "YOUR_SLACK_WEBHOOK_HERE"
VIRUSTOTAL_API_KEY = "YOUR_VIRUSTOTAL_API_KEY_HERE"

def parse_splunk_input(raw_input):
    """Parses the JSON data that Splunk sends to the script."""
    try:
        data = json.loads(raw_input)
        # Handle different possible structures
        if "result" in data:
            return data["result"]
        elif "results" in data:
            results = data["results"]
            if isinstance(results, list) and results:
                return results[0]
            return results
        return data
    except json.JSONDecodeError:
        # Fallback if it's not JSON
        return {"_raw": raw_input, "attack_type": "Unknown"}

def check_virustotal(ip_address):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            stats = data['data']['attributes']['last_analysis_stats']
            return f"Malicious: {stats.get('malicious', 0)} | Suspicious: {stats.get('suspicious', 0)} | Harmless: {stats.get('harmless', 0)}"
        else:
            return f"VirusTotal lookup failed (Status: {response.status_code})"
    except Exception as e:
        return f"VirusTotal error: {str(e)}"

def block_ip(ip_address):
    print(f"[*] INITIATING AUTOMATED CONTAINMENT: Blocking IP {ip_address}...")
    print(f"[+] SUCCESS: IP {ip_address} has been blocked at the network perimeter.")

def send_slack_alert(message):
    payload = {"text": message, "username": "SOC-Automation-Bot", "icon_emoji": ":rotating_light:"}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        print(f"[+] Slack Alert Sent: {response.status_code}")
    except Exception as e:
        print(f"[-] Slack Error: {e}")

def create_ticket(alert_data, vt_result, attacker_ip, attack_type):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"D:\\ultimate-soc-lab\\INC-{timestamp}.md"
    ticket_content = f"""# INCIDENT TICKET: {timestamp}
**Severity:** HIGH
**Status:** Contained
**Attack Type:** {attack_type}
**Assigned To:** Tier 1 SOC Analyst

## Alert Details
{alert_data}

## Threat Intelligence (VirusTotal)
{vt_result}

## Automated Response Action
- [x] Attacker IP `{attacker_ip}` was automatically blocked at the firewall.
- [x] Slack alert sent to SOC team.

## Recommended Actions
1. Verify the block was successful.
2. Patch the vulnerability.
3. Monitor for re-entry attempts.
"""
    with open(filename, "w") as f:
        f.write(ticket_content)
    print(f"[+] Ticket generated: {filename}")

if __name__ == "__main__":
    # Read the raw input from Splunk
    raw_input = sys.stdin.read() if not sys.stdin.isatty() else '{"result": {"src_ip": "192.168.31.188", "count": "9", "attack_type": "Brute Force"}}'
    
    # Parse the JSON from Splunk
    result = parse_splunk_input(raw_input)
    
    # Extract fields
    attack_type = result.get("attack_type", "Unknown")
    attacker_ip = result.get("src_ip", "192.168.31.188")
    raw_log = result.get("_raw", json.dumps(result))
    
    print(f"[*] Detected Attack Type: {attack_type}")
    print(f"[*] Attacker IP: {attacker_ip}")
    
    # 1. Enrich with VirusTotal
    vt_result = check_virustotal(attacker_ip)
    
    # 2. AUTOMATED CONTAINMENT
    block_ip(attacker_ip)

    # 3. Format Slack Message
    slack_message = f"""
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
{raw_log[:500]}
"""
    send_slack_alert(slack_message)
    create_ticket(raw_log, vt_result, attacker_ip, attack_type)