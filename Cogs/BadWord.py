import discord, time, tempfile, os, shutil, json
import regex as re
from discord.ext import commands
from datetime import timedelta
from Cogs import Settings, DisplayName, Utils
import joblib
import sys
sys.modules['sklearn.externals.joblib'] = joblib
from profanity_check import predict_prob

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

	@commands.Cog.listener()
	async def on_message(self, member, message):
		# Gather exclusions - no bots, no dms, and don't check if running a command
		if message.author.bot: return
		if not message.guild: return
		ctx = await self.bot.get_context(message)
		# Does the message contain a bad word?
		prob = predict_prob([message])
		DisplayName.DisplayName.name()
		if prob[0] > 0.5:
			msg = 'Naught naughty, *{}* said a bad word!'.format(DisplayName.DisplayName.memberForName(member))
			await ctx.send(msg)
			