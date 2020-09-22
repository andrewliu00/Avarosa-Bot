import os

import discord
import random
from discord.ext import commands
from dotenv import load_dotenv
from requests import get
from bs4 import BeautifulSoup

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready(): 
    print('Bot is ready.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.cooldown(1,4,commands.BucketType.guild)
async def opgg(ctx, name):
    name = name
    url = 'https://na.op.gg/summoner/userName=' + name
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    #rank_badge = html_soup.find('div', class_='SummonerRatingMedium')
    #rank_badge = rank_badge.img['src']
    summ_name = html_soup.find('span', class_='Name')
    summ_name = summ_name.text
    rank = html_soup.find('div', class_='TierRank')
    rank = rank.text
    rank_type = html_soup.find('div', class_='RankType')
    rank_type = rank_type.text
    league_points = html_soup.find('span', class_='LeaguePoints')
    league_points = (league_points.text)
    league_points = league_points.strip('\n').strip('\t').strip()
    win = html_soup.find('span', class_='wins')
    win = win.text
    loss = html_soup.find('span', class_='losses')
    loss = loss.text
    WL = win + '/' + loss
    embed = discord.Embed(
        title = name,
        color = discord.Color.blue()
    )

    embed.add_field(name = 'Rank', value = rank, inline=False)
    embed.add_field(name = 'Rank Type', value = rank_type, inline=False)
    embed.add_field(name = 'LP', value = league_points, inline=False)
    embed.add_field(name = 'Win/Loss', value = WL, inline=False)
    #await ctx.send(summ_name  + '\n' + rank + '\n' + rank_type + '\n' + league_points + '\n' + win + '/' + loss)
    await ctx.send(embed=embed)

@opgg.error
async def opgg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'Oops! Looks like you called this command too soon, please try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@client.command()
@commands.cooldown(1,4,commands.BucketType.guild)
async def mpchamp(ctx, name):
    name = name
    url = 'https://na.op.gg/summoner/userName=' + name
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    champbox = html_soup.find('div', class_='ChampionBox')
    mpc = champbox.find('div', class_='Face')
    mpc = mpc['title']
    cs = champbox.find('div', class_='ChampionMinionKill')
    cs = cs.text.strip('\n').strip('\t').strip()
    cs = cs[3:]
    pkda = champbox.find('div', class_='PersonalKDA')
    fullkda = pkda.find('span', class_='KDA').text
    eachkda = champbox.find('div', class_='KDAEach')
    specific_kda = eachkda.find('span', class_='Kill').text + '/' + eachkda.find('span', class_='Death').text + '/' + eachkda.find('span', class_='Assist').text

    embed = discord.Embed(
        title = name + "'s Most Played Champ",
        color = discord.Color.blue()
    )

    embed.add_field(name = 'Champion', value = mpc, inline=False)
    embed.add_field(name = 'cs', value = cs, inline=False)
    embed.add_field(name = 'KDA', value = fullkda + '\n' + specific_kda, inline=False)
    #await ctx.send(summ_name  + '\n' + rank + '\n' + rank_type + '\n' + league_points + '\n' + win + '/' + loss)
    await ctx.send(embed=embed)

@mpchamp.error
async def mpchamp_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'Oops! Looks like you called this command too soon, please try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


client.run(token)