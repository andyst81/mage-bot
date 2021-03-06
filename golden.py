import requests
import json
from pycoingecko import CoinGeckoAPI
import discord

cg = CoinGeckoAPI()



def get_alch_prices():
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

  return kek_price, alpha_price, fomo_price, fud_price, ghst_price



async def get_altar_prices(message_channel):

  kek_price, alpha_price, fomo_price, fud_price, ghst_price = get_alch_prices()

  # 3,000 FUD, 1,500 FOMO, 2,000 ALPHA, and 750 KEK
  altar_kek = round(kek_price * 750)
  altar_alpha = round(alpha_price * 2000)
  altar_fomo = round(fomo_price * 1500)
  altar_fud = round(fud_price * 3000)

  altar_price = round(altar_kek + altar_alpha + altar_fomo + altar_fud)
  altar_ghst = round(altar_price / ghst_price)

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
  print(data)
  price_in_wei = data['priceInWei']
  baazaar_price = int(price_in_wei) / 10**18
  # baazaar_usd = round(baazaar_price * ghst_price, 2)

  listing_url = 'https://app.aavegotchi.com/baazaar/erc1155/' + data['id']

  print(altar_price, altar_alpha, altar_fomo, altar_fud, altar_ghst, altar_kek, baazaar_price, listing_url)
  # message = f'Cost of alchemica to craft LE Golden Aaltar is {altar_price} USD, {altar_ghst} GHST. \n{altar_kek} of KEK, {altar_alpha} of ALPHA, {altar_fomo} of FOMO and {altar_fud} of FUD. \nBaazaar floor price is {baazaar_price} GHST, {baazaar_usd} USD. \n{listing_url}'
  embedVar = discord.Embed(
      title=f'LE Golden Altar costs approx {altar_ghst} GHST or {altar_price} USD to buy with alchemica', 
      color=0x8617bb)
  image = discord.File("mage-icon.png", filename="mage-icon.png")
  embedVar.set_author(name="The Order of Portal Mages", icon_url='attachment://mage-icon.png')
  embedVar.set_thumbnail(url="attachment://mage-icon.png")
  embedVar.add_field(name="KEK Cost", value=str(altar_kek) + ' USD', inline=True)
  embedVar.add_field(name="ALPHA Cost", value=str(altar_alpha) + ' USD', inline=True)
  embedVar.add_field(name="FOMO Cost", value=str(altar_fomo) + ' USD', inline=True)
  embedVar.add_field(name="FUD Cost", value=str(altar_fud) + ' USD', inline=True)
  embedVar.add_field(name="Current Baazaar Floor", value=str(baazaar_price) + " GHST", inline=False)
  embedVar.add_field(name="Baazaar Link", value=listing_url, inline=True)
  
  await message_channel.send(file=image, embed=embedVar)
  # return image, embedVar



async def get_tile_prices(message_channel):

  kek_price, alpha_price, fomo_price, fud_price, ghst_price = get_alch_prices()

  # 25 FUD, 25 FOMO, 75 ALPHA, and 25 KEK
  tile_kek = round(kek_price * 25)
  tile_alpha = round(alpha_price * 75)
  tile_fomo = round(fomo_price * 25)
  tile_fud = round(fud_price * 25)

  tile_price = round(tile_kek + tile_alpha + tile_fomo + tile_fud)
  tile_ghst = round(tile_price / ghst_price)

  # query = '''
  # {
  #   erc1155Listings ( 
  #     first: 1,
  #     orderBy: priceInWei,
  #     orderDirection: asc,
  #     where: {
  #     erc1155TokenAddress: "0x19f870bd94a34b3adaa9caa439d333da18d6812a",
  #     cancelled: false,
  #     sold: false
  #   })
  #   {
  #     priceInWei
  #     id
  #   }
  # }
  # '''

  # base_url = 'https://api.thegraph.com/subgraphs/name/aavegotchi/aavegotchi-core-matic'

  # response = requests.post(base_url, json={'query': query})
  # raw_data = response.json()
  # data = raw_data['data']['erc1155Listings'][0]
  # # print(data)
  # price_in_wei = data['priceInWei']
  # baazaar_price = int(price_in_wei) / 10**18
  # baazaar_usd = round(baazaar_price * ghst_price, 2)

  # listing_url = 'https://app.aavegotchi.com/baazaar/erc1155/' + data['id']

  # print(altar_price, altar_alpha, altar_fomo, altar_fud, altar_ghst, altar_kek, baazaar_price, baazaar_usd, listing_url)
  # message = f'Cost of alchemica to craft LE Golden Aaltar is {altar_price} USD, {altar_ghst} GHST. \n{altar_kek} of KEK, {altar_alpha} of ALPHA, {altar_fomo} of FOMO and {altar_fud} of FUD. \nBaazaar floor price is {baazaar_price} GHST, {baazaar_usd} USD. \n{listing_url}'
  embedVar = discord.Embed(
      title=f'LE Golden Tile costs approx {tile_ghst} GHST or {tile_price} USD to buy with alchemica', 
      color=0x8617bb)
  image = discord.File("mage-icon.png", filename="mage-icon.png")
  embedVar.set_author(name="The Order of Portal Mages", icon_url='attachment://mage-icon.png')
  embedVar.set_thumbnail(url="attachment://mage-icon.png")
  embedVar.add_field(name="KEK Cost", value=str(tile_kek) + ' USD', inline=True)
  embedVar.add_field(name="ALPHA Cost", value=str(tile_alpha) + ' USD', inline=True)
  embedVar.add_field(name="FOMO Cost", value=str(tile_fomo) + ' USD', inline=True)
  embedVar.add_field(name="FUD Cost", value=str(tile_fud) + ' USD', inline=True)
  # embedVar.add_field(name="Current Baazaar Floor", value=str(baazaar_price) + " GHST", inline=False)
  # embedVar.add_field(name="Baazaar Link", value=listing_url, inline=True)
  
  await message_channel.send(file=image, embed=embedVar)