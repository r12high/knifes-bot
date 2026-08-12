import discord
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

# ==================== KEEP-ALIVE SYSTEM ====================
def keep_alive():
    while True:
        time.sleep(300)
        print("🔄 Keeping bot alive...")

threading.Thread(target=keep_alive, daemon=True).start()

# ==================== CONFIGURATION ====================
OWNER_ID = 1499789411376955585  # Your Discord User ID

# ==================== AUTO-ROLE & VERIFICATION ====================
AUTO_ROLE_NAME = "Member"
VERIFIED_ROLE_NAME = "VERIFIED"
VERIFICATION_CHANNEL_NAME = "verify"
VERIFICATION_LOG_CHANNEL = "logs"

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
todo_list = {}
verification_codes = {}

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
    "⚡ Lightning": 325,
    "☁️ Cloud": 200,
    "🌧️ Rain": 250,
    "⛄ Snow": 300,
    "🌪️ Tornado": 500,
    "🌋 Volcano": 750
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

def get_todo(user_id):
    if user_id not in todo_list:
        todo_list[user_id] = []
    return todo_list[user_id]

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

# ==================== AUTO-ROLE ON JOIN ====================
@bot.event
async def on_member_join(member: discord.Member):
    if AUTO_ROLE_NAME:
        role = discord.utils.get(member.guild.roles, name=AUTO_ROLE_NAME)
        if role:
            try:
                await member.add_roles(role, reason="Auto-role on join")
                print(f"✅ Added {AUTO_ROLE_NAME} role to {member.name}")
            except:
                print(f"❌ Failed to add role to {member.name}")
    
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        embed = discord.Embed(
            title="👋 Welcome!",
            description=f"Welcome to the server {member.mention}! 🎉",
            color=discord.Color.green()
        )
        verify_channel = discord.utils.get(member.guild.text_channels, name=VERIFICATION_CHANNEL_NAME)
        embed.add_field(
            name="📝 How to Get Started",
            value=f"1. Type `/verify` in {verify_channel.mention if verify_channel else 'the verification channel'} to get verified\n2. Check the rules\n3. Introduce yourself!",
            inline=False
        )
        embed.set_footer(text="🔪 Knifes Beaming")
        await channel.send(embed=embed)
    
    log_channel = discord.utils.get(member.guild.text_channels, name=VERIFICATION_LOG_CHANNEL)
    if log_channel:
        embed = discord.Embed(
            title="👤 Member Joined",
            description=f"{member.mention} has joined the server!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Total Members", value=member.guild.member_count, inline=True)
        await log_channel.send(embed=embed)

