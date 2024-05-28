from typing import Final
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from classPlanner import classPlanner

#LOAD DISCORD TOKEN
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

#SETUP BOT
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

#HANDLING BOT STARTUP
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

#BOT COMMANDS

@bot.tree.command(name="plan")
@app_commands.describe(klasa="Nazwa klasy", day="Dzień tygodnia, dla którego ma być wyświetlony plan")
async def plan(interaction: discord.Interaction, klasa: str, day: str):
    classP = classPlanner(klasa, day)
    print(classP.getLessonsIds())
    if classP.getDayAsNumber() == "":
        await interaction.response.send_message("Podano nieprawidłową nazwę dnia tygodnia")
    else:
        await interaction.response.send_message(f"Plan lekcji klasy {klasa} w {day}: "+classP.createCodeBlockResponse(classP.getLessonsForSpecificDay()))

@bot.tree.command(name="subjects")
@app_commands.describe(klasa="Nazwa klasy")
async def subjects(interaction: discord.Interaction, klasa: str):
    classP = classPlanner(klasa, None)
    if classP.getDayAsNumber() == "":
        await interaction.response.send_message("Podano nieprawidłową nazwę klasy")
    else:
        await interaction.response.send_message(f"Przedmioty klasy {klasa}: "+classP.createCodeBlockResponse(classP.getSubjectNames()))


#CREATE MAIN ENTRY POINT
def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()