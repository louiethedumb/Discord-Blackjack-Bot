#imports
import random
from random import Random

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

#init dotenv
load_dotenv()

#set token (req file named .env configured with your token)
token = os.getenv('DISCORD_TOKEN')

#rigged the game
Rigged_ID = 0#discord ID of someone you hate lol

#init intents
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
intents.reactions = True
intents.guilds = True
intents.emojis = True

#games active
Hands = []
active_users = []
Dealer_Hands = []


#dealer logic
bot = commands.Bot(command_prefix='b!', intents=intents)
@bot.event
async def on_ready():
    print(f"black jack online, im {bot.user.name}")
@bot.event
async def on_member_join(member):
    x = ["gambling", "cards", "dice", "Las Vegas"]
    channel = member.guild.system_channel
    if channel:
        await channel.send(f'{member.mention} Greetings {member.name}, Do you like {random.choice(x)}?')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        if "blackjack" in message.content.lower():
            x = ["hate","stupid","rigged","unfair","bullshit","fuck"]
            y = False
            for i in range(len(x)):
                if x[i] in message.content.lower():
                    y = True
            if not y:
                await message.channel.send(f"{message.author.mention} Did somebody say blackjack? (do b!new to start blackjack)")
            else:
                await message.channel.send(f"{message.author.mention} DONT HATE ON BLACKJACK")
    await bot.process_commands(message)
@bot.command()
async def new(ctx):
    if ctx.author.id not in active_users:
        await ctx.send('Welcome to Blackjack!')
        user_id = ctx.author.id
        active_users.append(user_id)
        Hands.append((random.randint(2,10) + random.randint(2,10)))
        Dealer_Hands.append((random.randint(2,10) + random.randint(2,10)))
        index = active_users.index(ctx.author.id)
        await ctx.send(f'Your hand: {Hands[index]}')
        await ctx.send(f'Dealer hand: {Dealer_Hands[index]}')
    else:
        await ctx.send('You are already playing blackjack!, Do b!reset to clear the match')
@bot.command()
async def hand(ctx):
    if ctx.author.id in active_users:
        index = active_users.index(ctx.author.id)
        await ctx.send(f'Your hand: {Hands[index]}')
        await ctx.send(f'Dealer hand: {Dealer_Hands[index]}')
    else:
        await ctx.send('You are not playing blackjack!, Do b!new to start')
@bot.command()
async def reset(ctx):
    if ctx.author.id in active_users:
        index = active_users.index(ctx.author.id)
        Hands.pop(index)
        active_users.remove(ctx.author.id)
        await ctx.send(f'Your hand has been reset')
    else:
        await ctx.send('You are not in playing blackjack!, Do b!new to start')
@bot.command()
async def hit(ctx):
    if ctx.author.id in active_users:
        index = active_users.index(ctx.author.id)
        if ctx.author.id == Rigged_ID:
            Hands[index] = random.randint(Hands[index] + (21 - Hands[index]),(Hands[index] + (21 - Hands[index])) + 10)
            await ctx.send(f'{Hands[index]} > 21, You lose')
            Hands.pop(index)
            active_users.remove(ctx.author.id)
        else:
            hand = Hands[index]
            #did you get an ace?
            if random.randrange(0,52,1) > 48:
                #will it kill ya?
                if (hand + 11) > 21:
                    #yes
                    hand += 1
                else:
                    #no
                    hand += 11
            else:
                #if you didn't get an ace what did you get?
                hand += random.randrange(2,10,1)
            #does it kill you?
            if hand > 21:
                #yes
                await ctx.send(f'{hand} > 21, You lose')
                Hands.pop(index)
                active_users.remove(ctx.author.id)
            else:
                #did you get 21?
                if hand == 21:
                    #yes
                    await ctx.send(f'{hand} = 21, You win')
                    Hands.pop(index)
                    active_users.remove(ctx.author.id)
                #no
                Hands[index] = hand
                await ctx.send(f'Your hand: {Hands[index]}')
                # v same as ^ but for the dealer with additions for (VERY) basic AI
                Dhand = Dealer_Hands[index]
                if not Dealer_Hands[index] >= 17:
                    if random.randrange(0, 52, 1) > 48:
                        if (Dhand + 11) > 21:
                            Dhand += 1
                        else:
                            Dhand += 11
                    else:
                        Dhand += random.randrange(2, 10, 1)
                    if Dhand > 21:
                        await ctx.send(f'Dealer hand: {Dhand} > 21, You Win')
                        Hands.pop(index)
                        active_users.remove(ctx.author.id)
                    elif Dhand == 21:
                        await ctx.send(f'Dealer hand: {Dhand} = 21, You Lose')
                        Hands.pop(index)
                        active_users.remove(ctx.author.id)
                    else:
                        Dealer_Hands[index] = Dhand
                        await ctx.send(f'Dealer Hits')
                        await ctx.send(f'Dealer hand: {Dealer_Hands[index]}')
                else:
                    await ctx.send(f'Dealer Stands')
                    await ctx.send(f'Dealer hand: {Dealer_Hands[index]}')
    else:
        await ctx.send('You are not playing blackjack!, Do b!new to start')
@bot.command()
async def stand(ctx):
    if ctx.author.id in active_users:
        index = active_users.index(ctx.author.id)
        if Hands[index] < Dealer_Hands[index]:
            await ctx.send(f'You stand on {Hands[index]}')
            await ctx.send(f'{Hands[index]} < {Dealer_Hands[index]}, You Lose')
            Hands.pop(index)
            active_users.remove(ctx.author.id)
        else:
            await ctx.send(f'Your hand: {Hands[index]}')
            Dhand = Dealer_Hands[index]
            if not Dealer_Hands[index] >= 17:
                if random.randrange(0, 52, 1) > 48:
                    if (Dhand + 11) > 21:
                        Dhand += 1
                    else:
                        Dhand += 11
                else:
                    Dhand += random.randrange(2, 10, 1)
                if Dhand > 21:
                    await ctx.send(f'Dealer hand: {Dhand} > 21, You Win')
                    Hands.pop(index)
                    active_users.remove(ctx.author.id)
                elif Dhand == 21:
                    await ctx.send(f'Dealer hand: {Dhand} = 21, You Lose')
                    Hands.pop(index)
                    active_users.remove(ctx.author.id)
                else:
                    Dealer_Hands[index] = Dhand
                    await ctx.send(f'Dealer Hits')
                    await ctx.send(f'Dealer hand: {Dealer_Hands[index]}')
            else:
                await ctx.send(f'Dealer Stands')
                await ctx.send(f'Dealer hand: {Dealer_Hands[index]}')
    else:
        await ctx.send('You are not playing blackjack!, Do b!new to start')

@bot.command()
async def h(ctx):
    await ctx.send(f'h - Prints list of commands')
    await ctx.send(f'new - Starts new game')
    await ctx.send(f'reset - Resets game')
    await ctx.send(f'hit - draw a card')
    await ctx.send(f'stand - pass your turn')
    await ctx.send(f"hand - show your hand and the dealer's hand")
#run bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
