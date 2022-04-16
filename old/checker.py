import time
import requests
import json

async def get_multiples(channel):
    base_url = 'https://static.138.182.90.157.clients.your-server.de/subgraphs/name/aavegotchi/aavegotchi-core-matic-lending-two'

    query = '''
    {gotchiLendings(
      where:{
        thirdPartyAddress:"0x0d235F7B57ed4E4ca3D6189F1Ac1E13360a1A769", 
        completed: false, 
        cancelled: false, 
        timeAgreed_gt: 0
        }) 
      {
        upfrontCost
        period
        lastClaimed
        borrower
        lender
        splitOwner
        splitBorrower
        splitOther
        gotchi {
          name   
        }
      }
    }
    '''

    response = requests.post(base_url, json={'query': query})
    raw_data = response.json()
    data = raw_data['data']['gotchiLendings']

    borrowers = []
    messages = await channel.history().flatten()
    now = time.time()
    yesterday = now - 86400


    for d in data:
      # print(d)
      borrower = d['borrower']
      if borrower not in borrowers:
        borrowers.append(borrower)
      else:
        msg = f':rotating_light: Alert! :rotating_light: {borrower} has borrowed more than one gotchi. \n https://app.aavegotchi.com/aavegotchis/{borrower}'
        if msg not in messages:
          print(msg)
        else:
          for message in messages:
            raw_time = message.created_at
            print(raw_time)
            unix_time = (time.mktime(raw_time.timetuple()))
            if unix_time < yesterday:
              print(msg)
            