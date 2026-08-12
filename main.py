# import discord
from discord import app_commands
import os
import random
import datetime
import asyncio
import json
import math
import re
import requests
from typing import Optional
from flask import Flask
import threading
import time
import hashlib
import base64
import string
import uuid
import urllib.parse
import html
import xml.etree.ElementTree as ET

# ==================== KEEP-ALIVE SYSTEM ====================
def keep_alive():
    while True:
        time.sleep(300)
        print("🔄 Keeping bot alive...")

threading.Thread(target=keep_alive, daemon=True).start()

# ==================== CONFIGURATION ====================
OWNER_ID = 1499789411376955585

ROLES = {
    "FOUNDER": "FOUNDER",
    "STAFF": "STAFF",
    "MOD": "MOD",
    "HELPER": "HELPER",
    "HITTER1": "#1 HITTER",
    "HITTER2": "#2 HITTER",
    "HITTER3": "#3 HITTER",
    "ADVERTISER1": "#1 ADVERTISER",
    "ADVERTISER2": "#2 ADVERTISER",
    "ADVERTISER3": "#3 ADVERTISER",
    "PARTNER": "PARTNER",
    "VERIFIED": "VERIFIED"
}

# ==================== PERMISSION CHECKS ====================
def has_role(interaction: discord.Interaction, role_name: str) -> bool:
    if not interaction.guild:
        return False
    role = discord.utils.get(interaction.guild.roles, name=role_name)
    return role in interaction.user.roles if role else False

def has_any_role(interaction: discord.Interaction, role_names: list) -> bool:
    return any(has_role(interaction, role) for role in role_names)

def is_owner(interaction: discord.Interaction) -> bool:
    return interaction.user.id == OWNER_ID

def is_founder(interaction: discord.Interaction) -> bool:
    return is_owner(interaction) or has_role(interaction, ROLES["FOUNDER"])

def is_staff(interaction: discord.Interaction) -> bool:
    return has_role(interaction, ROLES["STAFF"])

def is_mod(interaction: discord.Interaction) -> bool:
    return has_role(interaction, ROLES["MOD"])

def is_helper(interaction: discord.Interaction) -> bool:
    return has_role(interaction, ROLES["HELPER"])

def is_hitter(interaction: discord.Interaction) -> bool:
    return has_any_role(interaction, [ROLES["HITTER1"], ROLES["HITTER2"], ROLES["HITTER3"]])

def is_advertiser(interaction: discord.Interaction) -> bool:
    return has_any_role(interaction, [ROLES["ADVERTISER1"], ROLES["ADVERTISER2"], ROLES["ADVERTISER3"]])

def is_partner(interaction: discord.Interaction) -> bool:
    return has_role(interaction, ROLES["PARTNER"])

def is_verified(interaction: discord.Interaction) -> bool:
    return has_role(interaction, ROLES["VERIFIED"])

def has_minimum_role(interaction: discord.Interaction) -> bool:
    return is_verified(interaction) or is_partner(interaction) or is_advertiser(interaction) or is_hitter(interaction) or is_helper(interaction) or is_mod(interaction) or is_staff(interaction) or is_founder(interaction)

# ==================== BOT SETUP ====================
intents = discord.Intents.all()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# ==================== DATA STORE ====================
economy = {}
levels = {}
warnings = {}
tickets = {}
giveaways = {}
reminders = {}
suggestions = {}
reports = {}
marriage = {}
pets = {}
daily_streak = {}
inventory = {}
achievements = {}
blacklist = {}
muted = {}
reaction_roles = {}
auto_roles = {}
welcome_channels = {}
log_channels = {}
suggestion_channels = {}
report_channels = {}
ticket_channels = {}
giveaway_channels = {}
starboard = {}
counting = {}
minesweeper_games = {}
wordle_games = {}
hangman_games = {}
trivia_games = {}
blackjack_games = {}
typing_games = {}
tictactoe_games = {}
memory_games = {}
poker_games = {}
roulette_games = {}
slot_games = {}
craps_games = {}
baccarat_games = {}
keno_games = {}
bingo_games = {}
plinko_games = {}
wheel_games = {}

# ==================== SHOP ITEMS ====================
shop_items = {
    "🍕 Pizza": 50,
    "🎮 Game": 100,
    "💎 Diamond": 500,
    "👑 Crown": 1000,
    "🚗 Car": 2000,
    "🏠 House": 5000,
    "🛡️ Shield": 300,
    "⚔️ Sword": 400,
    "🎯 Target": 150,
    "📚 Book": 75,
    "🧪 Potion": 200,
    "🔮 Crystal": 350,
    "🎵 Music": 80,
    "🍦 Ice Cream": 25,
    "🎨 Art": 120,
    "🏆 Trophy": 800,
    "🎁 Gift": 250,
    "💊 Health": 180,
    "⚡ Energy": 220,
    "🌟 Star": 600,
    "🌙 Moon": 700,
    "☀️ Sun": 900,
    "🌍 Earth": 1200,
    "🪐 Saturn": 1500,
    "🚀 Rocket": 2500,
    "🛸 UFO": 3000,
    "👾 Alien": 2000,
    "🤖 Robot": 1800,
    "🧠 Brain": 400,
    "❤️ Heart": 350,
    "💀 Skull": 450,
    "👑 Crown": 1000,
    "🗡️ Knife": 600,
    "🏹 Bow": 700,
    "🪓 Axe": 800,
    "🔨 Hammer": 550,
    "⚒️ Pickaxe": 500,
    "🧨 Bomb": 950,
    "🎆 Firework": 300,
    "🎇 Sparkle": 250,
    "🌈 Rainbow": 400,
    "🌊 Wave": 350,
    "🔥 Fire": 275,
    "❄️ Ice": 300,
    "⚡ Lightning": 325
}

# ==================== HELPER FUNCTIONS ====================
def load_json(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def get_user(user_id):
    if user_id not in economy:
        economy[user_id] = {"balance": 100, "inventory": [], "last_daily": 0, "last_weekly": 0, "last_monthly": 0, "last_hourly": 0}
    return economy[user_id]

def get_achievement(user_id):
    if user_id not in achievements:
        achievements[user_id] = []
    return achievements[user_id]

def add_achievement(user_id, name):
    if name not in achievements[user_id]:
        achievements[user_id].append(name)
        return True
    return False

# ==================== BOT READY ====================
@bot.event
async def on_ready():
    await tree.sync()
    bot.start_time = datetime.datetime.now()
    print(f'✅ Logged in as {bot.user}')
    print(f'📊 Bot is in {len(bot.guilds)} servers')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="/help | 500+ commands"
    ))

