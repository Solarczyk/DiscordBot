from typing import Final
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from classPlanner import classPlanner
from classroomsPlanner import classroomsPlanner

#LOAD DISCORD TOKEN
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')  #Token znajduje się w pliku .env. Wygenerowany przez discorda

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
#interaction.response.send_message nie jest widoczne dla PyCharma, ale nadal normalnie działa. Jest to błąd po stronie aplikacji
@bot.tree.command(name="plan")  #Wyświetl plan lekcji na konkretny dzień
@app_commands.describe(klasa="Nazwa klasy", day="Dzień tygodnia, dla którego ma być wyświetlony plan")
async def plan(interaction: discord.Interaction, klasa: str, day: str):

    if day == "1" or day == "poniedzialek":
        day = "poniedziałek"
    if day == '2':
        day = "wtorek"
    if day == '3' or day == 'sroda':
        day = "środa"
    if day == '4':
        day = "czwartek"
    if day == '5' or day == 'piatek':
        day = "piątek"
    classP = classPlanner(klasa, day)
    if classP.getClassId() == "":
        await interaction.response.send_message("Podano nieprawidłową nazwę klasy")
    elif classP.getDayAsNumber() == "":
        await interaction.response.send_message("Podano nieprawidłową nazwę dnia tygodnia")
    else:
        await interaction.response.send_message(f"Plan lekcji klasy {klasa} - {day}: "+classP.createCodeBlockResponse(classP.getLessonsForSpecificDay()))

@bot.tree.command(name="subjects")  #Wyświetl przedmioty, które obowiązują podaną klasę
@app_commands.describe(klasa="Nazwa klasy")
async def subjects(interaction: discord.Interaction, klasa: str):
    classP = classPlanner(klasa, None)
    if classP.getClassId() == "":
        await interaction.response.send_message("Podano nieprawidłową nazwę klasy")
    else:
        await interaction.response.send_message(f"Przedmioty klasy {klasa}: "+classP.createCodeBlockResponse(classP.getSubjectNames()))


@bot.tree.command(name="okienka")  #Wyświetl wolne gabinety na dany dzień !!!JESZCZE NIE DZIAŁA POPRAWNIE!!!
@app_commands.describe(day="Dzień tygodnia, dla którego mają być wyświetlone wolne sale")
async def okienka(interaction: discord.Interaction, day: str):

    if day == "poniedziałek" or day == "poniedzialek" or day == "1":
        day = "0"
    if day == "wtorek" or day == "2":
        day = "1"
    if day == "środa" or day == 'sroda' or day == "3":
        day = "2"
    if day == "czwartek" or day == "4":
        day = "3"
    if day == "piątek" or day == "piatek" or day == "5":
        day = "4"
    classroomsP = classroomsPlanner(day)

    if classroomsP.getClassIds() == "":
        await interaction.response.send_message("Podano nieprawidłową nazwę dnia tygodnia")
    else:
        await interaction.response.send_message("Wolne klasy na podany dzień: "+classroomsP.createCodeBlockResponse(classroomsP.sortClassroomsByHour()))

#CREATE MAIN ENTRY POINT
def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()