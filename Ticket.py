import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import random
import time
import json
import io
import os
import requests

category_name = 'YOUR_CATEGORY_NAME'
messageID = "YOUR_MESSAGE_ID"
token = "YOUR-TOKEN"

bot = commands.Bot(command_prefix="!", case_intensive=True, intents=discord.Intents.all())
bot.remove_command('help')
bot.launch_time = datetime.utcnow()

@bot.event
async def on_ready():
    print(f'{bot.user.name}')
    print(f'{bot.user.id}')
    print("Online")
    print("-------------")
    await bot.change_presence(activity=discord.Game('coded by Lukas9627'), status=discord.Status.online)

@bot.tree.command(description="Create Ticket Embed")
async def create(interaction: discord.interaction):
  global guildticket
  guildticket = interaction.guild
  embed = discord.Embed(title=f"`{interaction.guild.name}`", description="Um ein Ticket zu erstellen reagiere mit 🎟️.", color="2F3136")
  embed.set_footer(text=f"{interaction.guild.name}",icon_url=f"{interaction.guild.icon_url}")
  embed.timestamp = datetime.utcnow()
  message = await interaction.channel.send(embed=embed)
  await message.add_reaction('🎟️')

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    user = await bot.fetch_user(payload.user_id)
    channel = bot.get_channel(payload.channel_id)
    guild = bot.get_guild(payload.guild_id)

    ######################### APPLY ######################### 

    message_id = payload.message_id
    if message_id == messageID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        if str(payload.emoji) == "🎟️":
          def dm_check(m):
            return m.author.id == user.id and m.guild is None

          if True:
            category = discord.utils.get(guild.categories, name=category_name)
            ticket_channel = await guild.create_text_channel("🎫┃・ticket {}".format(user.name), category=category)
            await ticket_channel.set_permissions(guild.get_role(guild.id), send_messages=False, read_messages=False)
            await ticket_channel.set_permissions(user, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
                        
            embed = discord.Embed(title=f"**Order by** `{guild.name}`",description=f"", color="2F3136")
            embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon_url}")
            embed.set_thumbnail(url=f"{guild.icon_url}")
            embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon_url}")
            mess = await ticket_channel.send(embed=embed)
            await mess.add_reaction('✅')
            await mess.add_reaction('❌')                     

@bot.command()
@commands.has_permissions(manage_messages=True)
async def close(ctx, reason = None):
  membert = discord.utils.get(ctx.channel.members, discriminator=f"{ctx.channel.name[0:4]}")

  if ctx.channel.category.name == f"{category_name}":
    filename = f"transcript.txt"

    with open(filename, "w") as file:
      async for msg in ctx.channel.history(limit=None,oldest_first=True):
        zeit = msg.created_at.strftime("%d/%m/%Y, %H:%M")
        file.write(f"{zeit} - {msg.author} >> {msg.clean_content}\n")

    with open(filename, "rb") as file:
      embed = discord.Embed(title=f"**Log für den Ticket-Channel** `{ctx.channel.name}`", 
                            description=f"{ctx.author.mention}\n`{ctx.author}`\n`({ctx.channel.id})`", color="2F3136")
      embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
      embed.timestamp = datetime.utcnow()
      await membert.send(embed=embed)
      await membert.send(file=discord.File(file,filename=filename))    

    os.remove(f"{filename}")
    await ctx.channel.delete() 

bot.run(token)
