import discord
from discord.ext import commands
import sys

class Runcode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("runcode: loaded")

    @commands.command()
    async def runcode(self, ctx,*, code=None):
        """runcode"""
        try:
            #save original standart output reference

            original_stdout = sys.stdout
            sys.stdout = open('output.txt', 'w') #change the standard output to the file we created

            #execute code

            exec(code)  #example =>   print("hello world")

            sys.stdout.close()

            sys.stdout = original_stdout  #reset the standard output to its original value

            # finally read output from file and save in output variable

            output = open('output.txt', 'r').read()

        except Exception as e:
            # to return error in the code
            sys.stdout = original_stdout
            output = e
        await ctx.send(f"**code**  ```{code}```")
        await ctx.send(f"**output** ```{output}```")

def setup(bot):
    bot.add_cog(Runcode(bot))