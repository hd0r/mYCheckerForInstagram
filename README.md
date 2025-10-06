# mYCheckerForInstagram

An advanced Python-based tool for checking Instagram account credentials. It features multi-threading, proxy support with auto-switching, and smart throttling logic to prevent rate-limiting.

**Telegram:** [@hd0rr](https://t.me/hd0rr )

---

### **DISCLAIMER**
This tool is intended for **educational purposes only**. The developer assumes no responsibility for any misuse by others. Unauthorized account access is illegal. Please use this script responsibly and ethically.

---

## Features

- **Instagram Account Checker**: Verifies login credentials (username/password).
- **Multi-Threading**: Utilizes multiple threads to check accounts concurrently, significantly speeding up the process.
- **Proxy Support**: Comes with a built-in list of proxies and automatically switches to a new proxy if the current one is blocked or fails.
- **Smart Throttling**: Implements a throttling mechanism that pauses the script if it detects too many consecutive invalid user errors, helping to avoid IP bans.
- **Fixed Password List**: Checks each username against a predefined list of common passwords.
- **Telegram Notifications**: Sends detailed information of successfully accessed accounts to a specified Telegram chat via a bot.
- **Dynamic User-Agent Generation**: Creates random, realistic mobile user-agents for each request to mimic real devices.

## How It Works

The script reads a list of usernames from a text file (`usernames.txt`). For each username, it attempts to log in using a list of predefined passwords. It uses the internal Instagram mobile API to perform login attempts.

If a login is successful or requires a challenge, the account details (followers, following, bio, etc.) are fetched and sent to your Telegram chat. The script uses proxies to distribute requests and implements delays and throttling to avoid detection.

## Requirements

- **Python 3.x**
- **Required Libraries**: `requests`, `python-dotenv`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-hd0r/mYCheckerForInstagram.git
    cd mYCheckerForInstagram
    ```

2.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    *(You will need to create a `requirements.txt` file, see below )*

## Configuration

Before running the script, you need to set up the environment variables for Telegram notifications.

1.  **Create a `.env` file** in the same directory as the script:
    ```
    touch .env
    ```

2.  **Add your Telegram Bot Token and Chat ID** to the `.env` file. You can get these from [@BotFather](https://t.me/BotFather ) and [@userinfobot](https://t.me/userinfobot ) on Telegram.
    ```env
    BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
    CHAT_ID="YOUR_TELEGRAM_CHAT_ID"
    ```

3.  **Create a `requirements.txt` file** with the following content:
    ```
    requests
    python-dotenv
    ```

4.  **Prepare your username list**:
    Create a file named `usernames.txt` and add the usernames you want to check, one per line.
    ```
    username1
    username2
    username3
    ```

## Usage

Run the script from your terminal. The script is configured by default to use `usernames.txt`.

```bash
python your_script_name.py
