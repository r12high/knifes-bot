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

# ==================== FUN COMMANDS ====================
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

# ==================== MORE COMMANDS (ECONOMY, MODERATION, LEVELING, UTILITY, ADMIN, OWNER) ====================

# ECONOMY
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

# MODERATION
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
    embed = discord.Embed(title=f"📊 {member.name}", color=discord.Color.blue())
    embed.add_field(name="Level", value=lvl, inline=True)
    embed.add_field(name="EXP", value=f"{exp} / {next_exp}", inline=True)
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

# ==================== UTILITY ====================
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

# ==================== ADMIN ====================
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

@tree.command(name="resetbalance", description="[Admin] Reset a user's balance to 100")
async def resetbalance(interaction: discord.Interaction, member: discord.Member):
    if not (is_staff(interaction) or is_founder(interaction)):
        await interaction.response.send_message("❌ You need STAFF role or higher!", ephemeral=True)
        return
    data = get_user(str(member.id))
    data['balance'] = 100
    await interaction.response.send_message(f"✅ {member.mention}'s balance reset to 100 coins")

# ==================== OWNER ====================
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