# ==================== COMPLETE HELP ====================
@tree.command(name="help", description="Show all 500+ commands")
async def help(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="📋 ULTIMATE MEGA BOT - 500+ COMMANDS",
        description="The most powerful Discord bot with 500+ commands!",
        color=discord.Color.gold()
    )
    categories = {
        "ℹ️ Information (20)": ["ping", "uptime", "info", "botinfo", "serverinfo", "userinfo", "roleinfo", "channelinfo", "emojiinfo", "serverstats", "membercount", "boosters", "banner", "servericon", "serverowner", "serverbanner", "serverinvite", "serveremoji", "serversticker", "serverboosts"],
        "🎲 Fun (35)": ["flip", "roll", "choose", "randomnumber", "rps", "math", "8ball", "fact", "joke", "meme", "cat", "dog", "koala", "panda", "fox", "bird", "fish", "randomcolor", "randomword", "randomletter", "randomemoji", "randomquote", "randomname", "randompassword", "randomhex", "randomuuid", "randomdate", "randomtime", "randomip", "randommac", "randomhash", "randomemoji", "randomascii", "randombinary"],
        "🛡️ Moderation (30)": ["kick", "ban", "clear", "timeout", "warn", "warnings", "removewarn", "slowmode", "lock", "unlock", "poll", "announce", "purgeuser", "nickname", "softban", "unban", "mute", "unmute", "addrole", "removerole", "addroleall", "removeroleall", "rename", "createchannel", "deletechannel", "createrole", "deleterole", "settopic", "clonechannel", "movechannel"],
        "🎮 Games (40)": ["guess", "slots", "blackjack", "typerace", "hangman", "trivia", "wordle", "memory", "tictactoe", "numbergame", "quiz", "riddle", "scramble", "anagram", "minesweeper", "2048", "snake", "pong", "tetris", "pacman", "roulette", "craps", "baccarat", "keno", "bingo", "plinko", "wheel", "poker", "casino", "chess", "checkers", "dominoes", "mahjong", "sudoku", "crossword", "jigsaw", "maze", "adventure", "trivia2", "quiz2"],
        "💰 Economy (40)": ["balance", "daily", "weekly", "monthly", "hourly", "work", "steal", "give", "donate", "transfer", "shop", "buy", "inventory", "gamble", "coinflip", "lottery", "rob", "bank", "invest", "beg", "mine", "fish", "hunt", "farm", "craft", "brew", "cook", "trade", "sell", "auction", "bidding", "deposit", "withdraw", "interest", "stocks", "bonds", "realestate", "business", "salary", "bonus"],
        "💍 Social (35)": ["marry", "divorce", "kiss", "hug", "pat", "slap", "punch", "kickuser", "highfive", "handshake", "wave", "dance", "sing", "sleep", "eat", "drink", "walk", "run", "jump", "fly", "swim", "climb", "cook", "paint", "write", "cuddle", "tickle", "bite", "bonk", "smug", "cry", "blush", "stare", "smile", "laugh"],
        "🐾 Pets (20)": ["pet", "feed", "play", "walkpet", "petstats", "breed", "adopt", "train", "petbattle", "petlist", "petname", "petfeed", "petplay", "petclean", "petgroom", "petlove", "pethealth", "petenergy", "petmood", "petlevel"],
        "📈 Leveling (15)": ["level", "leaderboard", "rank", "xp", "top10", "levels", "setlevel", "addxp", "removexp", "resetlevels", "reward", "prestige", "badge", "title", "rolelevel"],
        "🔧 Utility (50)": ["time", "date", "avatar", "invite", "weather", "translate", "calculate", "screenshot", "shortenurl", "qrcode", "color", "emoji", "hashtag", "trending", "news", "define", "synonym", "antonym", "rhyme", "password", "uuid", "base64encode", "base64decode", "hash", "timestamp", "countdown", "remind", "reminders", "removemind", "todo", "addtodo", "donetodo", "removetodo", "listtodo", "alarm", "timer", "stopwatch", "calendar", "schedule", "event", "birthday", "anniversary", "countdown2", "timezone", "worldclock", "currency", "crypto", "stock", "weather2", "airquality"],
        "👑 Admin (50)": ["setbalance", "addcoins", "removecoins", "resetbalance", "resetwarnings", "setlevel", "addxp", "removexp", "resetlevels", "cleardata", "backup", "restore", "blacklist", "unblacklist", "addroleall", "removeroleall", "giverole", "takerole", "rename", "reset", "createchannel", "deletechannel", "createrole", "deleterole", "renamechannel", "movechannel", "clonechannel", "settopic", "setwelcome", "setlogs", "setsuggestions", "setreports", "settickets", "setgiveaway", "setcounting", "setstarboard", "setautorole", "setreactionrole", "lockall", "unlockall", "setvanity", "setboost", "setlevelroles", "setxpchannel", "seteconomy", "setgamble", "setcasino"],
        "👑 Owner (70)": ["serverlist", "leaveserver", "broadcast", "exportdata", "importdata", "cleareconomy", "clearlevels", "purgeall", "restart", "shutdown", "status", "servers", "blacklistuser", "unblacklistuser", "giveaway", "endgiveaway", "addroleall", "removeroleall", "setwelcome", "setlogs", "setsuggestions", "setreports", "settickets", "setgiveaway", "setcounting", "setstarboard", "setautorole", "setreactionrole", "lockall", "unlockall", "setvanity", "setboost", "setlevelroles", "setxpchannel", "seteconomy", "setgamble", "setcasino", "eval", "exec", "cmd", "shell", "setbotname", "setavatar", "setgame", "setstream", "setlistening", "setwatching", "setactivity", "setserver", "deleteallchannels", "deleteallroles", "massban", "masskick", "masspurge", "createinvite", "cloneguild", "copyguild", "backupguild", "restoreguild", "exportguild", "importguild", "resetguild", "optimize", "cleanup", "purgebots", "purgehumans"]
    }
    for cat, cmds in categories.items():
        embed.add_field(name=cat, value="`/" + "`, `/".join(cmds[:5]) + "`...", inline=False)
    embed.set_footer(text=f"Requested by {interaction.user.name} | Total: 500+ commands")
    await interaction.response.send_message(embed=embed)

# ==================== INFORMATION COMMANDS ====================
@tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    await interaction.response.send_message(f'🏓 Pong! Latency: `{round(bot.latency*1000)}ms`')

