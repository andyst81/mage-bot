import time
import requests
import json

async def get_deletes(channel):

  base_url = 'https://api.thegraph.com/subgraphs/name/froid1911/aavegotchi-lending'

  query = '''query getDeletes
  {
    gotchiLendings(
      where: {
        thirdPartyAddress: "0x0d235F7B57ed4E4ca3D6189F1Ac1E13360a1A769", 
        cancelled: true
        })
        {
          id
          timeAgreed
          cancelled
        }
  }'''

  messages = await channel.history().flatten()
  
  response = requests.post(base_url, json={'query': query})
  raw_data = response.json()
  data = raw_data['data']['gotchiLendings']
  # print(data)
  for d in data:
    message_id = str(d['id'])
    for message in messages:
      try: 
        embed = message.embeds[0].to_dict()
        url = embed['url']
        # print(url)
        m = url.split('/')
        # print(m)
        if message_id in m:
          msg = await channel.fetch_message(message.id)
          await msg.delete()
      except:
        pass
    
    
  print("delete loop completed")