# How the Price Tracker Email System Works

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRICE TRACKER WORKFLOW                       │
└─────────────────────────────────────────────────────────────────┘

START
  │
  ├─► Load Configuration from config.py
  │   ├─ SENDER_EMAIL
  │   ├─ SENDER_APP_PASSWORD (16 chars, no spaces)
  │   ├─ RECIPIENT_EMAIL
  │   ├─ PRODUCT_URL
  │   ├─ TARGET_PRICE
  │   └─ CHECK_INTERVAL
  │
  ├─► Send Test Email
  │   │
  │   ├─► Connect to Gmail SMTP (smtp.gmail.com:465)
  │   ├─► Login with App Password
  │   ├─► Send test message
  │   │
  │   ├─► SUCCESS? ──► Continue to tracking
  │   │
  │   └─► FAILED? ──► Show error & exit
  │       └─ Check App Password
  │       └─ Verify 2-Step Verification enabled
  │       └─ Confirm email addresses correct
  │
  ├─► Start Price Tracking Loop
  │   │
  │   └─► LOOP (every CHECK_INTERVAL seconds)
  │       │
  │       ├─► Fetch Product Page from Amazon
  │       │   ├─ Send HTTP request with headers
  │       │   ├─ Parse HTML with BeautifulSoup
  │       │   └─ Extract price using CSS selectors
  │       │
  │       ├─► Compare Price
  │       │   │
  │       │   ├─► Current Price <= Target Price?
  │       │   │   │
  │       │   │   YES ──► Send Alert Email
  │       │   │   │       ├─ Subject: "Product Price Dropped!"
  │       │   │   │       ├─ Body: Price details + product link
  │       │   │   │       └─ Connect to Gmail & send
  │       │   │   │
  │       │   │   │       └─► Email Sent? ──► STOP TRACKING
  │       │   │   │
  │       │   │   NO ──► Log current price
  │       │   │           └─ Wait CHECK_INTERVAL seconds
  │       │   │           └─ Continue loop
  │       │   │
  │       │   └─► Price Fetch Failed?
  │       │       └─ Log error
  │       │       └─ Wait CHECK_INTERVAL seconds
  │       │       └─ Retry
  │       │
  │       └─► [Loop continues until price drops]
  │
END
```

## Email Authentication Flow

```
┌──────────────────────────────────────────────────────────────┐
│                  GMAIL AUTHENTICATION                        │
└──────────────────────────────────────────────────────────────┘

Your Script
    │
    ├─► Connect to smtp.gmail.com:465 (SSL)
    │
    ├─► Send LOGIN command
    │   ├─ Username: SENDER_EMAIL
    │   └─ Password: SENDER_APP_PASSWORD
    │
    ├─► Gmail Server Validates
    │   │
    │   ├─► Valid App Password?
    │   │   │
    │   │   YES ──► Authentication Success
    │   │   │       └─► Can send emails
    │   │   │
    │   │   NO ──► Authentication Failed
    │   │           └─► Error 535: Bad Credentials
    │   │               │
    │   │               └─► Possible Causes:
    │   │                   ├─ Using regular password (not App Password)
    │   │                   ├─ App Password has spaces
    │   │                   ├─ App Password is wrong/expired
    │   │                   ├─ 2-Step Verification not enabled
    │   │                   └─ Email address is incorrect
    │
    └─► Send Email
        ├─ FROM: SENDER_EMAIL
        ├─ TO: RECIPIENT_EMAIL
        ├─ SUBJECT: "Price Tracker - Test Email" or "Product Price Dropped!"
        └─ BODY: Message content
