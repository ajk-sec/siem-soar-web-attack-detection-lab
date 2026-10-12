# Incident Response Playbook: Web Application Attack

**Framework:** NIST SP 800-61 (Computer Security Incident Handling Guide)

## 1. Preparation
- Ensure Splunk is ingesting logs from the web application and OS (Auditd).
- Ensure the SOAR pipeline (Python, Slack, VirusTotal) is running.

## 2. Detection & Analysis
- **Trigger:** Splunk alerts for SQLi, Brute Force, XSS, Command Injection, or Suspicious Process Execution.
- **Analysis Steps:**
    1. Review the Slack alert for the attack type, source IP, and payload.
    2. Search Splunk `index=sqli` for related activity from the same IP.
    3. Check VirusTotal for the attacker's IP reputation.
    4. Determine if the attack was successful (e.g., check for `LOGIN_SUCCESS` after an injection).

## 3. Containment
- **Short-term:** Block the attacker's IP address at the firewall (`iptables -A INPUT -s <IP> -j DROP`).
- **Long-term:** Isolate the affected server from the network if a reverse shell is detected.

## 4. Eradication & Recovery
- Patch the vulnerable code (e.g., use parameterized queries for SQLi).
- Remove any web shells or malicious files.
- Restart the web server.
- Monitor for re-entry attempts.

## 5. Post-Incident Activity
- Update the Splunk detection rules to catch variations of the attack.
- Document lessons learned.
- Update this playbook.