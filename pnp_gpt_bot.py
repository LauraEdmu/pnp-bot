import discord
from discord import app_commands
from openai_manager import OpenaiManager
import logging
import aiofiles
import re

OAI = OpenaiManager()

needed_intents = discord.Intents.default()
needed_intents.message_content = True
needed_intents.members = True
client = discord.Client(intents=needed_intents)
tree = app_commands.CommandTree(client)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('pnp_bot.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

banned_words_pattern = None # Initialize banned words pattern

async def read_banned_words():
	try:
		async with aiofiles.open("banned_words.txt", 'r') as banned_words_file:
			banned_words = await banned_words_file.read()
			banned_words = banned_words.split("\n")
		return banned_words
	except FileNotFoundError:
		logger.error("Could not find banned words file")
		return []

@client.event
async def on_ready():
	await tree.sync()

	await client.change_presence(
		status=discord.Status.online,
		activity=discord.Game("Here to Help!")
	)

	logger.debug(f"Logged in as {client.user}")
	
	await OAI.load_key("openai.priv") # Load OpenAI key

	global banned_words_pattern
	banned_words = await read_banned_words()
	if banned_words:
		banned_words_pattern = re.compile(r"\b(" + "|".join(banned_words) + r")\b", re.IGNORECASE)
		logger.debug(f"Read the banned words")
	else:
		banned_words_pattern = None
		logger.error(f"Could not read the banned words")


async def banned_words_check(message): # Function to check for banned words using global banned_words list and regex
	if banned_words_pattern:
		if banned_words_pattern.search(message.content):
			await message.delete()
			# await message.channel.send("Please refrain from using inappropriate language. Your message has been deleted.")
			return True
		else:
			return False
	

@tree.command(name="ask", description="Ask the bot a question")
async def ask(interaction, msg: str):
	if await banned_words_check(interaction):
		await interaction.response.send_message("Please refrain from using inappropriate language. Your message has been deleted.", ephemeral=True)
		return

	logger.debug(f"Received message: {msg}")
	
	async with aiofiles.open("system_message.txt", 'r') as system_message_file:
		system_message = await system_message_file.read()

	resp = await OAI.chat(msg, smsg=system_message, model="gpt-4o-mini", amnesia=True)
	await interaction.response.send_message(resp)

	logger.debug(f"Response: {resp}")

if __name__ == '__main__':
	logger.debug("Starting bot")
	try:
		with open("bot.priv", 'r') as token_file:
			token = token_file.read()
		logger.debug("Read token")
		
		client.run(token)
	except FileNotFoundError:
		logger.critical("Could not find token")
	except Exception as e:
		logger.critical(f"Error: {e}")