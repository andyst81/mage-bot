import requests
import json
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


def get_altar_prices():
  kek_ticker = cg.get_price(ids='aavegotchi-kek', vs_currencies='usd')
  kek_price = kek_ticker['aavegotchi-kek']['usd']

  alpha_ticker = cg.get_price(ids='aavegotchi-alpha', vs_currencies='usd')
  alpha_price = alpha_ticker['aavegotchi-alpha']['usd']

  fomo_ticker = cg.get_price(ids='aavegotchi-fomo', vs_currencies='usd')
  fomo_price = fomo_ticker['aavegotchi-fomo']['usd']

  fud_ticker = cg.get_price(ids='aavegotchi-fud', vs_currencies='usd')
  fud_price = fud_ticker['aavegotchi-fud']['usd']

  ghst_ticker = cg.get_price(ids='aavegotchi', vs_currencies='usd')
  ghst_price = ghst_ticker['aavegotchi']['usd']

  # 3,000 FUD, 1,500 FOMO, 2,000 ALPHA, and 750 KEK
  altar_kek = round(kek_price * 750, 2)
  altar_alpha = round(alpha_price * 2000, 2)
  altar_fomo = round(fomo_price * 1500, 2)
  altar_fud = round(fud_price * 3000, 2)

  altar_price = round(altar_kek + altar_alpha + altar_fomo + altar_fud, 2)
  altar_ghst = round(altar_price / ghst_price, 2)

  query = '''
  {
    erc1155Listings ( 
      first: 1,
      orderBy: priceInWei,
      orderDirection: asc,
      where: {
      erc1155TokenAddress: "0x19f870bd94a34b3adaa9caa439d333da18d6812a",
      cancelled: false,
      sold: false
    })
    {
      priceInWei
      id
    }
  }
  '''

  base_url = 'https://api.thegraph.com/subgraphs/name/aavegotchi/aavegotchi-core-matic'

  response = requests.post(base_url, json={'query': query})
  raw_data = response.json()
  data = raw_data['data']['erc1155Listings'][0]
  # print(data)
  price_in_wei = data['priceInWei']
  baazaar_price = int(price_in_wei) / 10**18
  baazaar_usd = round(baazaar_price * ghst_price, 2)

  listing_url = 'https://app.aavegotchi.com/baazaar/erc1155/' + data['id']

  print(altar_price, altar_alpha, altar_fomo, altar_fud, altar_ghst, altar_kek, baazaar_price, baazaar_usd, listing_url)
  return altar_price, altar_alpha, altar_fomo, altar_fud, altar_ghst, altar_kek, baazaar_price, baazaar_usd, listing_url

if __name__ == '__main__':
  get_altar_prices()