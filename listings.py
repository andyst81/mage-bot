from datetime import datetime
import requests
import json
import discord
from owners import get_owners

async def get_listings(channel):
  time_now = datetime.now().strftime('%s')
  last_time = int(time_now) - 900

  message_information = await channel.history().flatten()

  messages = []
  for message in message_information:
    try:
      if message.embeds[0]:
        embed = message.embeds[0].to_dict()
        if embed['url']:
          messages.append(embed['url'])
    except:
      pass


  base_url = 'https://api.thegraph.com/subgraphs/name/froid1911/aavegotchi-lending'

  query = '''query getLends($last_time: Int)
  {
    gotchiLendings(
      where: {
        thirdPartyAddress: "0x0d235F7B57ed4E4ca3D6189F1Ac1E13360a1A769", 
        timeCreated_gte: $last_time
        })
        {
          id
          timeAgreed
          period
          lender
          whitelist {
            id
          }
          gotchi {
            name
            kinship
            withSetsRarityScore
            experience
            level
          }
        }
  }'''
  variables = {'last_time': last_time}

  response = requests.post(base_url, json={'query': query, 'variables': variables})
  raw_data = response.json()
  data = raw_data['data']['gotchiLendings']
  # print(data)
  for d in data:
    owner_address = d['lender']
    owner_discord = get_owners(owner_address)
    id = d['id']
    name = d['gotchi']['name']
    # kinship = d['gotchi']['kinship']
    # brs = d['gotchi']['withSetsRarityScore']
    # experience = d['gotchi']['experience']
    # level = d['gotchi']['level']
    period = int(d['period'])/3600
    whitelist = d['whitelist']['id']
    listing_url = "https://app.aavegotchi.com/lending/" + id
    
    embedVar = discord.Embed(
      title=f'**{name}** is available!', 
      url=listing_url, 
      description=f"A fine new gotchi from the Portal Mages is available to rent for {period} hours", 
      color=0x8617bb)
    embedVar.add_field(name="Whitelist", value=whitelist, inline=False)
    # embedVar.add_field(name="Rarity", value=brs, inline=True)
    # embedVar.add_field(name="Kinship", value=kinship, inline=True)
    # embedVar.add_field(name="Experience", value=experience, inline=True)
    # embedVar.add_field(name="Level", value=level, inline=False)
    embedVar.add_field(name="Owner Discord", value='@'+owner_discord, inline=False)

    if listing_url in messages:
      pass
    else:
      await channel.send(embed=embedVar)
  
  print("listing loop completed")
