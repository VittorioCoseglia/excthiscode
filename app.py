from flask import Flask, request, render_template, redirect
import sys
import discord
from discord.ext import commands
import os
from functools import partial
from threading import Thread
import asyncio

app = Flask(__name__)
token = "your token"

@app.route('/')
def home():
    return redirect("/comp")

@app.route('/comp')
def compiler():
	return render_template('comp.html', methods=['POST'])

@app.route('/runcode', methods=['GET', 'POST'])
def runcode():

    if request.method == "POST":
        codeareadata = request.form['codearea']

        try:
            #save original standart output reference

            original_stdout = sys.stdout
            sys.stdout = open('output.txt', 'w') #change the standard output to the file we created

            #execute code

            exec(codeareadata)  #example =>   print("hello world")

            sys.stdout.close()

            sys.stdout = original_stdout  #reset the standard output to its original value

            # finally read output from file and save in output variable

            output = open('output.txt', 'r').read()

        except Exception as e:
            # to return error in the code
            sys.stdout = original_stdout
            output = e


    #finally return and render index page and send codedata and output to show on page

    return render_template("comp.html", code=codeareadata, output=output)



#discord bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), case_insensitive=True, help_command=None)

async def status_task():
    while True:
        await bot.change_presence(activity=discord.Streaming(name=f' {len(bot.guilds)} servers ', url='https://www.twitch.tv/vitttwitchyt'))
        await asyncio.sleep(40)
        activity = discord.Game(name="Netflix", type=3)
        await bot.change_presence(status=discord.Status.idle, activity=activity)
        await asyncio.sleep(30)

@bot.event
async def on_ready():
    print(f"Bot Logged in {bot.user}.")
    bot.loop.create_task(status_task())

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): # or discord.ext.commands.errors.CommandNotFound as you wrote
        await ctx.send("wrong command")

for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"commands.{filename[:-3]}")


# Make a partial app.run to pass args/kwargs to it
partial_run = partial(app.run, host="0.0.0.0", port=80, debug=True, use_reloader=False,)
# Run the Flask app in another thread.
# Unfortunately this means we can't have hot reload
# (We turned it off above)
# Because there's no signal support.
t = Thread(target=partial_run)
t.start()
# Run the bot
bot.run(token)
