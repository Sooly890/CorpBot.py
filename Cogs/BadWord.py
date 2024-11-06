import discord, time, tempfile, os, shutil, json
import regex as re
from discord.ext import commands
from datetime import timedelta
from Cogs import Settings, DisplayName, Utils
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

	@commands.command(pass_context=True)
	async def badwordenable(self, ctx):
		"""Enables BadWord (bot-admin only)."""
		if not await Utils.is_bot_admin_reply(ctx):
			return
		serverOptions = self.settings.getServerStat(ctx.guild, "BadWord")

		serverOptionsSet = set(serverOptions)
		if not "enabled" in serverOptionsSet:
			serverOptions.append("enabled")
		
		# Save the updated options
		self.settings.setServerStat(ctx.guild, "BadWord", serverOptions)

		await ctx.send("BadWord enabled")

	@commands.command(pass_context=True)
	async def badworddisable(self, ctx):
		"""Disables BadWord (bot-admin only)."""
		if not await Utils.is_bot_admin_reply(ctx):
			return
		serverOptions = self.settings.getServerStat(ctx.guild, "BadWord")

		serverOptionsSet = set(serverOptions)
		if "enabled" in serverOptionsSet:
			serverOptions.remove("enabled")
		
		# Save the updated options
		self.settings.setServerStat(ctx.guild, "BadWord", serverOptions)

		await ctx.send("BadWord disabled")
		
	@commands.Cog.listener()
	async def on_message(self, message):
		# Gather exclusions - no bots, no dms, and don't check if running a command
		if message.author.bot:
			return
		if not message.guild:
			return
		ctx = await self.bot.get_context(message)
		# Does the message contain a bad word?
		prob = predict_prob([message.content])  # Predicts based on message content, not message object
		if prob[0] > 0.5:
			msg = 'Naughty naughty, *{}* said a bad word!'.format(DisplayName.name(ctx.author))
			await ctx.send(msg)