@tree.command(name="uptime", description="Check bot uptime")
async def uptime(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    now = datetime.datetime.now()
    uptime = now - bot.start_time if hasattr(bot, 'start_time') else datetime.timedelta(seconds=0)
    days, remainder = divmod(int(uptime.total_seconds()), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    await interaction.response.send_message(f"⏱️ Uptime: **{days}d {hours}h {minutes}m {seconds}s**")

@tree.command(name="info", description="Bot information")
async def info(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    embed = discord.Embed(title="🤖 Bot Info", color=discord.Color.blue())
    embed.add_field(name="Name", value=bot.user.name, inline=True)
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Users", value=len(bot.users), inline=True)
    embed.add_field(name="Commands", value="500+", inline=True)
    embed.add_field(name="Latency", value=f"{round(bot.latency*1000)}ms", inline=True)
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None)
    await interaction.response.send_message(embed=embed)

@tree.command(name="botinfo", description="Detailed bot statistics")
async def botinfo(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    embed = discord.Embed(title="📊 Bot Statistics", color=discord.Color.purple())
    embed.add_field(name="Name", value=bot.user.name, inline=True)
    embed.add_field(name="ID", value=bot.user.id, inline=True)
    embed.add_field(name="Created", value=bot.user.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Users", value=len(bot.users), inline=True)
    embed.add_field(name="Ping", value=f"{round(bot.latency*1000)}ms", inline=True)
    embed.add_field(name="Commands", value="500+", inline=True)
    embed.add_field(name="Python", value="3.13", inline=True)
    embed.add_field(name="discord.py", value="2.5+", inline=True)
    await interaction.response.send_message(embed=embed)

@tree.command(name="serverinfo", description="Server information")
async def serverinfo(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    guild = interaction.guild
    embed = discord.Embed(title=f"📊 {guild.name}", color=discord.Color.green())
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="Boosts", value=guild.premium_subscription_count or 0, inline=True)
    embed.add_field(name="Boost Level", value=guild.premium_tier or 0, inline=True)
    embed.add_field(name="Vanity URL", value=guild.vanity_url_code or "None", inline=True)
    embed.add_field(name="Banner", value="Yes" if guild.banner else "No", inline=True)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    if guild.banner:
        embed.set_image(url=guild.banner.url)
    await interaction.response.send_message(embed=embed)

@tree.command(name="userinfo", description="User information")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if member is None:
        member = interaction.user
    embed = discord.Embed(title=f"👤 {member.name}", color=member.color)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M") if member.joined_at else "Unknown", inline=True)
    embed.add_field(name="Joined Discord", value=member.created_at.strftime("%Y-%m-%d %H:%M"), inline=True)
    embed.add_field(name="Bot", value="Yes" if member.bot else "No", inline=True)
    embed.add_field(name="Status", value=str(member.status).title(), inline=True)
    embed.add_field(name="Nickname", value=member.nickname or "None", inline=True)
    embed.add_field(name="Highest Role", value=member.top_role.mention if member.top_role else "None", inline=True)
    embed.add_field(name="Boost Since", value=member.premium_since.strftime("%Y-%m-%d") if member.premium_since else "None", inline=True)
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    await interaction.response.send_message(embed=embed)

@tree.command(name="roleinfo", description="Role information")
async def roleinfo(interaction: discord.Interaction, role: discord.Role):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    embed = discord.Embed(title=f"🎭 {role.name}", color=role.color)
    embed.add_field(name="ID", value=role.id, inline=True)
    embed.add_field(name="Color", value=str(role.color), inline=True)
    embed.add_field(name="Members", value=len(role.members), inline=True)
    embed.add_field(name="Created", value=role.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Hoisted", value="Yes" if role.hoist else "No", inline=True)
    embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
    embed.add_field(name="Bot Role", value="Yes" if role.is_bot_managed() else "No", inline=True)
    embed.add_field(name="Position", value=role.position, inline=True)
    await interaction.response.send_message(embed=embed)

@tree.command(name="channelinfo", description="Channel information")
async def channelinfo(interaction: discord.Interaction, channel: discord.TextChannel = None):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if channel is None:
        channel = interaction.channel
    embed = discord.Embed(title=f"💬 #{channel.name}", color=discord.Color.blue())
    embed.add_field(name="ID", value=channel.id, inline=True)
    embed.add_field(name="Category", value=channel.category.name if channel.category else "None", inline=True)
    embed.add_field(name="Created", value=channel.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="NSFW", value="Yes" if channel.nsfw else "No", inline=True)
    embed.add_field(name="Slowmode", value=f"{channel.slowmode_delay}s" if channel.slowmode_delay else "Off", inline=True)
    embed.add_field(name="Position", value=channel.position, inline=True)
    await interaction.response.send_message(embed=embed)

@tree.command(name="emojiinfo", description="Emoji information")
async def emojiinfo(interaction: discord.Interaction, emoji: discord.Emoji):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    embed = discord.Embed(title=f"🎨 {emoji.name}", color=discord.Color.gold())
    embed.add_field(name="ID", value=emoji.id, inline=True)
    embed.add_field(name="Created", value=emoji.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Animated", value="Yes" if emoji.animated else "No", inline=True)
    embed.add_field(name="Managed", value="Yes" if emoji.managed else "No", inline=True)
    embed.add_field(name="Guild", value=emoji.guild.name, inline=True)
    embed.set_thumbnail(url=emoji.url)
    await interaction.response.send_message(embed=embed)

@tree.command(name="serverstats", description="Server statistics")
async def serverstats(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    guild = interaction.guild
    bots = sum(1 for m in guild.members if m.bot)
    humans = guild.member_count - bots
    online = sum(1 for m in guild.members if m.status != discord.Status.offline)
    idle = sum(1 for m in guild.members if m.status == discord.Status.idle)
    dnd = sum(1 for m in guild.members if m.status == discord.Status.dnd)
    embed = discord.Embed(title=f"📊 {guild.name}", color=discord.Color.blue())
    embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
    embed.add_field(name="👤 Humans", value=humans, inline=True)
    embed.add_field(name="🤖 Bots", value=bots, inline=True)
    embed.add_field(name="🟢 Online", value=online, inline=True)
    embed.add_field(name="🟡 Idle", value=idle, inline=True)
    embed.add_field(name="🔴 DND", value=dnd, inline=True)
    embed.add_field(name="💬 Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="🎭 Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="📅 Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
    await interaction.response.send_message(embed=embed)

@tree.command(name="membercount", description="Member count")
async def membercount(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    await interaction.response.send_message(f"👥 {interaction.guild.name} has **{interaction.guild.member_count}** members")

@tree.command(name="boosters", description="Server boosters")
async def boosters(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    guild = interaction.guild
    boosters = [m for m in guild.members if m.premium_since]
    if not boosters:
        await interaction.response.send_message("❌ No boosters")
        return
    booster_list = "\n".join([f"• {b.mention} (Since: {b.premium_since.strftime('%Y-%m-%d')})" for b in boosters[:15]])
    embed = discord.Embed(title=f"✨ Boosters ({len(boosters)})", color=discord.Color.purple())
    embed.add_field(name="Boosters", value=booster_list or "No boosters", inline=False)
    embed.add_field(name="Boost Level", value=guild.premium_tier or 0, inline=True)
    embed.add_field(name="Total Boosts", value=guild.premium_subscription_count or 0, inline=True)
    await interaction.response.send_message(embed=embed)

@tree.command(name="banner", description="Server banner")
async def banner(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if interaction.guild.banner:
        embed = discord.Embed(title=f"🖼️ {interaction.guild.name}", color=discord.Color.blue())
        embed.set_image(url=interaction.guild.banner.url)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("❌ No banner")

@tree.command(name="servericon", description="Server icon")
async def servericon(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if interaction.guild.icon:
        embed = discord.Embed(title=f"🖼️ {interaction.guild.name}", color=discord.Color.blue())
        embed.set_image(url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("❌ No icon")

@tree.command(name="serverowner", description="Server owner")
async def serverowner(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    await interaction.response.send_message(f"👑 Server owner: {interaction.guild.owner.mention}")

@tree.command(name="serverbanner", description="Server banner with details")
async def serverbanner(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    guild = interaction.guild
    embed = discord.Embed(title=f"🖼️ {guild.name}", color=discord.Color.blue())
    if guild.banner:
        embed.set_image(url=guild.banner.url)
        embed.add_field(name="Banner", value="Yes", inline=True)
    else:
        embed.add_field(name="Banner", value="No banner set", inline=True)
    await interaction.response.send_message(embed=embed)

@tree.command(name="serverinvite", description="Get server invite link")
async def serverinvite(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    try:
        invite = await interaction.channel.create_invite(max_age=86400, max_uses=1)
        await interaction.response.send_message(f"🔗 Server invite: {invite.url}")
    except:
        await interaction.response.send_message("❌ Can't create invite (missing permissions)")

@tree.command(name="serveremoji", description="List all server emojis")
async def serveremoji(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    emojis = interaction.guild.emojis
    if not emojis:
        await interaction.response.send_message("❌ No emojis")
        return
    embed = discord.Embed(title=f"🎨 Server Emojis ({len(emojis)})", color=discord.Color.gold())
    emoji_list = "\n".join([f"{e} - {e.name}" for e in emojis[:25]])
    embed.add_field(name="Emojis", value=emoji_list or "No emojis", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="serversticker", description="List all server stickers")
async def serversticker(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    stickers = interaction.guild.stickers
    if not stickers:
        await interaction.response.send_message("❌ No stickers")
        return
    embed = discord.Embed(title=f"🔖 Server Stickers ({len(stickers)})", color=discord.Color.blue())
    sticker_list = "\n".join([f"• {s.name}" for s in stickers[:25]])
    embed.add_field(name="Stickers", value=sticker_list or "No stickers", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="serverboosts", description="Server boost statistics")
async def serverboosts(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    guild = interaction.guild
    embed = discord.Embed(title=f"✨ Boost Statistics", color=discord.Color.purple())
    embed.add_field(name="Boost Level", value=guild.premium_tier or 0, inline=True)
    embed.add_field(name="Total Boosts", value=guild.premium_subscription_count or 0, inline=True)
    embed.add_field(name="Boosters", value=len([m for m in guild.members if m.premium_since]), inline=True)
    await interaction.response.send_message(embed=embed)

# ==================== FUN COMMANDS ====================
@tree.command(name="flip", description="Flip a coin")
async def flip(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    await interaction.response.send_message(f'**{random.choice(["Heads 🪙", "Tails 🪙"])}**!')

@tree.command(name="roll", description="Roll a dice")
async def roll(interaction: discord.Interaction, sides: int = 6):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if sides < 2:
        await interaction.response.send_message("❌ Must be at least 2 sides!", ephemeral=True)
        return
    await interaction.response.send_message(f'🎲 You rolled **{random.randint(1, sides)}** (1-{sides})')

@tree.command(name="choose", description="Choose between options")
async def choose(interaction: discord.Interaction, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None, option6: str = None, option7: str = None):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    options = [o for o in [option1, option2, option3, option4, option5, option6, option7] if o]
    await interaction.response.send_message(f'🤔 I choose **{random.choice(options)}**!')

@tree.command(name="randomnumber", description="Random number")
async def randomnumber(interaction: discord.Interaction, min: int, max: int):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if min > max:
        await interaction.response.send_message("❌ Min must be less than max!", ephemeral=True)
        return
    await interaction.response.send_message(f'🔢 **{random.randint(min, max)}**')

@tree.command(name="rps", description="Rock Paper Scissors")
async def rps(interaction: discord.Interaction, choice: str):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    choices = ["rock", "paper", "scissors"]
    if choice.lower() not in choices:
        await interaction.response.send_message("❌ Choose rock, paper, or scissors", ephemeral=True)
        return
    bot_choice = random.choice(choices)
    if choice.lower() == bot_choice:
        result = "It's a tie! 🤝"
    elif (choice.lower() == "rock" and bot_choice == "scissors") or \
         (choice.lower() == "paper" and bot_choice == "rock") or \
         (choice.lower() == "scissors" and bot_choice == "paper"):
        result = "You win! 🎉"
    else:
        result = "I win! 😎"
    await interaction.response.send_message(f"🧱 You chose {choice}\n🤖 I chose {bot_choice}\n\n{result}")

@tree.command(name="math", description="Calculate math")
async def math(interaction: discord.Interaction, num1: float, operator: str, num2: float):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    ops = {"+": lambda a,b: a+b, "-": lambda a,b: a-b, "*": lambda a,b: a*b, "/": lambda a,b: a/b if b else None, "^": lambda a,b: a**b, "%": lambda a,b: a%b if b else None}
    if operator not in ops:
        await interaction.response.send_message("❌ Use + - * / ^ %", ephemeral=True)
        return
    result = ops[operator](num1, num2)
    if result is None:
        await interaction.response.send_message("❌ Cannot divide/mod by zero!", ephemeral=True)
        return
    await interaction.response.send_message(f"🧮 `{num1} {operator} {num2} = {result}`")

@tree.command(name="8ball", description="Ask the magic 8-ball")
async def eightball(interaction: discord.Interaction, question: str):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    responses = ["It is certain 🎱", "It is decidedly so 🎱", "Without a doubt 🎱", "Yes definitely 🎱", "You may rely on it 🎱", "As I see it, yes 🎱", "Most likely 🎱", "Outlook good 🎱", "Yes 🎱", "Signs point to yes 🎱", "Reply hazy, try again 🎱", "Ask again later 🎱", "Better not tell you now 🎱", "Cannot predict now 🎱", "Concentrate and ask again 🎱", "Don't count on it 🎱", "My reply is no 🎱", "My sources say no 🎱", "Outlook not so good 🎱", "Very doubtful 🎱"]
    await interaction.response.send_message(f"🎱 Question: *{question}*\n\n**{random.choice(responses)}**")

@tree.command(name="fact", description="Random fact")
async def fact(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    facts = ["Honey never spoils 🍯", "Octopuses have three hearts 🐙", "Bananas are berries 🍌", "A day on Venus is longer than a year 🪐", "Cows have best friends 🐄", "A group of flamingos is called a flamboyance 🦩", "The shortest war was 38 minutes ⚔️", "Bamboo can grow up to 3 feet in a day 🎋", "The human nose can detect over 1 trillion smells 👃", "Butterflies taste with their feet 🦋", "Slugs have four noses 🐌", "A jiffy is 1/100th of a second ⏱️", "Koalas have human-like fingerprints 🐨", "Birds are the only animals with feathers 🐦", "Cats sleep 70% of their lives 🐱", "Dolphins have names for each other 🐬", "Elephants can't jump 🐘", "Giraffes have blue tongues 🦒", "Horses can sleep standing up 🐴", "Lions are the only social big cats 🦁", "Penguins propose with pebbles 🐧", "Sloths can hold their breath for 40 minutes 🦥", "Kangaroos can't walk backwards 🦘", "Crocodiles can't stick out their tongues 🐊", "Flamingos are born gray 🦩", "Hummingbirds can fly backwards 🐦", "Chameleons change color to communicate 🦎", "Starfish can regenerate arms ⭐", "Cows produce more milk when listening to music 🐄", "Butterflies taste with their feet 🦋"]
    await interaction.response.send_message(f"💡 **{random.choice(facts)}**")

@tree.command(name="joke", description="Random joke")
async def joke(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    jokes = ["Why don't scientists trust atoms? Because they make up everything! ⚛️", "What do you call a fish with no eyes? A fsh! 🐟", "Why did the scarecrow win an award? He was outstanding in his field! 🌾", "What do you call a bear with no teeth? A gummy bear! 🧸", "Why don't skeletons fight each other? They don't have the guts! 💀", "What do you call a fake noodle? An impasta! 🍝", "Why did the bicycle fall over? It was two-tired! 🚲", "What do you call a snowman with a carrot nose? A chill guy! ⛄", "Why did the math book look so sad? It had too many problems! 📚", "What do you call a sleeping dinosaur? A dino-snore! 🦕", "Why did the chicken cross the road? To get to the other side! 🐔", "What do you call a cow with no legs? Ground beef! 🐄", "Why do seagulls fly over the sea? Because if they flew over the bay, they'd be bagels! 🥯", "What do you call a bear that got caught in the rain? A drizzly bear! 🐻", "Why did the banana go to the doctor? He wasn't peeling well! 🍌", "What do you call a magic dog? A labracadabrador! 🐕", "Why did the tomato turn red? Because it saw the salad dressing! 🍅", "What do you call a sleeping cow? A bull-dozer! 🐮", "Why did the gym close down? It just didn't work out! 💪", "What do you call a sad strawberry? A blueberry! 🍓"]
    await interaction.response.send_message(f"😂 {random.choice(jokes)}")

@tree.command(name="meme", description="Random meme")
async def meme(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    try:
        resp = requests.get("https://meme-api.com/gimme")
        if resp.status_code == 200:
            data = resp.json()
            embed = discord.Embed(title=data['title'], color=discord.Color.random())
            embed.set_image(url=data['url'])
            embed.set_footer(text=f"👍 {data['ups']} | r/{data['subreddit']}")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ Could not fetch meme")
    except:
        await interaction.response.send_message("❌ API error")

@tree.command(name="cat", description="Random cat picture")
async def cat(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    try:
        resp = requests.get("https://api.thecatapi.com/v1/images/search")
        if resp.status_code == 200:
            data = resp.json()
            embed = discord.Embed(title="🐱 Meow!", color=discord.Color.random())
            embed.set_image(url=data[0]['url'])
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ Could not fetch cat")
    except:
        await interaction.response.send_message("❌ API error")

@tree.command(name="dog", description="Random dog picture")
async def dog(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    try:
        resp = requests.get("https://api.thedogapi.com/v1/images/search")
        if resp.status_code == 200:
            data = resp.json()
            embed = discord.Embed(title="🐶 Woof!", color=discord.Color.random())
            embed.set_image(url=data[0]['url'])
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ Could not fetch dog")
    except:
        await interaction.response.send_message("❌ API error")

@tree.command(name="randomcolor", description="Random color")
async def randomcolor(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    r, g, b = random.randint(0,255), random.randint(0,255), random.randint(0,255)
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    embed = discord.Embed(title=f"🎨 {hex_color}", color=int(hex_color[1:], 16))
    await interaction.response.send_message(embed=embed)

@tree.command(name="randomword", description="Random word")
async def randomword(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    words = ["apple", "banana", "cherry", "dragon", "elephant", "forest", "garden", "happy", "island", "jungle", "knight", "lion", "mountain", "night", "ocean", "pizza", "queen", "river", "sun", "tree", "umbrella", "village", "water", "xray", "yellow", "zebra", "arcade", "blizzard", "crystal", "diamond", "ember", "frost", "galaxy", "haven", "ice", "jade", "karma", "lunar", "mystic", "nova", "orbit", "phantom", "quartz", "rainbow", "shadow", "titan", "ultimate", "vortex", "whisper", "xenon", "youth", "zenith"]
    await interaction.response.send_message(f"📝 **{random.choice(words)}**")

@tree.command(name="randomletter", description="Random letter")
async def randomletter(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    await interaction.response.send_message(f"🔤 **{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}**")

@tree.command(name="randomemoji", description="Random emoji")
async def randomemoji(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    emojis = ["😂", "❤️", "🔥", "💀", "👀", "💯", "🤔", "😭", "🥺", "😊", "🤣", "💕", "✨", "😍", "🙏", "😅", "💪", "👋", "🤗", "🎉", "🫶", "😎", "💖", "🙌", "🤩", "🥰", "😘", "💗", "🥳", "😁"]
    await interaction.response.send_message(f"🎯 **{random.choice(emojis)}**")

@tree.command(name="randomquote", description="Random quote")
async def randomquote(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    quotes = ["The only way to do great work is to love what you do. - Steve Jobs", "Life is what happens when you're busy making other plans. - John Lennon", "In the end, we will remember not the words of our enemies, but the silence of our friends. - Martin Luther King Jr.", "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt", "It does not matter how slowly you go as long as you do not stop. - Confucius", "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill", "Believe you can and you're halfway there. - Theodore Roosevelt", "The only impossible journey is the one you never begin. - Tony Robbins", "Start where you are. Use what you have. Do what you can. - Arthur Ashe", "Don't watch the clock; do what it does. Keep going. - Sam Levenson"]
    await interaction.response.send_message(f"💬 **{random.choice(quotes)}**")

@tree.command(name="randomname", description="Random name")
async def randomname(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan", "Jessica", "Sarah", "Karen"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee"]
    await interaction.response.send_message(f"👤 **{random.choice(first_names)} {random.choice(last_names)}**")

@tree.command(name="randompassword", description="Random password")
async def randompassword(interaction: discord.Interaction, length: int = 12):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if length < 6 or length > 32:
        await interaction.response.send_message("❌ Length must be between 6 and 32", ephemeral=True)
        return
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = ''.join(random.choice(chars) for _ in range(length))
    await interaction.response.send_message(f"🔑 **{password}**")

@tree.command(name="randomhex", description="Random hex color")
async def randomhex(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    hex_color = random.randint(0, 0xFFFFFF)
    await interaction.response.send_message(f"🎨 **#{hex_color:06x}**")

# ==================== ECONOMY COMMANDS ====================
@tree.command(name="balance", description="Check your balance")
async def balance(interaction: discord.Interaction, member: discord.Member = None):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if member is None:
        member = interaction.user
    data = get_user(str(member.id))
    await interaction.response.send_message(f"💰 {member.mention} has **{data['balance']}** coins")

@tree.command(name="daily", description="Claim daily reward")
async def daily(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    user_id = str(interaction.user.id)
    data = get_user(user_id)
    now = datetime.datetime.now().timestamp()
    if now - data['last_daily'] < 86400:
        hours = int((86400 - (now - data['last_daily'])) / 3600) + 1
        await interaction.response.send_message(f"⏰ Already claimed, come back in {hours}h", ephemeral=True)
        return
    reward = random.randint(50, 200)
    data['balance'] += reward
    data['last_daily'] = now
    add_achievement(user_id, "Daily Collector")
    await interaction.response.send_message(f"✅ You got **{reward}** coins!")

@tree.command(name="weekly", description="Claim weekly reward")
async def weekly(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    user_id = str(interaction.user.id)
    data = get_user(user_id)
    now = datetime.datetime.now().timestamp()
    if now - data.get('last_weekly', 0) < 604800:
        days = int((604800 - (now - data.get('last_weekly', 0))) / 86400) + 1
        await interaction.response.send_message(f"⏰ Already claimed, come back in {days}d", ephemeral=True)
        return
    reward = random.randint(500, 1000)
    data['balance'] += reward
    data['last_weekly'] = now
    add_achievement(user_id, "Weekly Warrior")
    await interaction.response.send_message(f"✅ You got **{reward}** coins!")

@tree.command(name="monthly", description="Claim monthly reward")
async def monthly(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    user_id = str(interaction.user.id)
    data = get_user(user_id)
    now = datetime.datetime.now().timestamp()
    if now - data.get('last_monthly', 0) < 2592000:
        days = int((2592000 - (now - data.get('last_monthly', 0))) / 86400) + 1
        await interaction.response.send_message(f"⏰ Already claimed, come back in {days}d", ephemeral=True)
        return
    reward = random.randint(2000, 5000)
    data['balance'] += reward
    data['last_monthly'] = now
    add_achievement(user_id, "Monthly Master")
    await interaction.response.send_message(f"✅ You got **{reward}** coins!")

@tree.command(name="hourly", description="Claim hourly reward")
async def hourly(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    user_id = str(interaction.user.id)
    data = get_user(user_id)
    now = datetime.datetime.now().timestamp()
    if now - data.get('last_hourly', 0) < 3600:
        minutes = int((3600 - (now - data.get('last_hourly', 0))) / 60) + 1
        await interaction.response.send_message(f"⏰ Already claimed, come back in {minutes}m", ephemeral=True)
        return
    reward = random.randint(10, 30)
    data['balance'] += reward
    data['last_hourly'] = now
    await interaction.response.send_message(f"✅ You got **{reward}** coins!")

@tree.command(name="work", description="Work for coins")
async def work(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    jobs = ["programmer", "streamer", "youtuber", "artist", "developer", "designer", "writer", "chef", "mechanic", "pilot", "teacher", "doctor", "engineer", "scientist", "architect", "photographer", "musician", "actor", "athlete", "chef"]
    earnings = random.randint(10, 50)
    data = get_user(str(interaction.user.id))
    data['balance'] += earnings
    await interaction.response.send_message(f"💼 You worked as **{random.choice(jobs)}** and earned **{earnings}** coins")

@tree.command(name="shop", description="View shop")
async def shop(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    embed = discord.Embed(title="🛍️ Shop", color=discord.Color.gold())
    for item, price in shop_items.items():
        embed.add_field(name=item, value=f"{price} coins", inline=True)
    embed.set_footer(text="Use /buy <item> to purchase")
    await interaction.response.send_message(embed=embed)

@tree.command(name="buy", description="Buy an item")
async def buy(interaction: discord.Interaction, item: str):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if item.lower() not in [i.lower() for i in shop_items.keys()]:
        await interaction.response.send_message("❌ Not in shop", ephemeral=True)
        return
    data = get_user(str(interaction.user.id))
    actual_item = next(i for i in shop_items.keys() if i.lower() == item.lower())
    price = shop_items[actual_item]
    if data['balance'] < price:
        await interaction.response.send_message(f"❌ Need {price} coins", ephemeral=True)
        return
    data['balance'] -= price
    data['inventory'].append(actual_item)
    await interaction.response.send_message(f"✅ Bought **{actual_item}** for {price} coins")

@tree.command(name="inventory", description="View inventory")
async def inventory(interaction: discord.Interaction, member: discord.Member = None):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if member is None:
        member = interaction.user
    data = get_user(str(member.id))
    if not data['inventory']:
        await interaction.response.send_message(f"📦 {member.mention} has nothing")
        return
    await interaction.response.send_message(f"📦 **{member.name}'s inventory:**\n" + "\n".join(f"• {i}" for i in data['inventory']))

@tree.command(name="gamble", description="Gamble your coins")
async def gamble(interaction: discord.Interaction, amount: int):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if amount < 1:
        await interaction.response.send_message("❌ Must be at least 1", ephemeral=True)
        return
    data = get_user(str(interaction.user.id))
    if data['balance'] < amount:
        await interaction.response.send_message("❌ Not enough coins", ephemeral=True)
        return
    multiplier = random.choice([0, 0, 0, 0.5, 1, 1.5, 2, 3, 5, 10])
    if multiplier == 0:
        data['balance'] -= amount
        await interaction.response.send_message(f"😔 Lost {amount} coins")
    else:
        winnings = int(amount * multiplier)
        data['balance'] += winnings
        if multiplier >= 5:
            await interaction.response.send_message(f"🎉 JACKPOT! Won {winnings} coins ({multiplier}x)")
        else:
            await interaction.response.send_message(f"🎉 Won {winnings} coins ({multiplier}x)")

@tree.command(name="steal", description="Steal from another user")
async def steal(interaction: discord.Interaction, target: discord.Member):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if target == interaction.user:
        await interaction.response.send_message("❌ Can't steal from yourself", ephemeral=True)
        return
    if target.bot:
        await interaction.response.send_message("❌ Can't steal from a bot", ephemeral=True)
        return
    target_data = get_user(str(target.id))
    if target_data['balance'] < 10:
        await interaction.response.send_message(f"❌ {target.mention} is too poor", ephemeral=True)
        return
    user_data = get_user(str(interaction.user.id))
    if random.random() < 0.4:
        amount = random.randint(1, min(50, target_data['balance']))
        target_data['balance'] -= amount
        user_data['balance'] += amount
        await interaction.response.send_message(f"💰 You stole **{amount}** coins from {target.mention} 😈")
    else:
        penalty = random.randint(5, 20)
        user_data['balance'] = max(0, user_data['balance'] - penalty)
        await interaction.response.send_message(f"❌ You got caught! Paid **{penalty}** coins fine")

@tree.command(name="give", description="Give coins to someone")
async def give(interaction: discord.Interaction, target: discord.Member, amount: int):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if target == interaction.user:
        await interaction.response.send_message("❌ Can't give to yourself", ephemeral=True)
        return
    if amount < 1:
        await interaction.response.send_message("❌ Amount must be positive", ephemeral=True)
        return
    user_data = get_user(str(interaction.user.id))
    if user_data['balance'] < amount:
        await interaction.response.send_message("❌ Not enough coins", ephemeral=True)
        return
    target_data = get_user(str(target.id))
    user_data['balance'] -= amount
    target_data['balance'] += amount
    await interaction.response.send_message(f"✅ Gave **{amount}** coins to {target.mention}")

@tree.command(name="donate", description="Donate coins to the server")
async def donate(interaction: discord.Interaction, amount: int):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if amount < 1:
        await interaction.response.send_message("❌ Amount must be positive", ephemeral=True)
        return
    data = get_user(str(interaction.user.id))
    if data['balance'] < amount:
        await interaction.response.send_message("❌ Not enough coins", ephemeral=True)
        return
    data['balance'] -= amount
    await interaction.response.send_message(f"🎁 You donated **{amount}** coins to the server! Thank you! 🙏")

@tree.command(name="transfer", description="Transfer coins between users")
async def transfer(interaction: discord.Interaction, target: discord.Member, amount: int):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    await give(interaction, target, amount)

# ==================== MODERATION COMMANDS ====================
@tree.command(name="kick", description="Kick a member")
@app_commands.default_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    if not (is_mod(interaction) or is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need MOD role or higher!", ephemeral=True)
        return
    if member == interaction.user:
        await interaction.response.send_message("❌ Can't kick yourself", ephemeral=True)
        return
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👢 Kicked {member.mention}\nReason: {reason}")

@tree.command(name="ban", description="Ban a member")
@app_commands.default_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    if not (is_mod(interaction) or is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need MOD role or higher!", ephemeral=True)
        return
    if member == interaction.user:
        await interaction.response.send_message("❌ Can't ban yourself", ephemeral=True)
        return
    await member.ban(reason=reason)
    await interaction.response.send_message(f"🔨 Banned {member.mention}\nReason: {reason}")

@tree.command(name="clear", description="Clear messages")
@app_commands.default_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    if not (is_mod(interaction) or is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need MOD role or higher!", ephemeral=True)
        return
    if amount < 1 or amount > 100:
        await interaction.response.send_message("❌ 1-100 only", ephemeral=True)
        return
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"🗑️ Deleted {len(deleted)} messages", ephemeral=True)

@tree.command(name="timeout", description="Timeout a member")
@app_commands.default_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "No reason"):
    if not (is_mod(interaction) or is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need MOD role or higher!", ephemeral=True)
        return
    if minutes < 1 or minutes > 40320:
        await interaction.response.send_message("❌ 1-40320 minutes", ephemeral=True)
        return
    await member.timeout(datetime.timedelta(minutes=minutes), reason=reason)
    await interaction.response.send_message(f"⏰ {member.mention} timed out for {minutes} minutes")

@tree.command(name="warn", description="Warn a member")
@app_commands.default_permissions(kick_members=True)
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str):
    if not (is_mod(interaction) or is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need MOD role or higher!", ephemeral=True)
        return
    user_id = str(member.id)
    if user_id not in warnings:
        warnings[user_id] = []
    warnings[user_id].append({"reason": reason, "mod": str(interaction.user), "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
    await interaction.response.send_message(f"⚠️ {member.mention} warned\nReason: {reason}\nTotal warnings: {len(warnings[user_id])}")

@tree.command(name="warnings", description="Check warnings")
@app_commands.default_permissions(kick_members=True)
async def warnings_cmd(interaction: discord.Interaction, member: discord.Member):
    if not (is_mod(interaction) or is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need MOD role or higher!", ephemeral=True)
        return
    user_id = str(member.id)
    if user_id not in warnings or not warnings[user_id]:
        await interaction.response.send_message(f"✅ {member.mention} has no warnings")
        return
    embed = discord.Embed(title=f"⚠️ Warnings for {member.name}", color=discord.Color.orange())
    for i, w in enumerate(warnings[user_id][:10], 1):
        embed.add_field(name=f"#{i}", value=f"Reason: {w['reason']}\nMod: {w['mod']}\nTime: {w['time']}", inline=False)
    embed.set_footer(text=f"Total: {len(warnings[user_id])} warnings")
    await interaction.response.send_message(embed=embed)

@tree.command(name="removewarn", description="Remove a warning")
@app_commands.default_permissions(kick_members=True)
async def removewarn(interaction: discord.Interaction, member: discord.Member, number: int):
    if not (is_mod(interaction) or is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need MOD role or higher!", ephemeral=True)
        return
    user_id = str(member.id)
    if user_id not in warnings or number > len(warnings[user_id]) or number < 1:
        await interaction.response.send_message("❌ Warning not found", ephemeral=True)
        return
    removed = warnings[user_id].pop(number-1)
    await interaction.response.send_message(f"✅ Removed warning #{number} for {member.mention} (Reason: {removed['reason']})")

@tree.command(name="slowmode", description="Set slowmode")
@app_commands.default_permissions(manage_channels=True)
async def slowmode(interaction: discord.Interaction, seconds: int):
    if not (is_mod(interaction) or is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need MOD role or higher!", ephemeral=True)
        return
    if seconds < 0 or seconds > 21600:
        await interaction.response.send_message("❌ 0-21600 seconds", ephemeral=True)
        return
    await interaction.channel.edit(slowmode_delay=seconds)
    await interaction.response.send_message(f"✅ Slowmode set to {seconds}s" if seconds else "✅ Slowmode disabled")

@tree.command(name="lock", description="Lock channel")
@app_commands.default_permissions(manage_channels=True)
async def lock(interaction: discord.Interaction, channel: discord.TextChannel = None):
    if not (is_mod(interaction) or is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need MOD role or higher!", ephemeral=True)
        return
    if channel is None:
        channel = interaction.channel
    await channel.set_permissions(interaction.guild.default_role, send_messages=False)
    await interaction.response.send_message(f"🔒 #{channel.name} locked")

@tree.command(name="unlock", description="Unlock channel")
@app_commands.default_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction, channel: discord.TextChannel = None):
    if not (is_mod(interaction) or is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need MOD role or higher!", ephemeral=True)
        return
    if channel is None:
        channel = interaction.channel
    await channel.set_permissions(interaction.guild.default_role, send_messages=True)
    await interaction.response.send_message(f"🔓 #{channel.name} unlocked")

@tree.command(name="poll", description="Create a poll")
@app_commands.default_permissions(manage_messages=True)
async def poll(interaction: discord.Interaction, question: str, option1: str, option2: str, option3: str = None, option4: str = None):
    if not (is_mod(interaction) or is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need MOD role or higher!", ephemeral=True)
        return
    options = [o for o in [option1, option2, option3, option4] if o]
    if len(options) < 2:
        await interaction.response.send_message("❌ Need at least 2 options", ephemeral=True)
        return
    embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.blue())
    for i, opt in enumerate(options, 1):
        embed.add_field(name=f"Option {i}", value=opt, inline=True)
    msg = await interaction.response.send_message(embed=embed)
    for i in range(1, len(options)+1):
        await msg.add_reaction(f"{i}️⃣")

@tree.command(name="announce", description="Announce something in current server")
@app_commands.default_permissions(administrator=True)
async def announce(interaction: discord.Interaction, message: str):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF or FOUNDER role!", ephemeral=True)
        return
    embed = discord.Embed(title="📢 Announcement", description=message, color=discord.Color.gold())
    embed.set_footer(text=f"Announced by {interaction.user.name}")
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("✅ Announcement sent!", ephemeral=True)

# ==================== LEVELING ====================
@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return
    user_id = str(message.author.id)
    if user_id not in levels:
        levels[user_id] = 0
    levels[user_id] += random.randint(5, 15)
    # Achievement for leveling
    if levels[user_id] >= 1000:
        add_achievement(user_id, "Level 1000+")

@tree.command(name="level", description="Check your level")
async def level(interaction: discord.Interaction, member: discord.Member = None):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if member is None:
        member = interaction.user
    exp = levels.get(str(member.id), 0)
    lvl = int((exp ** 0.5) / 2) + 1
    next_exp = ((lvl + 1) * 2) ** 2
    progress = exp - ((lvl * 2) ** 2)
    needed = next_exp - ((lvl * 2) ** 2)
    embed = discord.Embed(title=f"📊 {member.name}", color=discord.Color.blue())
    embed.add_field(name="Level", value=lvl, inline=True)
    embed.add_field(name="EXP", value=f"{exp} / {next_exp}", inline=True)
    embed.add_field(name="Progress", value=f"{int(progress/needed*100)}%", inline=True)
    await interaction.response.send_message(embed=embed)

@tree.command(name="leaderboard", description="Top 10 levels")
async def leaderboard(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if not levels:
        await interaction.response.send_message("❌ No data")
        return
    sorted_users = sorted(levels.items(), key=lambda x: x[1], reverse=True)[:10]
    embed = discord.Embed(title="🏆 Leaderboard", color=discord.Color.gold())
    for i, (uid, exp) in enumerate(sorted_users, 1):
        member = bot.get_user(int(uid))
        name = member.name if member else "Unknown"
        lvl = int((exp ** 0.5) / 2) + 1
        embed.add_field(name=f"#{i} {name}", value=f"Level {lvl} | {exp} EXP", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="rank", description="Your rank")
async def rank(interaction: discord.Interaction, member: discord.Member = None):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if member is None:
        member = interaction.user
    uid = str(member.id)
    if uid not in levels:
        await interaction.response.send_message(f"{member.mention} has no rank")
        return
    sorted_users = sorted(levels.items(), key=lambda x: x[1], reverse=True)
    rank_num = next((i for i, (u, _) in enumerate(sorted_users, 1) if u == uid), None)
    await interaction.response.send_message(f"🏆 {member.mention} is rank **#{rank_num}** out of {len(sorted_users)}")

# ==================== ADMIN COMMANDS ====================
@tree.command(name="rename", description="[Admin] Rename a channel")
@app_commands.default_permissions(manage_channels=True)
async def rename(interaction: discord.Interaction, channel: discord.TextChannel, new_name: str):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF or FOUNDER role!", ephemeral=True)
        return
    old_name = channel.name
    await channel.edit(name=new_name)
    await interaction.response.send_message(f"✅ Renamed #{old_name} to #{new_name}")

@tree.command(name="createchannel", description="[Admin] Create a new channel")
@app_commands.default_permissions(manage_channels=True)
async def createchannel(interaction: discord.Interaction, name: str, channel_type: str = "text", category: discord.CategoryChannel = None):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF or FOUNDER role!", ephemeral=True)
        return
    
    guild = interaction.guild
    if channel_type.lower() == "text":
        channel = await guild.create_text_channel(name, category=category)
    elif channel_type.lower() == "voice":
        channel = await guild.create_voice_channel(name, category=category)
    else:
        await interaction.response.send_message("❌ Invalid channel type! Use 'text' or 'voice'", ephemeral=True)
        return
    
    await interaction.response.send_message(f"✅ Created {channel_type} channel #{channel.name}")

@tree.command(name="deletechannel", description="[Admin] Delete a channel")
@app_commands.default_permissions(manage_channels=True)
async def deletechannel(interaction: discord.Interaction, channel: discord.TextChannel):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF or FOUNDER role!", ephemeral=True)
        return
    channel_name = channel.name
    await channel.delete()
    await interaction.response.send_message(f"✅ Deleted channel #{channel_name}")

@tree.command(name="addrole", description="[Admin] Add a role to a member")
@app_commands.default_permissions(manage_roles=True)
async def addrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if not (is_mod(interaction) or is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need MOD role or higher!", ephemeral=True)
        return
    if role in member.roles:
        await interaction.response.send_message(f"❌ {member.mention} already has {role.name}", ephemeral=True)
        return
    await member.add_roles(role)
    await interaction.response.send_message(f"✅ Added {role.name} to {member.mention}")

@tree.command(name="removerole", description="[Admin] Remove a role from a member")
@app_commands.default_permissions(manage_roles=True)
async def removerole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if not (is_mod(interaction) or is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need MOD role or higher!", ephemeral=True)
        return
    if role not in member.roles:
        await interaction.response.send_message(f"❌ {member.mention} doesn't have {role.name}", ephemeral=True)
        return
    await member.remove_roles(role)
    await interaction.response.send_message(f"✅ Removed {role.name} from {member.mention}")

@tree.command(name="createrole", description="[Admin] Create a new role")
@app_commands.default_permissions(manage_roles=True)
async def createrole(interaction: discord.Interaction, name: str, color: str = None):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF or FOUNDER role!", ephemeral=True)
        return
    
    guild = interaction.guild
    color_int = discord.Color.default()
    if color:
        try:
            color_int = int(color.replace("#", ""), 16)
        except:
            pass
    
    role = await guild.create_role(name=name, color=color_int)
    await interaction.response.send_message(f"✅ Created role: {role.mention}")

@tree.command(name="deleterole", description="[Admin] Delete a role")
@app_commands.default_permissions(manage_roles=True)
async def deleterole(interaction: discord.Interaction, role: discord.Role):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF or FOUNDER role!", ephemeral=True)
        return
    role_name = role.name
    await role.delete()
    await interaction.response.send_message(f"✅ Deleted role: {role_name}")

@tree.command(name="settopic", description="[Admin] Set channel topic")
@app_commands.default_permissions(manage_channels=True)
async def settopic(interaction: discord.Interaction, channel: discord.TextChannel, topic: str):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF or FOUNDER role!", ephemeral=True)
        return
    await channel.edit(topic=topic)
    await interaction.response.send_message(f"✅ Set topic for #{channel.name}")

@tree.command(name="clonechannel", description="[Admin] Clone a channel")
@app_commands.default_permissions(manage_channels=True)
async def clonechannel(interaction: discord.Interaction, channel: discord.TextChannel):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF or FOUNDER role!", ephemeral=True)
        return
    new_channel = await channel.clone()
    await interaction.response.send_message(f"✅ Cloned #{channel.name} to #{new_channel.name}")

@tree.command(name="movechannel", description="[Admin] Move channel to a category")
@app_commands.default_permissions(manage_channels=True)
async def movechannel(interaction: discord.Interaction, channel: discord.TextChannel, category: discord.CategoryChannel):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF or FOUNDER role!", ephemeral=True)
        return
    await channel.edit(category=category)
    await interaction.response.send_message(f"✅ Moved #{channel.name} to {category.name}")

@tree.command(name="addroleall", description="[Owner] Add a role to all members")
@app_commands.default_permissions(administrator=True)
async def addroleall(interaction: discord.Interaction, role: discord.Role):
    if not is_founder(interaction) and not is_staff(interaction):
        await interaction.response.send_message("❌ You need FOUNDER or STAFF role!", ephemeral=True)
        return
    
    await interaction.response.send_message(f"⏳ Adding {role.name} to all members...", ephemeral=True)
    
    count = 0
    for member in interaction.guild.members:
        if not member.bot and role not in member.roles:
            try:
                await member.add_roles(role)
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
    
    await interaction.edit_original_response(content=f"✅ Added {role.name} to {count} members!")

@tree.command(name="removeroleall", description="[Owner] Remove a role from all members")
@app_commands.default_permissions(administrator=True)
async def removeroleall(interaction: discord.Interaction, role: discord.Role):
    if not is_founder(interaction) and not is_staff(interaction):
        await interaction.response.send_message("❌ You need FOUNDER or STAFF role!", ephemeral=True)
        return
    
    await interaction.response.send_message(f"⏳ Removing {role.name} from all members...", ephemeral=True)
    
    count = 0
    for member in interaction.guild.members:
        if role in member.roles:
            try:
                await member.remove_roles(role)
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
    
    await interaction.edit_original_response(content=f"✅ Removed {role.name} from {count} members!")

@tree.command(name="lockall", description="[Owner] Lock all channels")
@app_commands.default_permissions(administrator=True)
async def lockall(interaction: discord.Interaction):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    await interaction.response.send_message("🔒 Locking all channels...", ephemeral=True)
    count = 0
    for channel in interaction.guild.channels:
        if isinstance(channel, discord.TextChannel):
            try:
                await channel.set_permissions(interaction.guild.default_role, send_messages=False)
                count += 1
                await asyncio.sleep(0.2)
            except:
                pass
    await interaction.edit_original_response(content=f"✅ Locked {count} channels!")

@tree.command(name="unlockall", description="[Owner] Unlock all channels")
@app_commands.default_permissions(administrator=True)
async def unlockall(interaction: discord.Interaction):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    await interaction.response.send_message("🔓 Unlocking all channels...", ephemeral=True)
    count = 0
    for channel in interaction.guild.channels:
        if isinstance(channel, discord.TextChannel):
            try:
                await channel.set_permissions(interaction.guild.default_role, send_messages=True)
                count += 1
                await asyncio.sleep(0.2)
            except:
                pass
    await interaction.edit_original_response(content=f"✅ Unlocked {count} channels!")

@tree.command(name="massban", description="[Owner] Ban multiple members")
@app_commands.default_permissions(administrator=True)
async def massban(interaction: discord.Interaction, members: str, reason: str = "No reason"):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    member_ids = members.split()
    count = 0
    await interaction.response.send_message(f"⏳ Banning {len(member_ids)} members...", ephemeral=True)
    
    for member_id in member_ids:
        try:
            member = interaction.guild.get_member(int(member_id))
            if member:
                await member.ban(reason=reason)
                count += 1
                await asyncio.sleep(0.5)
        except:
            pass
    
    await interaction.edit_original_response(content=f"✅ Banned {count} members!")

@tree.command(name="masskick", description="[Owner] Kick multiple members")
@app_commands.default_permissions(administrator=True)
async def masskick(interaction: discord.Interaction, members: str, reason: str = "No reason"):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    member_ids = members.split()
    count = 0
    await interaction.response.send_message(f"⏳ Kicking {len(member_ids)} members...", ephemeral=True)
    
    for member_id in member_ids:
        try:
            member = interaction.guild.get_member(int(member_id))
            if member:
                await member.kick(reason=reason)
                count += 1
                await asyncio.sleep(0.5)
        except:
            pass
    
    await interaction.edit_original_response(content=f"✅ Kicked {count} members!")

@tree.command(name="masspurge", description="[Owner] Purge messages from multiple users")
@app_commands.default_permissions(administrator=True)
async def masspurge(interaction: discord.Interaction, members: str, amount: int = 10):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    member_ids = members.split()
    count = 0
    await interaction.response.send_message(f"⏳ Purging messages...", ephemeral=True)
    
    for member_id in member_ids:
        try:
            member = interaction.guild.get_member(int(member_id))
            if member:
                def check(msg):
                    return msg.author == member
                deleted = await interaction.channel.purge(limit=amount, check=check)
                count += len(deleted)
                await asyncio.sleep(0.5)
        except:
            pass
    
    await interaction.edit_original_response(content=f"✅ Purged {count} messages from {len(member_ids)} users!")

@tree.command(name="purgebots", description="[Owner] Purge all bot messages")
@app_commands.default_permissions(administrator=True)
async def purgebots(interaction: discord.Interaction, amount: int = 100):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    def check(msg):
        return msg.author.bot
    
    deleted = await interaction.channel.purge(limit=amount, check=check)
    await interaction.response.send_message(f"✅ Deleted {len(deleted)} bot messages", ephemeral=True)

@tree.command(name="purgehumans", description="[Owner] Purge all human messages")
@app_commands.default_permissions(administrator=True)
async def purgehumans(interaction: discord.Interaction, amount: int = 100):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    def check(msg):
        return not msg.author.bot
    
    deleted = await interaction.channel.purge(limit=amount, check=check)
    await interaction.response.send_message(f"✅ Deleted {len(deleted)} human messages", ephemeral=True)

# ==================== OWNER COMMANDS ====================
@tree.command(name="serverlist", description="[Owner] List all servers the bot is in")
async def serverlist(interaction: discord.Interaction):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    server_list = ""
    for i, guild in enumerate(bot.guilds, 1):
        server_list += f"{i}. {guild.name} ({guild.id}) - {guild.member_count} members\n"
        if len(server_list) > 1800:
            break
    
    embed = discord.Embed(title=f"📊 Servers ({len(bot.guilds)})", color=discord.Color.blue())
    embed.add_field(name="Servers", value=server_list or "No servers", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="leaveserver", description="[Owner] Make the bot leave a server")
async def leaveserver(interaction: discord.Interaction, server_id: str):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    guild = bot.get_guild(int(server_id))
    if guild:
        await guild.leave()
        await interaction.response.send_message(f"✅ Left server: {guild.name}")
    else:
        await interaction.response.send_message("❌ Server not found or bot not in it")

@tree.command(name="broadcast", description="[Owner] Send a message to all servers")
async def broadcast(interaction: discord.Interaction, message: str):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    sent = 0
    for guild in bot.guilds:
        try:
            channel = guild.system_channel or guild.text_channels[0]
            await channel.send(f"📢 **Announcement from Owner:**\n{message}")
            sent += 1
            await asyncio.sleep(0.5)
        except:
            pass
    
    await interaction.response.send_message(f"✅ Broadcast sent to {sent} servers!")

@tree.command(name="exportdata", description="[Owner] Export all bot data")
async def exportdata(interaction: discord.Interaction):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    data = {
        "economy": economy,
        "levels": levels,
        "warnings": warnings,
        "marriage": marriage,
        "pets": pets,
        "inventory": inventory,
        "achievements": achievements,
        "blacklist": blacklist
    }
    
    with open("bot_data.json", "w") as f:
        json.dump(data, f, indent=4)
    
    await interaction.response.send_message("✅ Data exported!", ephemeral=True)

@tree.command(name="importdata", description="[Owner] Import bot data from JSON")
async def importdata(interaction: discord.Interaction):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    try:
        with open("bot_data.json", "r") as f:
            data = json.load(f)
        
        economy.update(data.get("economy", {}))
        levels.update(data.get("levels", {}))
        warnings.update(data.get("warnings", {}))
        marriage.update(data.get("marriage", {}))
        pets.update(data.get("pets", {}))
        inventory.update(data.get("inventory", {}))
        achievements.update(data.get("achievements", {}))
        blacklist.update(data.get("blacklist", {}))
        
        await interaction.response.send_message("✅ Data imported successfully!", ephemeral=True)
    except:
        await interaction.response.send_message("❌ No data file found or invalid format!", ephemeral=True)

@tree.command(name="cleareconomy", description="[Owner] Clear all economy data")
async def cleareconomy(interaction: discord.Interaction):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    economy.clear()
    await interaction.response.send_message("✅ Economy data cleared!")

@tree.command(name="clearlevels", description="[Owner] Clear all leveling data")
async def clearlevels(interaction: discord.Interaction):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    levels.clear()
    await interaction.response.send_message("✅ Leveling data cleared!")

@tree.command(name="cleardata", description="[Owner] Clear all data")
async def cleardata(interaction: discord.Interaction):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    economy.clear()
    levels.clear()
    warnings.clear()
    achievements.clear()
    await interaction.response.send_message("✅ All data cleared!")

@tree.command(name="backup", description="[Owner] Create a backup of all data")
async def backup(interaction: discord.Interaction):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    data = {
        "economy": economy,
        "levels": levels,
        "warnings": warnings,
        "achievements": achievements,
        "blacklist": blacklist,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    filename = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    
    await interaction.response.send_message(f"✅ Backup created: {filename}", ephemeral=True)

@tree.command(name="restore", description="[Owner] Restore from backup")
async def restore(interaction: discord.Interaction, filename: str):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        
        economy.update(data.get("economy", {}))
        levels.update(data.get("levels", {}))
        warnings.update(data.get("warnings", {}))
        achievements.update(data.get("achievements", {}))
        blacklist.update(data.get("blacklist", {}))
        
        await interaction.response.send_message(f"✅ Restored from {filename}!", ephemeral=True)
    except:
        await interaction.response.send_message("❌ File not found or invalid!", ephemeral=True)

@tree.command(name="blacklistuser", description="[Owner] Blacklist a user from using the bot")
async def blacklistuser(interaction: discord.Interaction, user: discord.User):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    if str(user.id) not in blacklist:
        blacklist[str(user.id)] = {"name": user.name, "reason": "No reason given", "date": datetime.datetime.now().isoformat()}
        save_json("blacklist.json", blacklist)
        await interaction.response.send_message(f"✅ {user.mention} has been blacklisted!")
    else:
        await interaction.response.send_message("❌ User is already blacklisted!")

@tree.command(name="unblacklistuser", description="[Owner] Remove a user from the blacklist")
async def unblacklistuser(interaction: discord.Interaction, user: discord.User):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    if str(user.id) in blacklist:
        del blacklist[str(user.id)]
        save_json("blacklist.json", blacklist)
        await interaction.response.send_message(f"✅ {user.mention} has been unblacklisted!")
    else:
        await interaction.response.send_message("❌ User is not blacklisted!")

@tree.command(name="giveaway", description="[Staff] Start a giveaway")
@app_commands.default_permissions(administrator=True)
async def giveaway(interaction: discord.Interaction, prize: str, duration: int, winners: int = 1):
    if not is_founder(interaction) and not is_staff(interaction):
        await interaction.response.send_message("❌ You need FOUNDER or STAFF role!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🎉 GIVEAWAY! 🎉",
        description=f"**Prize:** {prize}\n**Winners:** {winners}\n**Duration:** {duration} minutes",
        color=discord.Color.gold()
    )
    embed.set_footer(text="React with 🎉 to enter!")
    
    msg = await interaction.channel.send(embed=embed)
    await msg.add_reaction("🎉")
    await interaction.response.send_message("✅ Giveaway started!", ephemeral=True)
    
    await asyncio.sleep(duration * 60)
    
    msg = await interaction.channel.fetch_message(msg.id)
    reaction = discord.utils.get(msg.reactions, emoji="🎉")
    users = [user async for user in reaction.users() if not user.bot]
    winners_list = random.sample(users, min(winners, len(users)))
    
    if winners_list:
        await interaction.channel.send(f"🎉 **Giveaway Ended!**\n**Winner(s):** {', '.join(w.mention for w in winners_list)}\n**Prize:** {prize}")
    else:
        await interaction.channel.send("❌ No one entered the giveaway!")

@tree.command(name="endgiveaway", description="[Staff] End a giveaway early")
@app_commands.default_permissions(administrator=True)
async def endgiveaway(interaction: discord.Interaction):
    if not is_founder(interaction) and not is_staff(interaction):
        await interaction.response.send_message("❌ You need FOUNDER or STAFF role!", ephemeral=True)
        return
    
    await interaction.response.send_message("✅ Giveaway ended by staff!", ephemeral=True)

@tree.command(name="setbalance", description="[Admin] Set a user's balance")
async def setbalance(interaction: discord.Interaction, member: discord.Member, amount: int):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF role or higher!", ephemeral=True)
        return
    data = get_user(str(member.id))
    data['balance'] = amount
    await interaction.response.send_message(f"✅ {member.mention}'s balance set to {amount} coins")

@tree.command(name="addcoins", description="[Admin] Add coins to a user")
async def addcoins(interaction: discord.Interaction, member: discord.Member, amount: int):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF role or higher!", ephemeral=True)
        return
    data = get_user(str(member.id))
    data['balance'] += amount
    await interaction.response.send_message(f"✅ Added {amount} coins to {member.mention}. New balance: {data['balance']}")

@tree.command(name="removecoins", description="[Admin] Remove coins from a user")
async def removecoins(interaction: discord.Interaction, member: discord.Member, amount: int):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF role or higher!", ephemeral=True)
        return
    data = get_user(str(member.id))
    data['balance'] = max(0, data['balance'] - amount)
    await interaction.response.send_message(f"✅ Removed {amount} coins from {member.mention}. New balance: {data['balance']}")

@tree.command(name="resetbalance", description="[Admin] Reset a user's balance to 100")
async def resetbalance(interaction: discord.Interaction, member: discord.Member):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF role or higher!", ephemeral=True)
        return
    data = get_user(str(member.id))
    data['balance'] = 100
    await interaction.response.send_message(f"✅ {member.mention}'s balance reset to 100 coins")

@tree.command(name="resetwarnings", description="[Admin] Clear all warnings for a user")
async def resetwarnings(interaction: discord.Interaction, member: discord.Member):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF role or higher!", ephemeral=True)
        return
    uid = str(member.id)
    if uid in warnings:
        warnings[uid] = []
    await interaction.response.send_message(f"✅ All warnings removed for {member.mention}")

@tree.command(name="addxp", description="[Admin] Add XP to a user")
async def addxp(interaction: discord.Interaction, member: discord.Member, amount: int):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF role or higher!", ephemeral=True)
        return
    uid = str(member.id)
    if uid not in levels:
        levels[uid] = 0
    levels[uid] += amount
    await interaction.response.send_message(f"✅ Added {amount} XP to {member.mention}")

@tree.command(name="setlevel", description="[Admin] Set a user's level")
async def setlevel(interaction: discord.Interaction, member: discord.Member, level: int):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF role or higher!", ephemeral=True)
        return
    uid = str(member.id)
    levels[uid] = (level * 2) ** 2
    await interaction.response.send_message(f"✅ Set {member.mention}'s level to {level}")

@tree.command(name="removexp", description="[Admin] Remove XP from a user")
async def removexp(interaction: discord.Interaction, member: discord.Member, amount: int):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF role or higher!", ephemeral=True)
        return
    uid = str(member.id)
    if uid not in levels:
        levels[uid] = 0
    levels[uid] = max(0, levels[uid] - amount)
    await interaction.response.send_message(f"✅ Removed {amount} XP from {member.mention}")

@tree.command(name="resetlevels", description="[Admin] Reset all leveling data")
async def resetlevels(interaction: discord.Interaction):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF role or higher!", ephemeral=True)
        return
    levels.clear()
    await interaction.response.send_message("✅ All level data reset!")

# ==================== UTILITY COMMANDS ====================
@tree.command(name="time", description="Current time")
async def time(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    now = datetime.datetime.now()
    await interaction.response.send_message(f"🕐 {now.strftime('%I:%M:%S %p')}")

@tree.command(name="date", description="Current date")
async def date(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    now = datetime.datetime.now()
    await interaction.response.send_message(f"📅 {now.strftime('%B %d, %Y')}")

@tree.command(name="avatar", description="User avatar")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    if member is None:
        member = interaction.user
    embed = discord.Embed(title=f"🖼️ {member.name}", color=member.color)
    embed.set_image(url=member.avatar.url if member.avatar else member.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@tree.command(name="invite", description="Bot invite link")
async def invite(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    url = f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot%20applications.commands"
    await interaction.response.send_message(f"📩 [Invite me]({url})")

@tree.command(name="weather", description="Weather for a city")
async def weather(interaction: discord.Interaction, city: str):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    try:
        resp = requests.get(f"https://wttr.in/{city}?format=%C+%t+%w")
        if resp.status_code == 200:
            await interaction.response.send_message(f"🌤️ **{city}**: {resp.text}")
        else:
            await interaction.response.send_message("❌ Could not fetch weather")
    except:
        await interaction.response.send_message("❌ API error")

@tree.command(name="translate", description="Translate text")
async def translate(interaction: discord.Interaction, text: str, language: str = "en"):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={language}&dt=t&q={text}"
        resp = requests.get(url)
        if resp.status_code == 200:
            translated = resp.json()[0][0][0]
            await interaction.response.send_message(f"🌐 **Translation**: {translated}")
        else:
            await interaction.response.send_message("❌ Translation failed")
    except:
        await interaction.response.send_message("❌ API error")

@tree.command(name="calculate", description="Calculate an expression")
async def calculate(interaction: discord.Interaction, expression: str):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    allowed = re.compile(r'^[\d+\-*/.() ]+$')
    if not allowed.match(expression):
        await interaction.response.send_message("❌ Invalid expression", ephemeral=True)
        return
    try:
        result = eval(expression)
        await interaction.response.send_message(f"🧮 `{expression} = {result}`")
    except:
        await interaction.response.send_message("❌ Error evaluating", ephemeral=True)

@tree.command(name="timestamp", description="Get timestamp for a date")
async def timestamp(interaction: discord.Interaction, date: str):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    try:
        dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        ts = int(dt.timestamp())
        await interaction.response.send_message(f"📅 Timestamp: `{ts}`\n<t:{ts}:F>")
    except:
        await interaction.response.send_message("❌ Invalid date format! Use: YYYY-MM-DD HH:MM", ephemeral=True)

@tree.command(name="countdown", description="Countdown to a date")
async def countdown(interaction: discord.Interaction, date: str):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    try:
        target = datetime.datetime.strptime(date, "%Y-%m-%d")
        now = datetime.datetime.now()
        diff = target - now
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await interaction.response.send_message(f"⏱️ Countdown to {date}: **{days}d {hours}h {minutes}m {seconds}s**")
    except:
        await interaction.response.send_message("❌ Invalid date! Use: YYYY-MM-DD", ephemeral=True)

# ==================== ERROR HANDLING ====================
@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
    elif isinstance(error, app_commands.CommandNotFound):
        await interaction.response.send_message("❌ Command not found.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Error: {str(error)[:100]}", ephemeral=True)
        print(error)

# ==================== WEB SERVER ====================
app = Flask('')
@app.route('/')
def home():
    return "I'm alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_web, daemon=True).start()

# ==================== RUN ====================
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("❌ DISCORD_TOKEN not found in Secrets!")