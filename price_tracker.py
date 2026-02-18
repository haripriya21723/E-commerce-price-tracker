import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import re
from datetime import datetime
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def get_price(url):
    """Fetch the current price from the product URL"""
    try:
        # Generic headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Cache-Control': 'max-age=0'
        }
        
        print(f"Fetching price from: {url[:50]}...") # Print first 50 chars of URL
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')

        # Try Amazon price selectors
        price_element = soup.select_one('.a-price-whole')
        if not price_element:
            price_element = soup.select_one('span.a-price span.a-offscreen')
        
        # Add other site selectors here if needed
        # Flipkart example:
        # if not price_element:
        #     price_element = soup.select_one('.Nx9bqj.CxhGGd')

        if price_element:
            price_text = price_element.text.strip()
            # Extract number from text (e.g., "1,234.00" -> 1234.00)
            price_number = re.findall(r'[\d,]+', price_text)
            if price_number:
                price = float(price_number[0].replace(',', ''))
                return price
        
        print("Could not find price element on the page")
        return None
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out")
        return None
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def send_email(subject, body, to_emails, from_email, from_password):
    """Send an email notification to multiple recipients"""
    if isinstance(to_emails, str):
        to_emails = [to_emails] # Convert single string to list
        
    success_count = 0
    
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Connecting to Gmail SMTP server...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, from_password)
        
        for recipient in to_emails:
            try:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = from_email
                msg['To'] = recipient
                
                text_part = MIMEText(body, 'plain')
                msg.attach(text_part)
                
                print(f"Sending email to {recipient}...")
                server.send_message(msg)
                print(f"[SUCCESS] Email sent to {recipient}")
                success_count += 1
            except Exception as e:
                print(f"[ERROR] Failed to send to {recipient}: {e}")
                
        server.quit()
        return success_count > 0
        
    except smtplib.SMTPAuthenticationError as e:
        print("[ERROR] Authentication failed. Please check your email and app password.")
        print(f"  Error details: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] SMTP Error: {e}")
        return False

def send_test_email(to_emails, from_email, from_password, products):
    """Send a test email to verify the email setup works"""
    product_list_str = "\n".join([f"- {p['url'][:50]}... (Target: Rs. {p['target_price']})" for p in products])
    
    subject = "Price Tracker - Test Email"
    body = f"""Hello!

This is a test email from your Price Tracker application.
If you're receiving this, your email configuration is working correctly!

Tracking Configuration:
{product_list_str}

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

The price tracker will now monitor these products and notify you when prices drop.
"""
    return send_email(subject, body, to_emails, from_email, from_password)

def track_prices(products, check_interval, to_emails, from_email, from_password):
    """Track multiple products and send email when price drops"""
    print("\n" + "="*60)
    print("PRICE TRACKER STARTED")
    print("="*60)
    print(f"Tracking {len(products)} products")
    print(f"Check Interval: {check_interval} seconds ({check_interval/3600:.1f} hours)")
    print(f"Recipients: {', '.join(to_emails)}")
    print("="*60 + "\n")
    
    check_count = 0
    
    while True:
        check_count += 1
        print(f"\n--- Check #{check_count} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        
        for i, product in enumerate(products, 1):
            url = product['url']
            target_price = product['target_price']
            
            print(f"\nProduct {i}: Tracking...")
            current_price = get_price(url)
            
            if current_price is not None:
                print(f"[OK] Current Price: Rs. {current_price}")
                
                if current_price <= target_price:
                    price_diff = target_price - current_price
                    print(f"*** PRICE DROP DETECTED! ***")
                    print(f"Price is Rs. {price_diff} below target (Rs. {target_price})")
                    
                    subject = f"Price Drop Alert! Product {i}"
                    body = f"""Great news! A product you're tracking has dropped in price!

Product {i} Details:
Current Price: Rs. {current_price}
Target Price: Rs. {target_price}
You Save: Rs. {price_diff}

Product Link:
{url}

Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                    send_email(subject, body, to_emails, from_email, from_password)
                else:
                    print(f"  Price is still above target (Rs. {target_price})")
            else:
                print(f"[ERROR] Could not check price for Product {i}")
        
        print(f"\nNext check in {check_interval} seconds...")
        time.sleep(check_interval)

if __name__ == "__main__":
    try:
        from config import (
            SENDER_EMAIL,
            SENDER_APP_PASSWORD,
            RECIPIENT_EMAILS,
            PRODUCTS,
            CHECK_INTERVAL
        )
        
    except ImportError:
        print("[ERROR] Could not import config.py")
        print("Please make sure config.py exists and has the new structure.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Error loading configuration: {e}")
        sys.exit(1)
    
    # Send test email first
    print("Sending test email to verify configuration...")
    if send_test_email(RECIPIENT_EMAILS, SENDER_EMAIL, SENDER_APP_PASSWORD, PRODUCTS):
        print("\n[SUCCESS] Test emails sent! checking inbox...\n")
        time.sleep(2)
        # Start tracking
        track_prices(PRODUCTS, CHECK_INTERVAL, RECIPIENT_EMAILS, SENDER_EMAIL, SENDER_APP_PASSWORD)
    else:
        print("\n[ERROR] Test email failed.")