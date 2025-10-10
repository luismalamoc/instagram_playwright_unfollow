# Instagram Playwright Unfollow Bot

This Python script allows you to automatically unfollow Instagram accounts using browser automation while protecting your trusted accounts.

## Prerequisites

Before running the script, ensure you have the following:

- Python 3.x installed on your machine.
- A stable internet connection.
- Your Instagram username and password.

## Setup Instructions

### 1. Navigate to Project Directory

```bash
cd instagram_playwright_unfollow
```

### 2. Install Required Python Packages

Install the necessary Python packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

Install the browser engines that Playwright will use:

```bash
playwright install
```

### 4. Configure Trusted Accounts

Edit the `trusted_accounts.json` file and add usernames you want to protect from being unfollowed:

```json
[
  "best_friend",
  "family_member", 
  "work_account",
  "important_brand"
]
```

**Important:** Use usernames WITHOUT the @ symbol.

## 5. Run the Script

Run the Python script using the following command:

```bash
python instagram_unfollow.py
```

## 6. Troubleshooting

### Login Issues

- Ensure your username and password are correct.
- Disable two-factor authentication temporarily if experiencing issues.
- Try running the script from the same network you usually use for Instagram.

### Browser Not Opening

```bash
playwright install
```

### Python Version Issues

- Use Python 3.10, 3.11, or 3.12 (Python 3.13 has compatibility issues).
- Create a virtual environment and activate it before running the script.

### General Tips

- The script uses Firefox or WebKit browsers for better compatibility on macOS.
- If Instagram detects automation, the script will handle it gracefully.
- Keep your trusted_accounts.json file updated with important accounts.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