```

## Configuration File Structure

```
config.py
├─ SENDER_EMAIL          → "your-gmail@gmail.com"
├─ SENDER_APP_PASSWORD   → "abcdefghijklmnop" (16 chars)
├─ RECIPIENT_EMAIL       → "recipient@gmail.com"
├─ PRODUCT_URL           → "https://www.amazon.in/..."
├─ TARGET_PRICE          → 38000 (number)
└─ CHECK_INTERVAL        → 3600 (seconds)
```

## Email Message Structure

### Test Email
```
┌─────────────────────────────────────────────────────────┐
│ From: himabindhubanda93@gmail.com                       │
│ To: harithalandi29@gmail.com                            │
│ Subject: Price Tracker - Test Email                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Hello!                                                   │
│                                                          │
│ This is a test email from your Price Tracker app.       │
│                                                          │
│ If you're receiving this, your email configuration      │
│ is working correctly!                                    │
│                                                          │
│ Tracking Details:                                        │
│ - Product URL: [Amazon link]                            │
│ - Recipient: harithalandi29@gmail.com                   │
│ - Timestamp: 2026-02-16 21:30:02                        │
│                                                          │
│ The price tracker will now monitor the product.         │
│                                                          │
│ Happy shopping!                                          │
└─────────────────────────────────────────────────────────┘
```

### Price Drop Alert Email
```
┌─────────────────────────────────────────────────────────┐
│ From: himabindhubanda93@gmail.com                       │
│ To: harithalandi29@gmail.com                            │
│ Subject: Product Price Dropped!                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Great news! The product you're tracking has dropped     │
│ in price!                                                │
│                                                          │
│ Current Price: Rs. 37,990                               │
│ Your Target Price: Rs. 38,000                           │
│ You Save: Rs. 10                                         │
│                                                          │
│ Product Link:                                            │
│ https://www.amazon.in/HP-i3-1215U-Anti-Glare...         │
│                                                          │
│ This notification was sent at: 2026-02-16 22:45:30      │
│                                                          │
│ Don't miss this deal!                                    │
└─────────────────────────────────────────────────────────┘
```

## Error Handling

```
Error Type                    → Action Taken
─────────────────────────────────────────────────────────
SMTPAuthenticationError       → Show detailed error message
                              → Suggest generating new App Password
                              → Provide link to create App Password

SMTPException                 → Log SMTP error details
                              → Return False (email failed)

RequestException              → Log network error
                              → Return None (price fetch failed)
                              → Retry after CHECK_INTERVAL

Timeout                       → Log timeout error
                              → Retry after CHECK_INTERVAL

UnicodeEncodeError            → Fixed with UTF-8 encoding
                              → sys.stdout.reconfigure(encoding='utf-8')
```

## Security Best Practices

```
✓ Use Gmail App Password (NOT regular password)
✓ App Password is 16 characters, no spaces
✓ Enable 2-Step Verification on Google Account
✓ Never commit config.py to public repositories
✓ Each application should have unique App Password
✓ Revoke App Passwords when no longer needed
```

## Troubleshooting Decision Tree

```
Email Not Working?
    │
    ├─► Authentication Failed?
    │   ├─► Check App Password is 16 chars
    │   ├─► Remove all spaces from password
    │   ├─► Verify 2-Step Verification enabled
    │   └─► Generate new App Password
    │
    ├─► Email Not Received?
    │   ├─► Check spam/junk folder
    │   ├─► Verify recipient email correct
    │   ├─► Wait a few minutes (delay possible)
    │   └─► Check console for "[SUCCESS]" message
    │
    ├─► Import Error?
    │   ├─► Ensure config.py exists
    │   ├─► Run python setup.py
    │   └─► Check file is in same directory
    │
    └─► Price Not Fetched?
        ├─► Verify product URL is valid
        ├─► Check internet connection
        ├─► Amazon might be rate-limiting
        └─► Try different product URL
```

## Files and Their Purposes

```
price_tracker.py
├─ Main script
├─ Imports config from config.py
├─ Sends test email
├─ Tracks price in loop
└─ Sends alert when price drops

config.py
├─ Configuration settings
├─ Email credentials
├─ Product details
└─ Tracking parameters

setup.py
├─ Interactive configuration wizard
├─ Guides user through setup
├─ Validates input
└─ Generates config.py

README.md
├─ Complete documentation
├─ Setup instructions
├─ Troubleshooting guide
└─ Feature list

SUMMARY.md
├─ What was fixed
├─ Quick reference
└─ Next steps

QUICKSTART.txt
└─ Quick start guide
```
