import os
import sys
import requests
import resend
from dotenv import load_dotenv

load_dotenv()

# Config
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
MJML_APP_ID = os.getenv("MJML_APP_ID")
MJML_SECRET_KEY = os.getenv("MJML_SECRET_KEY")

resend.api_key = RESEND_API_KEY

def get_recipients(filename):
    """Parses a text file for Name,Email pairs."""
    people = []
    try:
        with open(filename, "r") as f:
            for line in f:
                if "," in line:
                    name, email = line.strip().split(",")
                    people.append({"name": name, "email": email})
        return people
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found.")
        sys.exit(1)

def compile_mjml(mjml_content):
    url = "https://api.mjml.io/v1/render"
    response = requests.post(
        url,
        auth=(MJML_APP_ID, MJML_SECRET_KEY),
        json={"mjml": mjml_content}
    )
    return response.json().get("html")

def send_batch(html_body, recipients):
    batch_params = []
    for person in recipients:
        # Clean up any accidental whitespace from the text file
        name = person['name'].strip()
        email = person['email'].strip()
        
        # Format explicitly as "Name <email@example.com>"
        formatted_to = f"{name} <{email}>"
        
        batch_params.append({
            "from": "Jeremiah <theking@crousia.com>",
            "to": formatted_to,
            "subject": f"Hey {name}, a quick life update",
            "html": html_body,
        })

    try:
        # Pass the list of dictionaries to Resend
        resend.Batch.send(batch_params)
        print(f"🚀 Batch sent to {len(recipients)} recipients from list.")
    except Exception as e:
        # This will now give us more detail if it fails again
        print(f"❌ Resend Batch Error: {e}")

if __name__ == "__main__":
    # Check if a filename was provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python send.py <recipient_file.txt>")
        sys.exit(1)

    target_file = sys.argv[1]
    recipient_list = get_recipients(target_file)

    if not os.path.exists("template.mjml"):
        print("❌ Error: template.mjml not found.")
        sys.exit(1)

    with open("template.mjml", "r") as f:
        mjml_source = f.read()
    
    print(f"Compiling MJML and preparing batch for {target_file}...")
    html = compile_mjml(mjml_source)
    send_batch(html, recipient_list)
