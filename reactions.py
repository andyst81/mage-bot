import time
import requests
import json

async def get_reactions(channel):
  time_now = int(time.time())
  start_time = time_now - 86400

  messages = []
  message_data = await channel.history().flatten()
  for message in message_data:
    try:
      embed = message.embeds[0].to_dict()
      url = embed['url']
      m = url.split('/')
      listing_id = m[-1]
      temp_dict = {'listing_id': listing_id, 'message_id': message.id}
      temp_copy = temp_dict.copy()
      messages.append(temp_copy)
    except:
      pass
  # print (messages)

  base_url = 'https://api.thegraph.com/subgraphs/name/froid1911/aavegotchi-lending'
  
  query = '''query getLends($start_time: Int)
  {
    gotchiLendings(
      where: {
        thirdPartyAddress: "0x0d235F7B57ed4E4ca3D6189F1Ac1E13360a1A769", 
        timeAgreed_gte: $start_time
        })
        {
          id
          timeAgreed
          cancelled
        }
  }'''
  variables = {'start_time': start_time}

  response = requests.post(base_url, json={'query': query, 'variables': variables})
  raw_data = response.json()
  data = raw_data['data']['gotchiLendings']
  # print(data)
  for d in data:
    lending_id = d['id']
    # print(message_id)
    for message in messages:
      if message['listing_id'] == lending_id and d['timeAgreed'] != 0:
        # print(lending_id)
        message_id = message['message_id']
        msg = await channel.fetch_message(message_id)
        await msg.add_reaction("✅")
        
  print("reaction loop completed")