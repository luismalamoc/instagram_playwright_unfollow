# Instagram Playwright Unfollow Bot

This Python script helps you unfollow Instagram accounts using browser
automation while protecting the accounts in your trusted list.

You log in **manually** in the browser window that the script opens, and
Playwright waits until it detects your session before continuing. This avoids
the constant breakage caused by Instagram changing its login form and anti-bot
checks.

## Prerequisites

- Python 3.11+ installed (tested with Python 3.14).
- A stable internet connection.
- Your Instagram account (you log in by hand, no password is stored).

## Setup Instructions

### 1. Navigate to Project Directory

```bash
cd instagram_playwright_unfollow
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Required Python Packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

Install the browser engine used by the script (Firefox is recommended on macOS):

```bash
python -m playwright install firefox
```

> You can also run `python -m playwright install` to install all browsers.

### 5. Configure Trusted Accounts

Edit the `trusted_accounts.json` file and add the usernames you want to protect
from being unfollowed under `trusted_usernames`:

```json
{
  "trusted_usernames": [
    "best_friend",
    "family_member",
    "work_account",
    "important_brand"
  ]
}
```

**Important:** Use usernames WITHOUT the `@` symbol.

## Running the Script

```bash
python instagram_unfollow.py
```

You will be asked for:

1. **Your Instagram username** (without `@`) — used only to open your profile
   and your "following" list.
2. **The browser** to use (Firefox recommended).

Then:

1. A browser window opens on the Instagram login page.
2. **Log in manually** in that window (username, password, and any
   2FA / verification Instagram asks for).
3. The script waits (up to 5 minutes) until it detects you are logged in and
   then continues to the unfollow process.
4. Confirm when prompted to start unfollowing. Accounts in
   `trusted_accounts.json` are skipped.

> The browser always runs in **GUI (visible) mode** because the login is done
> by hand.

## Troubleshooting

### Login Not Detected

- Make sure you finished logging in (including 2FA) within 5 minutes.
- Complete any "Save your login info?" / "Turn on notifications" prompts.
- If your interface is in a different language and detection fails, share what
  is on screen after logging in so the detection selectors can be adjusted.

### Browser Not Opening

```bash
python -m playwright install firefox
```

### Python Version / Install Issues (greenlet build errors)

The pinned dependencies require prebuilt wheels for your Python version.

- This project is pinned to `playwright==1.61.0`, which ships wheels compatible
  with Python 3.14.
- If you see a `greenlet` compilation error, you are likely mixing an old
  Playwright version with a very new Python. Recreate the virtual environment
  and reinstall from `requirements.txt`:

  ```bash
  rm -rf .venv
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  python -m playwright install firefox
  ```

### General Tips

- Firefox tends to be the most stable option for GUI mode on macOS.
- Keep your `trusted_accounts.json` file updated with important accounts.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
