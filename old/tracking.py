from datetime import datetime
import requests
import json

def get_performance(gotchi):

  base_url = 'https://api.thegraph.com/subgraphs/name/sudeepb02/gotchi-lending'

  query = '''
    query getPerformance($gotchi_id: Int)
      {gotchiLendings
        (where: {
          gotchiId: $gotchi_id,
          endTimestamp: 0
        }) 
        {
          id
          gotchiId
          agreedPeriod
          actualPeriod
          startTimestamp
          endTimestamp
          upfrontCost
          splitOwner
          splitBorrower
          splitOther
          lender {
            id
          }
          borrower {
            id
          }
          thirdPartyAddress {
            id
          }
          cancelled
          completed
          claimedFUD
          claimedFOMO
          claimedALPHA
          claimedKEK
        }
      }
    
  '''

  variables = {'gotchi_id': int(gotchi)}

  response = requests.post(base_url, json={'query': query, 'variables': variables})
  raw_data = response.json()
  data = raw_data['data']['gotchiLendings'][0]
  print(data)

  borrower = data['borrower']['id']
  start_time = datetime.utcfromtimestamp(int(data['startTimestamp'])).strftime('%H:%M UTC on %d-%m-%Y')
  try:
    agree_period = int(data['agreedPeriod'])/3600
  except:
    agree_period = 0
  actual_period = int(data['actualPeriod'])/3600
  fud = int(data['claimedFUD'])/(10**18)
  fomo = int(data['claimedFOMO'])/(10**18)
  alpha = int(data['claimedALPHA'])/(10**18)
  kek = int(data['claimedKEK'])/(10**18)
  total = fud + fomo + alpha + kek

  message = f'{gotchi} has been lent by {borrower} since {start_time}. \n Time agreed {agree_period} hours, total time left {actual_period} hours. \n Total alchemica collected: {total} \n Total KEK collected: {kek} \n Total ALPHA collected: {alpha} \n Total FOMO collected: {fomo} \n Total FUD collected: {fud}'
  
  return(message)
