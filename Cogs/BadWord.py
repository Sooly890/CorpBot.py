import discord, time, tempfile, os, shutil, json
import regex as re
from discord.ext import commands
from datetime import timedelta
from Cogs import Settings, DisplayName, Utils

def setup(bot):
	# Add the bot and deps
	settings = bot.get_cog("Settings")
	bot.add_cog(BadWord(bot, settings))

class BadWord(commands.Cog):
	# Init with the bot reference, and a reference to the settings var
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		global Utils, DisplayName
		Utils = self.bot.get_cog("Utils")
		DisplayName = self.bot.get_cog("DisplayName")

	@commands.command(pass_context=True)
	async def badworddisable(self, ctx):
		"""Disables BadWord (bot-admin only)"""
		await ctx.send("BadWord disabled")
