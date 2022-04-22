import discord
from discord.ext import tasks
from decouple import config
# from tracking import get_performance
from listings import get_listings
from reactions import get_reactions
# from checker import get_multiples
from golden import get_altar_prices, get_tile_prices

token = config('TOKEN')

bot = discord.Bot()
guild_ids = [880940749422751785] # TOPM
# guild_ids = [953689715759022081] # testing


@tasks.loop(seconds=300)
async def cont_loop():
  print("Loop started")
  channel = bot.get_channel(957337208396861521) # main chat
  # channel = bot.get_channel(953689715759022084) # testing server
  # await get_listings(channel)
  # await get_reactions(channel)
  # await get_multiples(channel)
  print("Loop completed")

@bot.event
async def on_ready():
  print('on ready')
  cont_loop.start()

@bot.event
async def on_message(message):
  managers_channel = bot.get_channel(957358931053776956) # main chat
  # managers_channel = bot.get_channel(953689715759022084) # testing server
  if message.author == bot.user:
    return
  elif message.content.startswith('!altar'):
    await get_altar_prices(managers_channel)
  elif message.content.startswith('!tile'):
    await get_tile_prices(managers_channel)

@bot.slash_command(guild_ids=guild_ids)
async def pass_blunt(ctx, receiver):
  await ctx.respond(f'{ctx.author.name} passes the blunt to {receiver}')

@bot.slash_command(guild_ids=guild_ids)
async def buy_drink(ctx, receiver):
  await ctx.respond(f'{ctx.author.name} bought a drink for {receiver}')

@bot.slash_command(guild_ids=guild_ids)
async def pass_flagon(ctx, receiver):
  await ctx.respond(f'{ctx.author.name} passes a flagon of ale to {receiver}')

@bot.slash_command(guild_ids=guild_ids)
async def slaps(ctx, receiver):
  await ctx.respond(f'{ctx.author.name} slaps {receiver}')

@bot.slash_command(guild_ids=guild_ids)
async def high_fives(ctx, receiver):
  await ctx.respond(f'{ctx.author.name} high fives {receiver}')
  
@bot.slash_command(guild_ids=guild_ids)
async def touch_axes(ctx, receiver):
  await ctx.respond(f'{ctx.author.name} touches axes with {receiver}')

@bot.slash_command(guild_ids=guild_ids)
async def cast_spell(ctx, receiver):
  await ctx.respond(f'{ctx.author.name} casts a spell on {receiver}')

@bot.slash_command(guild_ids=guild_ids)
async def high_five(ctx, receiver):
  await ctx.respond(f'{ctx.author.name} high fives {receiver}')

# @bot.slash_command(guild_ids=guild_ids)
# async def get_perf(ctx, gotchi):
#   message = get_performance(gotchi)
#   await ctx.respond(message)

# @bot.slash_command(guild_ids=guild_ids)
# async def get_renter(gotchi):
#   await get_performance(gotchi)

bot.run(token)