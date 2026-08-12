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

# ==================== AUTO-ROLE & VERIFICATION CONFIG ====================
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
todo_list = {}
scheduled_events = {}
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

# ==================== HELP COMMANDS ====================
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
        "ℹ️ Information": ["ping", "uptime", "info", "botinfo", "serverinfo", "userinfo", "roleinfo", "channelinfo", "emojiinfo", "serverstats", "membercount", "boosters", "banner", "servericon", "serverowner"],
        "🎲 Fun": ["flip", "roll", "choose", "randomnumber", "rps", "math", "8ball", "fact", "joke", "meme", "cat", "dog", "randomcolor", "randomword", "randomletter", "randomemoji", "randomquote", "randomname", "randompassword", "ship", "roast", "compliment", "insult"],
        "🛡️ Moderation": ["kick", "ban", "clear", "timeout", "warn", "warnings", "removewarn", "slowmode", "lock", "unlock", "poll", "announce", "purgeuser", "nickname", "unban", "mute", "unmute"],
        "💰 Economy": ["balance", "daily", "weekly", "monthly", "hourly", "work", "steal", "give", "donate", "transfer", "shop", "buy", "inventory", "gamble", "coinflip", "lottery", "rob", "bank", "invest", "beg"],
        "📈 Leveling": ["level", "leaderboard", "rank", "xp", "top10", "levels"],
        "🔧 Utility": ["time", "date", "avatar", "invite", "weather", "translate", "calculate", "timestamp", "countdown"],
        "👑 Admin": ["setbalance", "addcoins", "removecoins", "resetbalance", "resetwarnings", "setlevel", "addxp", "removexp", "resetlevels", "addrole", "removerole", "createchannel", "deletechannel", "createrole", "deleterole"],
        "👑 Owner": ["serverlist", "leaveserver", "broadcast", "exportdata", "importdata", "cleareconomy", "clearlevels", "restart", "shutdown", "status", "servers", "blacklistuser", "unblacklistuser"],
        "✅ Verification": ["verify", "unverify", "setverificationrole", "setautorole", "verifyuser"]
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
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
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
    embed.add_field(name="