import os
import requests
import resend
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Configuration from Environment
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
MJML_APP_ID = os.getenv("MJML_APP_ID")
MJML_SECRET_KEY = os.getenv("MJML_SECRET_KEY")

resend.api_key = RESEND_API_KEY

def compile_mjml(mjml_content):
    """Converts MJML string to HTML using the MJML API."""
    url = "https://api.mjml.io/v1/render"
    response = requests.post(
        url,
        auth=(MJML_APP_ID, MJML_SECRET_KEY),
        json={"mjml": mjml_content}
    )
    if response.status_code == 200:
        return response.json().get("html")
    else:
        raise Exception(f"MJML Error: {response.text}")

def send_email(html_body):
    """Sends the compiled HTML via Resend."""
    params = {
        "from": "Jeremiah <theking@crousia.com>",
        "to": ["johnjcrouse@gmail.com", "pamcrouse@gmail.com", "hiddengold@gmail.com", "greatlyloved@gmail.com", "laurenacrouse@gmail.com", "jeremiahjcrouse@gmail.com"], # Update this or pull from a file
        "subject": "Friends & Family Update",
        "html": html_body,
    }
    
    try:
        email = resend.Emails.send(params)
        print(f"🚀 Email sent successfully! ID: {email['id']}")
    except Exception as e:
        print(f"❌ Resend Error: {e}")

if __name__ == "__main__":
    # 1. Read the MJML file authored by Big Pickle
    if not os.path.exists("template.mjml"):
        print("Error: template.mjml not found. Let Big Pickle write it first!")
    else:
        with open("template.mjml", "r") as f:
            mjml_source = f.read()
        
        print("Compiling MJML...")
        compiled_html = compile_mjml(mjml_source)
        
        print("Sending via Resend...")
        send_email(compiled_html)
