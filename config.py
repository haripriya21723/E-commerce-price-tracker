# Email Configuration
# Update these values with your email credentials

# Gmail account that will SEND the notifications
SENDER_EMAIL = "himabindhubanda93@gmail.com"

# Gmail App Password (NOT your regular password!)
# ⚠️ SECURITY WARNING: Do NOT use your login password (e.g., Hima@1920)
# You MUST generate an App Password at: https://myaccount.google.com/apppasswords
# If that link doesn't work, your college blocks it -> Use a personal Gmail account.
# Format: 16 characters without spaces (e.g., "abcdefghijklmnop")
SENDER_APP_PASSWORD = "ortoancwbxjxgyvi"

# Email addresses that will RECEIVE the notifications
RECIPIENT_EMAILS = [
    "harithalandi29@gmail.com", "23ra1a0550@kpritech.ac.in"
    # Add more emails here inside the list, separated by commas
    # "another_email@gmail.com",
]

# Product Configuration
# List of dictionaries containing product URL and target price
PRODUCTS = [
    {
        "url": "https://www.amazon.in/HP-i3-1215U-Anti-Glare-15-6-inch-Graphics/dp/B0D4LZMJ5Z/ref=sr_1_2_sspa?crid=3RBT17JHJCG22&dib=eyJ2IjoiMSJ9.xRoqzr9lU8PxiwOk-gz83l6YJWRp2O6pu_Lp44i8QPn1OSnC2CtnzKUhZVZ-9dFRQIVL_2B9eI8CM4DIT9N4FLAnsjwdP8FCZv_3Ku1UN8_ZxdCzvJcY_DkuK79NvITSutbPtqfRD7OsrOveM3AoDM9HRKdCSDUj_BWpISBOQboJ_d0JtFVIlbrRT2eIUUOHsTIS92a003RnSYsPwmGUZTuJtmVDdBgyzGn_RI78SVc.C9l3sfRmk5iwTA9tuaoO62wbrUj85CU2QM7Yao3x6pk&dib_tag=se&keywords=laptop%2Bunder%2B35000&qid=1749139630&sprefix=%2Caps%2C230&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",
        "target_price": 38000
    },
    {
        "url": "https://www.amazon.in/Apple-iPhone-13-128GB-Starlight/dp/B09G9D8KRQ",
        "target_price": 48000
    },
    {
        "url": "https://www.amazon.in/Sony-WH-1000XM4-Cancelling-Headphones-Bluetooth/dp/B0863TXGM3",
        "target_price": 19000
    },
]

# How often to check the price (in seconds)
# 3600 = 1 hour, 1800 = 30 minutes, 7200 = 2 hours
CHECK_INTERVAL = 3600
