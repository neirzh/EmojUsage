import discord
from discord.ext import commands, tasks
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from datetime import datetime, timedelta
import pytz

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Bangladesh timezone
BD_TIMEZONE = pytz.timezone('Asia/Dhaka')

# Data storage file
DATA_FILE = "emoji_usage.json"

# Load or initialize emoji usage data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save emoji usage data
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Emoji usage tracking
emoji_usage = load_data()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Get current date in BD timezone as string
    now = datetime.now(BD_TIMEZONE).date().strftime('%Y-%m-%d')

    # Extract custom emojis from message
    for emoji in message.content.split():
        if emoji.startswith('<:') or emoji.startswith('<a:'):
            emoji_id = emoji.split(':')[2].rstrip('>')
            if now not in emoji_usage:
                emoji_usage[now] = {}
            emoji_usage[now][emoji_id] = emoji_usage[now].get(emoji_id, 0) + 1

    save_data(emoji_usage)
    await bot.process_commands(message)

# Command to generate emoji usage bar graph
@bot.command()
async def emojusage(ctx):
    # Get last 30 days
    now = datetime.now(BD_TIMEZONE).date()
    last_30_days = [now - timedelta(days=x) for x in range(30)]
    
    # Aggregate usage for last 30 days
    emoji_counts = {}
    for date in last_30_days:
        date_str = date.strftime('%Y-%m-%d')
        if date_str in emoji_usage:
            for emoji_id, count in emoji_usage[date_str].items():
                emoji_counts[emoji_id] = emoji_counts.get(emoji_id, 0) + count

    if not emoji_counts:
        await ctx.send("No emoji usage data for the last 30 days.")
        return

    # Sort by usage (descending) and take top 5 (or all if fewer)
    sorted_emojis = sorted(emoji_counts.items(), key=lambda x: x[1], reverse=True)[:50]
    if not sorted_emojis:
        await ctx.send("No emoji usage data for the last 30 days.")
        return

    emoji_ids, counts = zip(*sorted_emojis)

    # Generate bar graph (portrait orientation)
    plt.figure(figsize=(6, 10))  # Portrait: width 6, height 10
    bars = plt.barh(range(len(counts)), counts, color='blue')
    plt.yticks(range(len(counts)), [f":{discord.utils.get(ctx.guild.emojis, id=int(e)).name}:" if discord.utils.get(ctx.guild.emojis, id=int(e)) else f"Emoji {e}" for e in emoji_ids])
    plt.xlabel('Usage Count (Last 30 Days)')
    plt.title('Emoji Usage')
    plt.tight_layout()

    # Add exact counts on bars
    for bar, count in zip(bars, counts):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{int(count)}', 
                 va='center', ha='left', color='black', fontweight='bold')

    # Save graph
    now = datetime.now(BD_TIMEZONE)
    filename = f"emoji_usage_{now.strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename)
    plt.close()

    # Send graph to the channel
    with open(filename, 'rb') as f:
        await ctx.send(file=discord.File(f, filename=filename))

    # Clean up
    os.remove(filename)

# Replace with your bot token
bot.run('your_bot_token_here')
