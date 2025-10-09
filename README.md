# Instagram Playwright Unfollow Bot

A browser automation script using Playwright to unfollow Instagram accounts while protecting trusted accounts.

## 🚀 Features

- ✅ **Browser Automation**: Uses real browser to avoid API detection
- ✅ **Trusted Accounts Protection**: Never unfollows accounts in your trusted list
- ✅ **Human-like Behavior**: Random delays and realistic typing
- ✅ **Simulation Mode**: Preview what would happen before executing
- ✅ **Stealth Mode**: Configured to avoid automation detection
- ✅ **Safe Limits**: Built-in limits to avoid Instagram restrictions

## 📋 Prerequisites

- Python 3.7 or higher
- Chrome/Chromium browser (installed automatically with Playwright)

## 🛠️ Installation

1. **Navigate to the project directory:**
```bash
cd instagram_playwright_unfollow
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers:**
```bash
playwright install chromium
```

## ⚙️ Configuration

### 1. Edit Trusted Accounts

Edit `trusted_accounts.json` and add usernames you want to protect:

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

**Important:** Use usernames WITHOUT the @ symbol.

### 2. Run the Script

```bash
python instagram_unfollow.py
```

## 📱 How It Works

1. **Login**: Enters your credentials with human-like typing
2. **Navigate**: Goes to your profile and opens the following list
3. **Analyze**: Checks each account against your trusted list
4. **Simulate**: Shows what would happen without making changes
5. **Execute**: After confirmation, performs real unfollows (optional)

## 🛡️ Safety Features

### Trusted Account Protection
- Accounts in `trusted_accounts.json` are **NEVER** unfollowed
- Clear indication when protected accounts are found

### Human-like Behavior
- Random delays between actions (1-6 seconds)
- Realistic typing speed with character-by-character input
- Random mouse movements and scrolling

### Rate Limiting
- Built-in delays to avoid Instagram limits
- Configurable maximum unfollows per session
- Automatic pauses between unfollows

### Stealth Configuration
- Removes automation detection flags
- Uses realistic user agent and viewport
- Disables webdriver indicators

## 📊 Example Output

```
🔥 Instagram Playwright Unfollow Bot
=============================================
📱 Instagram Username: your_username
🔒 Password: ********
🔢 Maximum unfollows (default 20): 15

✅ Loaded 4 trusted accounts
🚀 Starting browser...
✅ Browser started successfully
🔐 Logging into Instagram...
✅ Login successful!
📋 Navigating to following list...
✅ Opened following list

🔍 Running SIMULATION first...
👤 Processing: @random_user1
🎯 [SIMULATION] Would unfollow: @random_user1
👤 Processing: @best_friend
🛡️  PROTECTED: @best_friend
...

🎉 PROCESS COMPLETED
   • Simulated unfollows: 12
   • Protected accounts: 3
   • Errors: 0
   • Total processed: 15

🚨 Do you want to proceed with REAL unfollows? (type 'YES'): 
```

## ⚠️ Important Notes

### Instagram Limits
- Instagram has daily limits on unfollows (~200 per day)
- The script uses conservative defaults (20 max per session)
- Space out your sessions to avoid temporary restrictions

### Account Security
- Use your regular Instagram credentials
- The script doesn't store your password
- Consider using this from your usual device/network

### Responsible Use
- This tool is for personal use only
- Respect Instagram's terms of service
- Don't use for spam or harassment

## 🔧 Troubleshooting

### Login Issues
- Make sure username/password are correct
- Disable 2FA temporarily if having issues
- Try from the same network you usually use

### Browser Closes Unexpectedly
- This is normal - Instagram may detect automation
- The script handles this gracefully
- Try running again with longer delays

### Browser Not Opening
```bash
playwright install chromium
```

### Python Version Issues
- Use Python 3.10, 3.11, or 3.12 (3.13 has compatibility issues)
- Create virtual environment: `python3.12 -m venv .venv`
- Activate: `source .venv/bin/activate`

### No Users Found
- Make sure you're logged into the correct account
- Check that you have accounts to unfollow
- Verify the following list opened correctly

### Too Many Errors
- Reduce the maximum unfollows number
- Wait longer between sessions
- Check your internet connection

### Target Closed Error
- This happens when Instagram detects automation
- The script will handle this gracefully
- Try again later or use smaller batch sizes

## 📄 Project Structure

```
instagram_playwright_unfollow/
├── instagram_unfollow.py      # Main script
├── trusted_accounts.json      # Protected accounts list
├── requirements.txt          # Python dependencies
└── README.md                # This documentation
```

## 🤝 Contributing

If you find bugs or have suggestions:
1. Create an issue describing the problem
2. Include error messages and steps to reproduce
3. Suggestions for improvements are welcome

## 📜 License

This project is for educational and personal use only. Use responsibly and respect Instagram's terms of service.

---

**⚠️ Disclaimer**: This script is not affiliated with Instagram. Use at your own risk and responsibility. The authors are not responsible for any account restrictions or violations of Instagram's terms of service.