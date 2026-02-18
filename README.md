# 📧 Price Tracker - Email Setup Guide

Automated price tracking for Amazon products with email notifications!

## 🚀 Quick Start (Recommended)

### Option 1: Interactive Setup (Easiest)

1. **Install required packages:**
   ```bash
   pip install requests beautifulsoup4
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```
   
   The script will guide you through:
   - Entering your email addresses
   - Setting up your Gmail App Password
   - Configuring the product URL and target price
   - Automatically creating `config.py`

3. **Run the price tracker:**
   ```bash
   python price_tracker.py
   ```

### Option 2: Manual Setup

1. **Install required packages:**
   ```bash
   pip install requests beautifulsoup4
   ```

2. **Generate a Gmail App Password** (see instructions below)

3. **Edit `config.py`** with your details:
   - `SENDER_EMAIL`: Your Gmail address
   - `SENDER_APP_PASSWORD`: The 16-character app password
   - `RECIPIENT_EMAIL`: Where to send notifications
   - `PRODUCT_URL`: Amazon product link
   - `TARGET_PRICE`: Your desired price threshold
   - `CHECK_INTERVAL`: How often to check (in seconds)

4. **Run the price tracker:**
   ```bash
   python price_tracker.py
   ```

## 🔐 How to Generate a Gmail App Password

### Step 1: Enable 2-Step Verification
1. Go to: https://myaccount.google.com/security
2. Click on "2-Step Verification"
3. Follow the prompts to enable it (if not already enabled)

### Step 2: Create an App Password
1. Visit: **https://myaccount.google.com/apppasswords**
   *(Note: If you see "The setting you are looking for is not available for your account", your college admin has disabled App Passwords. You must use a personal Gmail account instead.)*
2. Sign in if prompted
3. In the "App name" field, type: **Price Tracker**
4. Click **Create**
5. Google will display a 16-character password like: `abcd efgh ijkl mnop`
6. **COPY THIS PASSWORD** - you won't see it again!

### Step 3: Use the App Password
- **Remove all spaces** from the password
- Example: `abcd efgh ijkl mnop` becomes `abcdefghijklmnop`
- Paste this into `config.py` as `SENDER_APP_PASSWORD`

## 📁 Project Files

- **`price_tracker.py`** - Main tracking script
- **`config.py`** - Configuration file (email, product, price)
- **`setup.py`** - Interactive setup wizard
- **`README.md`** - This file

## ⚙️ Configuration Options

Edit `config.py` to customize:

```python
# Email Settings
SENDER_EMAIL = "your-email@gmail.com"
SENDER_APP_PASSWORD = "your16charpassword"
RECIPIENT_EMAIL = "recipient@gmail.com"

# Product Settings
PRODUCT_URL = "https://www.amazon.in/..."
TARGET_PRICE = 38000  # Price in Rupees
CHECK_INTERVAL = 3600  # 1 hour (in seconds)
```

**Common intervals:**
- 30 minutes: `1800`
- 1 hour: `3600`
- 2 hours: `7200`
- 6 hours: `21600`

## ✨ Features

✅ **Automatic price monitoring** - Checks Amazon prices at your specified interval  
✅ **Email notifications** - Get alerted when price drops below your target  
✅ **Test email** - Verifies your setup before starting  
✅ **Detailed logging** - See exactly what's happening  
✅ **Error handling** - Retries on failures  
✅ **Windows compatible** - Fixed encoding issues  

## 🐛 Troubleshooting

### "Authentication failed" Error

**Problem:** The Gmail App Password is invalid or incorrect.

**Solutions:**
1. Make sure you're using an **App Password**, NOT your regular Gmail password
2. The password should be exactly **16 characters** with **no spaces**
3. Verify **2-Step Verification** is enabled on your Google account
4. Try generating a **new App Password**
5. Check that the email address is correct

### "Could not retrieve the current price" Error

**Problem:** Unable to fetch the price from Amazon.

**Solutions:**
1. Verify the product URL is valid (open it in a browser)
2. Amazon might be rate-limiting requests - try increasing `CHECK_INTERVAL`
3. The page structure might have changed - check if the product is still available
4. Try a different product URL

### Email Not Received

**Problem:** Test email or notification not arriving.

**Solutions:**
1. Check your **spam/junk folder**
2. Verify the recipient email address is correct in `config.py`
3. Make sure the test email showed "[SUCCESS]" in the console
4. Wait a few minutes - emails can be delayed
5. Try sending to a different email address

### Import Error: "Could not import config.py"

**Problem:** The config file is missing or in the wrong location.

**Solutions:**
1. Make sure `config.py` exists in the same folder as `price_tracker.py`
2. Run `python setup.py` to create it automatically
3. Check for typos in the filename

## 📊 How It Works

1. **Test Email** - Sends a test email to verify your configuration
2. **Price Check** - Fetches the current price from Amazon
3. **Comparison** - Compares current price with your target
4. **Notification** - Sends email if price drops below target
5. **Repeat** - Waits for the specified interval and checks again

## 🎯 Example Output

```
Sending test email to verify configuration...
[2026-02-16 21:30:02] Preparing to send email...
Connecting to Gmail SMTP server...
Logging in...
Sending email to recipient@gmail.com...
[SUCCESS] Email sent successfully to recipient@gmail.com!

[SUCCESS] Test email sent successfully!
Check your inbox to confirm you received it.

============================================================
PRICE TRACKER STARTED
============================================================
Target Price: Rs. 38000
Check Interval: 3600 seconds (1.0 hours)
Notification Email: recipient@gmail.com
============================================================

--- Check #1 at 2026-02-16 21:30:05 ---
[2026-02-16 21:30:05] Fetching price from URL...
Found price text: 42,990
[OK] Current Price: Rs. 42990.0
  Target Price: Rs. 38000
  Price is still Rs. 4990.0 above target
  Next check in 3600 seconds...
```

## 🔒 Security Notes

- **Never share your App Password** with anyone
- **Don't commit `config.py`** to public repositories
- App Passwords can be revoked at any time from your Google Account
- Each app should have its own unique App Password

## 📞 Need More Help?

If you're still having issues:

1. ✅ Verify all email addresses are correct
2. ✅ Confirm the App Password is exactly 16 characters
3. ✅ Check that 2-Step Verification is enabled
4. ✅ Try running `python setup.py` again
5. ✅ Test with a different product URL
6. ✅ Check your internet connection

## 📝 Current Default Configuration

- **From Email:** himabindhubanda93@gmail.com
- **To Email:** harithalandi29@gmail.com
- **Product:** HP Laptop on Amazon India
- **Target Price:** Rs. 38,000
- **Check Interval:** 1 hour

**To change these:** Edit `config.py` or run `python setup.py`

---

**Happy Price Tracking! 🎉**
