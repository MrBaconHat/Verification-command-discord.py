import discord
from discord.ext import commands
import requests
import random
import string

token = 'paste your bot token here inside the comas.'
verified_role_id = "paste your role ID here."  # this will be used to give user verified role once they successfully verify


intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
intents.message_content = True


'''
_______________________________________________________WARNING_______________________________________________________

DO NOT ATTEMPT TO CHANGE ANYTHING BELOW. ONLY CHANGE IF YOU KNOW WHAT YOU ARE DOING. 
BELOW CODE IS SENSITIVE MAKING CHANGES WHICH YOU DONT UNDERSTAND MIGHT RESULT IN GIVING BACKDOOR OF YOUR BOT TO SOMEONE. 
PLEASE ONLY ATTEMPT TO ENTER THIS ZONE IF YOU KNOW WHAT YOU ARE DOING. IF SOMEBODY IS TELLING YOU TO PASTE THEIRS CODE 
INSIDE THIS ZONE DO NOT PASTE IT. IT MAY BE MALICIOUS AND MIGHT INFECT THE CODE AND THE BOT.
AND DO NOT SHARE YOUR BOT TOKEN WITH ANYONE ONLINE SPECIALLY WHEN YOU ARE GIVING THIS CODE TO SOMEBODY. 
EXPOSING YOUR BOTS TOKEN WILL RESULT IN YOUR BOT GETTING CONTROLLED BY SOMEBODY ELSE.

_____________________________________________________________________________________________________________________
'''


def generate_random_strings(length):
    result = ''
    for count in range(length):
        if random.choice([True, False]):
            result += random.choice(str(string.ascii_letters))
        else:
            result += random.choice(str(string.digits))
    return result

def add_role(server_id, user_id):

    url = f'https://discord.com/api/v10/guilds/{server_id}/members/{user_id}/roles/{verified_role_id}'

    headers = {
        'Authorization': f'Bot {token}'
    }
    response = requests.put(url=url, headers=headers)
    if response.status_code == 204:
        return 'Success'
    elif response.status_code == 403:
        return 'Missing perms'

class verification_modal(discord.ui.Modal, title='Verification Form'):
    def __init__(self, generated_code):
        super().__init__()
        self.code = generated_code
    user_input = discord.ui.TextInput(
        style=discord.TextStyle.short,
        required=True,
        label='Q1: Please enter your verification code below',
        placeholder='...'
    )

    async def on_submit(self, interaction: discord.Interaction):

        if str(self.user_input).lower() == str(self.code).lower():
            response = add_role(server_id=interaction.guild.id, user_id=interaction.user.id)
            if response == 'Success':
                await interaction.response.edit_message(content='Successfully verified!!!', embed=None,
                                                        view=discord.ui.View())
            elif response == 'Missing perms':
                await interaction.response.send_message('I dont have permission to add roles. '
                                                        'Please contact a server admin and ask them to give me the '
                                                        'Manage roles permission.', ephemeral=True)

        elif str(self.user_input).lower() != str(self.code).lower():
            await interaction.response.send_message(f'The code you entered: **{self.user_input}** is incorrect. '
                                                    f'Please enter the correct code.', ephemeral=True)

class verify_button(discord.ui.View):
    def __init__(self, generated_code):
        super().__init__()
        self.code = generated_code

    @discord.ui.button(label='Enter and verify!', style=discord.ButtonStyle.success)
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = verification_modal(generated_code=self.code)
        await interaction.response.send_modal(view)

class start_verify_button(discord.ui.View):

    @discord.ui.button(label='Click to verify', style=discord.ButtonStyle.success)
    async def start_verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = generate_random_string(length=6)
        embed = discord.Embed(
            title='Verification code.',
            description='To verify please submit the code by pressing the button below.',
            color=discord.Color.brand_green()
        )
        embed.add_field(name='**Generated Code**', value=f'```{result}```')
        view = verify_button(generated_code=result)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


@bot.hybrid_command(name='verification')
async def verification(ctx, channel: discord.TextChannel):
    view = start_verify_button()
    embed = discord.Embed(
        title=f"{ctx.guild.name}'s Verification",
        description=f'In order to get access to rest of the server please go a head and press '
                    f'"Click to verify" button below.',
        color=discord.Color.brand_green()
    )
    embed.set_footer(text='Note: Pressing button will always generate a new code everytime')
    try:
        await channel.send(view=view, embed=embed)
    except discord.errors.Forbidden:
        await ctx.send(f"I don't have permission to send messages in: {channel.name} please make sure i have "
                       f"**Send Messages** permission in the channel.", ephemeral=True)
    else:
        await ctx.send(f"Successfully placed the button in: "
                       f"[{channel.name}](<https://discord.com/channels/{ctx.guild.id}/{channel.id}>)", ephemeral=True)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Successfully logged in as: {bot.user.name}. Invite: https://discord.com/oauth2/authorize?'
          f'client_id={bot.user.id}&permissions=8&scope=applications.commands+bot')


bot.run(token)