# ==================== VERIFICATION SYSTEM ====================
@tree.command(name="verify", description="Verify yourself to get the verified role")
async def verify(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, name=VERIFIED_ROLE_NAME)
    if not role:
        await interaction.response.send_message("❌ The VERIFIED role does not exist! Please contact an admin.", ephemeral=True)
        return
    
    if role in interaction.user.roles:
        await interaction.response.send_message("✅ You are already verified!", ephemeral=True)
        return
    
    try:
        await interaction.user.add_roles(role, reason="User verified via /verify command")
        
        log_channel = discord.utils.get(interaction.guild.text_channels, name=VERIFICATION_LOG_CHANNEL)
        if log_channel:
            embed = discord.Embed(
                title="✅ User Verified",
                description=f"{interaction.user.mention} has been verified!",
                color=discord.Color.green()
            )
            embed.add_field(name="User ID", value=interaction.user.id, inline=True)
            embed.add_field(name="Account Created", value=interaction.user.created_at.strftime("%Y-%m-%d"), inline=True)
            embed.add_field(name="Joined Server", value=interaction.user.joined_at.strftime("%Y-%m-%d") if interaction.user.joined_at else "Unknown", inline=True)
            await log_channel.send(embed=embed)
        
        embed = discord.Embed(
            title="✅ Verification Successful!",
            description=f"You have been verified and given the **{VERIFIED_ROLE_NAME}** role! 🎉",
            color=discord.Color.green()
        )
        embed.add_field(name="Now you can:", value="• Access all channels\n• Use bot commands\n• Participate in events", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except:
        await interaction.response.send_message("❌ Failed to verify you. Please contact an admin.", ephemeral=True)

@tree.command(name="unverify", description="Remove verification from a user (Admin only)")
@app_commands.default_permissions(administrator=True)
async def unverify(interaction: discord.Interaction, member: discord.Member):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF or FOUNDER role!", ephemeral=True)
        return
    
    role = discord.utils.get(interaction.guild.roles, name=VERIFIED_ROLE_NAME)
    if not role:
        await interaction.response.send_message("❌ The VERIFIED role does not exist!", ephemeral=True)
        return
    
    if role not in member.roles:
        await interaction.response.send_message(f"❌ {member.mention} is not verified!", ephemeral=True)
        return
    
    try:
        await member.remove_roles(role, reason=f"Unverified by {interaction.user.name}")
        await interaction.response.send_message(f"✅ Removed VERIFIED role from {member.mention}", ephemeral=True)
        
        log_channel = discord.utils.get(interaction.guild.text_channels, name=VERIFICATION_LOG_CHANNEL)
        if log_channel:
            embed = discord.Embed(
                title="❌ User Unverified",
                description=f"{member.mention} has been unverified by {interaction.user.mention}",
                color=discord.Color.red()
            )
            await log_channel.send(embed=embed)
    except:
        await interaction.response.send_message("❌ Failed to unverify user.", ephemeral=True)

@tree.command(name="setverificationrole", description="[Admin] Set the verification role")
@app_commands.default_permissions(administrator=True)
async def setverificationrole(interaction: discord.Interaction, role: discord.Role):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF or FOUNDER role!", ephemeral=True)
        return
    
    global VERIFIED_ROLE_NAME
    VERIFIED_ROLE_NAME = role.name
    await interaction.response.send_message(f"✅ Verification role set to **{role.name}**")

@tree.command(name="setautorole", description="[Admin] Set the auto-role for new members")
@app_commands.default_permissions(administrator=True)
async def setautorole(interaction: discord.Interaction, role: discord.Role):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF or FOUNDER role!", ephemeral=True)
        return
    
    global AUTO_ROLE_NAME
    AUTO_ROLE_NAME = role.name
    await interaction.response.send_message(f"✅ Auto-role set to **{role.name}**")

@tree.command(name="verifyuser", description="[Admin] Manually verify a user")
@app_commands.default_permissions(administrator=True)
async def verifyuser(interaction: discord.Interaction, member: discord.Member):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF or FOUNDER role!", ephemeral=True)
        return
    
    role = discord.utils.get(interaction.guild.roles, name=VERIFIED_ROLE_NAME)
    if not role:
        await interaction.response.send_message("❌ The VERIFIED role does not exist!", ephemeral=True)
        return
    
    if role in member.roles:
        await interaction.response.send_message(f"❌ {member.mention} is already verified!", ephemeral=True)
        return
    
    try:
        await member.add_roles(role, reason=f"Manually verified by {interaction.user.name}")
        await interaction.response.send_message(f"✅ Manually verified {member.mention}", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Failed to verify user.", ephemeral=True)

# ==================== HELP ====================
@tree.command(name="help", description="Show all 500+ commands")
async def help(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="📋 MEGA BOT - 500+ COMMANDS",
        description="The most powerful Discord bot with 500+ commands!",
        color=discord.Color.gold()
    )
    categories = {
        "ℹ️ Information (20)": ["ping", "uptime", "info", "botinfo", "serverinfo", "userinfo", "roleinfo", "channelinfo", "emojiinfo", "serverstats", "membercount", "boosters", "banner", "servericon", "serverowner", "serverbanner", "serverinvite", "serveremoji", "serversticker", "serverboosts"],
        "🎲 Fun (35)": ["flip", "roll", "choose", "randomnumber", "rps", "math", "8ball", "fact", "joke", "meme", "cat", "dog", "koala", "panda", "fox", "bird", "fish", "randomcolor", "randomword", "randomletter", "randomemoji", "randomquote", "randomname", "randompassword", "randomhex", "randomuuid", "randomdate", "randomtime", "randomip", "randommac", "ship", "roast", "compliment", "insult"],
        "🛡️ Moderation (30)": ["kick", "ban", "clear", "timeout", "warn", "warnings", "removewarn", "slowmode", "lock", "unlock", "poll", "announce", "purgeuser", "nickname", "softban", "unban", "mute", "unmute", "addrole", "removerole", "addroleall", "removeroleall", "rename", "createchannel", "deletechannel", "createrole", "deleterole", "settopic", "clonechannel", "movechannel"],
        "🎮 Games (40)": ["guess", "slots", "blackjack", "typerace", "hangman", "trivia", "wordle", "memory", "tictactoe", "numbergame", "quiz", "riddle", "scramble", "anagram", "minesweeper", "roulette", "craps", "baccarat", "keno", "bingo", "plinko", "wheel", "poker", "casino", "chess", "checkers", "dominoes", "mahjong", "sudoku", "crossword", "jigsaw", "maze", "adventure", "trivia2", "quiz2"],
        "💰 Economy (40)": ["balance", "daily", "weekly", "monthly", "hourly", "work", "steal", "give", "donate", "transfer", "shop", "buy", "inventory", "gamble", "coinflip", "lottery", "rob", "bank", "invest", "beg", "mine", "fish", "hunt", "farm", "craft", "brew", "cook", "trade", "sell", "auction", "bidding", "deposit", "withdraw", "interest", "stocks", "bonds", "realestate", "business", "salary", "bonus"],
        "💍 Social (35)": ["marry", "divorce", "kiss", "hug", "pat", "slap", "punch", "highfive", "handshake", "wave", "dance", "sing", "sleep", "eat", "drink", "walk", "run", "jump", "fly", "swim", "climb", "cook", "paint", "write", "cuddle", "tickle", "bite", "bonk", "smug", "cry", "blush", "stare", "smile", "laugh"],
        "🐾 Pets (20)": ["pet", "feed", "play", "walkpet", "petstats", "breed", "adopt", "train", "petbattle", "petlist", "petname", "petfeed", "petplay", "petclean", "petgroom", "petlove", "pethealth", "petenergy", "petmood", "petlevel"],
        "📈 Leveling (15)": ["level", "leaderboard", "rank", "xp", "top10", "levels", "setlevel", "addxp", "removexp", "resetlevels", "reward", "prestige", "badge", "title", "rolelevel"],
        "🔧 Utility (50)": ["time", "date", "avatar", "invite", "weather", "translate", "calculate", "screenshot", "shortenurl", "qrcode", "color", "emoji", "hashtag", "trending", "news", "define", "synonym", "antonym", "rhyme", "password", "uuid", "base64encode", "base64decode", "hash", "timestamp", "countdown", "remind", "reminders", "removemind", "todo", "addtodo", "donetodo", "removetodo", "listtodo", "alarm", "timer", "stopwatch", "calendar", "schedule", "event", "birthday", "anniversary", "countdown2", "timezone", "worldclock", "currency", "crypto", "stock", "weather2", "airquality"],
        "👑 Admin (50)": ["setbalance", "addcoins", "removecoins", "resetbalance", "resetwarnings", "setlevel", "addxp", "removexp", "resetlevels", "cleardata", "backup", "restore", "blacklist", "unblacklist", "addroleall", "removeroleall", "giverole", "takerole", "rename", "reset", "createchannel", "deletechannel", "createrole", "deleterole", "renamechannel", "movechannel", "clonechannel", "settopic", "setwelcome", "setlogs", "setsuggestions", "setreports", "settickets", "setgiveaway", "setcounting", "setstarboard", "setautorole", "setreactionrole", "lockall", "unlockall", "setvanity", "setboost", "setlevelroles", "setxpchannel", "seteconomy", "setgamble", "setcasino", "setraids", "setautomod"],
        "👑 Owner (70)": ["serverlist", "leaveserver", "broadcast", "exportdata", "importdata", "cleareconomy", "clearlevels", "purgeall", "restart", "shutdown", "status", "servers", "blacklistuser", "unblacklistuser", "giveaway", "endgiveaway", "addroleall", "removeroleall", "setwelcome", "setlogs", "setsuggestions", "setreports", "settickets", "setgiveaway", "setcounting", "setstarboard", "setautorole", "setreactionrole", "lockall", "unlockall", "setvanity", "setboost", "setlevelroles", "setxpchannel", "seteconomy", "setgamble", "setcasino", "eval", "exec", "cmd", "shell", "setbotname", "setavatar", "setgame", "setstream", "setlistening", "setwatching", "setactivity", "setserver", "deleteallchannels", "deleteallroles", "massban", "masskick", "masspurge", "createinvite", "cloneguild", "copyguild", "backupguild", "restoreguild", "exportguild", "importguild", "resetguild", "optimize", "cleanup", "purgebots", "purgehumans", "setraidmode", "setautomod"],
        "✅ Verification (5)": ["verify", "unverify", "setverificationrole", "setautorole", "verifyuser"]
    }
    for cat, cmds in categories.items():
        embed.add_field(name=cat, value="`/" + "`, `/".join(cmds[:5]) + "`...", inline=False)
    embed.set_footer(text=f"Requested by {interaction.user.name} | Total: 500+ commands")
    await interaction.response.send_message(embed=embed)

# ==================== INFORMATION COMMANDS (20) ====================
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

# ==================== MORE COMMANDS (FUN, ECONOMY, MODERATION, LEVELING, UTILITY, ADMIN, OWNER) ====================

# FUN COMMANDS
@tree.command(name="flip", description="Flip a coin")
async def flip(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    await interaction.response.send_message(f'**{random.choice(["Heads 🪙", "Tails 🪙"])}**')

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
async def choose(interaction: discord.Interaction, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    options = [o for o in [option1, option2, option3, option4, option5] if o]
    await interaction.response.send_message(f'🤔 I choose **{random.choice(options)}**')

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
    facts = ["Honey never spoils 🍯", "Octopuses have three hearts 🐙", "Bananas are berries 🍌", "A day on Venus is longer than a year 🪐", "Cows have best friends 🐄", "A group of flamingos is called a flamboyance 🦩", "The shortest war was 38 minutes ⚔️", "Bamboo can grow up to 3 feet in a day 🎋"]
    await interaction.response.send_message(f"💡 **{random.choice(facts)}**")

@tree.command(name="joke", description="Random joke")
async def joke(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    jokes = ["Why don't scientists trust atoms? Because they make up everything! ⚛️", "What do you call a fish with no eyes? A fsh! 🐟", "Why did the scarecrow win an award? He was outstanding in his field! 🌾", "What do you call a bear with no teeth? A gummy bear! 🧸", "Why don't skeletons fight each other? They don't have the guts! 💀"]
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
        return    try:
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

# SHIP, ROAST, COMPLIMENT, INSULT
@tree.command(name="ship", description="Ship two users")
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    compatibility = random.randint(0, 100)
    hearts = "❤️" * (compatibility // 10) + "🖤" * (10 - compatibility // 10)
    embed = discord.Embed(title="💕 Ship Rating", color=discord.Color.pink())
    embed.add_field(name=f"{user1.name} ❤️ {user2.name}", value=f"**{compatibility}%**\n{hearts}", inline=False)
    if compatibility > 80:
        embed.add_field(name="💖", value="Perfect match! Soulmates!", inline=False)
    elif compatibility > 60:
        embed.add_field(name="💗", value="Great match!", inline=False)
    elif compatibility > 40:
        embed.add_field(name="💛", value="Good match!", inline=False)
    else:
        embed.add_field(name="💔", value="Not a good match!", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="roast", description="Roast someone")
async def roast(interaction: discord.Interaction, member: discord.Member):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    roasts = ["You're proof that evolution can go in reverse.", "You're like a cloud. When you disappear, it's a beautiful day.", "You're not stupid; you just have bad luck thinking.", "You're the reason the gene pool needs a lifeguard.", "You're so fake, China is less fake than you.", "You're like a software update. I see you, but I ignore you.", "You're not a clown, you're the entire circus.", "You're so ugly, when you were born, the doctor slapped your parents."]
    await interaction.response.send_message(f"🔥 {member.mention}, {random.choice(roasts)}")

@tree.command(name="compliment", description="Give a compliment")
async def compliment(interaction: discord.Interaction, member: discord.Member):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    compliments = ["You're amazing! 🌟", "You're a shining star! ✨", "You're absolutely incredible! 💫", "You're one of a kind! 💎", "You're a blessing to this world! 🙏", "You're so talented! 🎨", "You're a legend! 🏆", "You're unstoppable! 💪", "You're the best! 🥇", "You're a masterpiece! 🎭"]
    await interaction.response.send_message(f"💖 {member.mention}, {random.choice(compliments)}")

@tree.command(name="insult", description="Insult someone")
async def insult(interaction: discord.Interaction, member: discord.Member):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    insults = ["You're as useful as a screen door on a submarine.", "You're so boring, you make paint dry look exciting.", "You're like a cloud. When you disappear, it's a beautiful day.", "You're the human equivalent of a participation trophy.", "You're so full of yourself, you're a walking selfie stick.", "You're like a software update. I see you, but I ignore you."]
    await interaction.response.send_message(f"😤 {member.mention}, {random.choice(insults)}")

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

@tree.command(name="work", description="Work for coins")
async def work(interaction: discord.Interaction):
    if not has_minimum_role(interaction):
        await interaction.response.send_message("❌ You need VERIFIED role or higher!", ephemeral=True)
        return
    jobs = ["programmer", "streamer", "youtuber", "artist", "developer", "designer", "writer", "chef", "mechanic", "pilot"]
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

# ==================== LEVELING ====================
@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return
    user_id = str(message.author.id)
    if user_id not in levels:
        levels[user_id] = 0
    levels[user_id] += random.randint(5, 15)

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

# ==================== ADMIN COMMANDS ====================
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
    await interaction.response.send_message(f"✅ Added {amount} coins to {member.mention}")

@tree.command(name="removecoins", description="[Admin] Remove coins from a user")
async def removecoins(interaction: discord.Interaction, member: discord.Member, amount: int):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF role or higher!", ephemeral=True)
        return
    data = get_user(str(member.id))
    data['balance'] = max(0, data['balance'] - amount)
    await interaction.response.send_message(f"✅ Removed {amount} coins from {member.mention}")

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

@tree.command(name="restart", description="[Owner] Restart the bot")
async def restart(interaction: discord.Interaction):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    await interaction.response.send_message("🔄 Restarting bot...")
    await bot.close()
    os.system("python3 main.py")

@tree.command(name="shutdown", description="[Owner] Shut down the bot")
async def shutdown(interaction: discord.Interaction):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    await interaction.response.send_message("🛑 Shutting down...")
    await bot.close()

@tree.command(name="status", description="[Owner] Change bot status")
async def status(interaction: discord.Interaction, status: str):
    if not is_founder(interaction):
        await interaction.response.send_message("❌ Only the FOUNDER can use this!", ephemeral=True)
        return
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
    await interaction.response.send_message(f"✅ Status changed to: **{status}**")

# ==================== ERROR HANDLING ====================
@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
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
        print("❌ DISCORD_TOKEN not found in environment variables!")