from code import interact

import discord
from discord.app_commands import guilds
from discord.ext import commands
from discord import app_commands, Embed, message
from pyexpat.errors import messages
import os

# =========================
# CONFIG
# =========================

SERVER_ID = os.getenv("SERVER_ID")
TOKEN = os.getenv("TOKEN")

GUILD_ID = discord.Object(id=SERVER_ID)

# logs_channel = discord.utils.get(
#     interaction.guild.text_channels,
#     name="logs"
# )

# =========================
# BOT
# =========================

class Client(commands.Bot):

    def get_logs_channel(self, guild):
        return discord.utils.get(guild.text_channels, name="〔👻〕ʟᴏɢꜱ")

    def get_hello_channel(self, guild):
        return discord.utils.get(guild.text_channels, name="〔👋〕ᴘʀᴢʏᴡɪᴛᴀɴɪᴀ")

    def get_boost_channel(self, guild):
        return discord.utils.get(guild.text_channels, name="〔📋〕ᴡꜱᴘᴀʀᴄɪᴇ")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

        try:
            synced = await self.tree.sync(guild=GUILD_ID)

            print(f'Synced {len(synced)} commands')

        except Exception as e:
            print(e)

    # EVENTS
    async def on_message(self, message):

        # if message.content.lower() == "Jak zapisać się na pani kurs?".lower():
        #     await message.channel.send("na stronie www.....pl/kursy", delete_after=600)

        if message.author == self.user:
            return

        print(f'{message.author}: {message.content}')

        if message.content.startswith("hello"):
            await message.channel.send(
                f'Hi {message.author.mention}!'
            )

        logs_channel = self.get_logs_channel(message.guild)

        if logs_channel:
            embed = discord.Embed(
                title="New Message",
                color=discord.Color.blue()
            )

            embed.add_field(
                name="Author",
                value=message.author.mention,
                inline=False
            )

            embed.add_field(
                name="Channel",
                value=message.channel.mention,
                inline=False
            )

            embed.add_field(
                name="Message",
                value=message.content,
                inline=False
            )

            embed.set_thumbnail(url=message.author.display_avatar.url)

            await logs_channel.send(embed=embed)

        await self.process_commands(message)

    async def on_reaction_add(self, reaction, user):
        logs_channel = self.get_logs_channel(reaction.message.guild)

        if logs_channel:
            embed = discord.Embed(
                title="Reaction Added",
                color=discord.Color.green()
            )

            embed.add_field(
                name="User",
                value=user.mention,
                inline=False
            )

            embed.add_field(
                name="Reaction",
                value=reaction.emoji,
                inline=False
            )

            embed.add_field(
                name="Message",
                value=reaction.message.content,
                inline=False
            )

            embed.add_field(
                name="Channel",
                value=reaction.message.channel.mention,
                inline=False
            )

            await logs_channel.send(embed=embed)

        if user.bot:
            return

        guild = reaction.message.guild

        if not guild:
            return

        if hasattr(self, "colour_role_message_id") and reaction.message.id != self.colour_role_message_id:
            return

        emoji = str(reaction.emoji)

        reaction_role_map = {
            "❤️": "Czerwony",
            "💙": "Niebieski",
            "🩷": "Różowy",
            "💚": "Zielony",
            "💛": "Żółty",
            "🧡": "Pomarańczowy",
        }

        if emoji in reaction_role_map:
            role_name = reaction_role_map[emoji]
            role = discord.utils.get(guild.roles, name=role_name)

            if role and user:
                await user.add_roles(role)
                print(f"Assigned {role} to {user}")

        if user.bot:
            return

        guild = reaction.message.guild

        if not guild:
            return

        if hasattr(self, "verify_message_id") and reaction.message.id != self.verify_message_id:
            return

        emoji = str(reaction.emoji)

        reaction_role_map_e = {
            "✅": "Zweryfikowany/a"
        }

        if emoji in reaction_role_map_e:
            role_name = reaction_role_map_e[emoji]
            role = discord.utils.get(guild.roles, name=role_name)

            unverified_role = discord.utils.get(guild.roles, name="Nie Zweryfikowany/a")

            if role and user:
                await user.add_roles(role)

                if unverified_role:
                    await user.remove_roles(unverified_role)

                print(f"Assigned {role} to {user}")

    async def on_reaction_remove(self, reaction, user):
        logs = self.get_logs_channel(reaction.message.guild)

        if logs:
            embed = discord.Embed(
                title="Reaction Removed",
                color=discord.Color.blurple()
            )

            embed.add_field(
                name="User",
                value=user.mention,
                inline=False
            )

            embed.add_field(
                name="Reaction",
                value=reaction.emoji,
                inline=False
            )

            embed.add_field(
                name="Message",
                value=reaction.message.content,
                inline=False
            )

            embed.add_field(
                name="Channel",
                value=reaction.message.channel.mention,
                inline=False
            )

            embed.set_thumbnail(url=user.display_avatar.url)

            await logs.send(embed=embed)
        print(f'{user} removed {reaction.emoji}')
        if user.bot:
            return

        guild = reaction.message.guild

        if not guild:
            return

        if hasattr(self, "colour_role_message_id") and reaction.message.id != self.colour_role_message_id:
            return

        emoji = str(reaction.emoji)

        reaction_role_map = {
            "❤️": "Czerwony",
            "💙": "Niebieski",
            "🩷": "Różowy",
            "💚": "Zielony",
            "💛": "Żółty",
            "🧡": "Pomarańczowy",
        }

        if emoji in reaction_role_map:
            role_name = reaction_role_map[emoji]
            role = discord.utils.get(guild.roles, name=role_name)

            if role and user:
                await user.remove_roles(role)
                print(f"Removed {role} from {user}")

    async def on_member_join(self, member):
        helo = self.get_hello_channel(member.guild)

        role = discord.utils.get(member.guild.roles, name="Nie Zweryfikowany/a")

        if role:
            await member.add_roles(role)
            print(f"Dodano rolę {role} dla {member}")

        if helo:
            embed = discord.Embed(
                title="Członek Dołączył",
                description=f"{member.mention} dołączył do naszej cudownej społeczności",
                color=discord.Color.green()
            )

            embed.set_thumbnail(url=member.display_avatar.url)

            await helo.send(embed=embed)

        logs = self.get_logs_channel(member.guild)

        if logs:
            embed = discord.Embed(
                title="Member Joined",
                description=f"{member.mention} joined the server",
                color=discord.Color.green()
            )

            embed.set_thumbnail(url=member.display_avatar.url)

            await logs.send(embed=embed)

    async def on_member_remove(self, member):

        logs = self.get_logs_channel(member.guild)

        if logs:
            embed = discord.Embed(
                title="Member Left",
                description=f"{member} left the server",
                color=discord.Color.red()
            )

            embed.set_thumbnail(url=member.display_avatar.url)

            await logs.send(embed=embed)

    async def on_message_delete(self, message):

        if message.author.bot:
            return

        logs = self.get_logs_channel(message.guild)

        if logs:
            embed = discord.Embed(
                title="Message Deleted",
                color=discord.Color.red()
            )

            embed.add_field(
                name="Author",
                value=message.author.mention,
                inline=False
            )

            embed.add_field(
                name="Channel",
                value=message.channel.mention,
                inline=False
            )

            embed.add_field(
                name="Message",
                value=message.content,
                inline=False
            )

            embed.set_thumbnail(url=message.author.display_avatar.url)

            await logs.send(embed=embed)

    async def on_message_edit(self, before, after):

        if before.author.bot:
            return

        if before.content == after.content:
            return

        logs = self.get_logs_channel(before.guild)

        if logs:
            embed = discord.Embed(
                title="Message Edited",
                color=discord.Color.orange()
            )

            embed.add_field(
                name="Author",
                value=before.author.mention,
                inline=False
            )

            embed.add_field(
                name="Before",
                value=before.content,
                inline=False
            )

            embed.add_field(
                name="After",
                value=after.content,
                inline=False
            )

            embed.add_field(
                name="Channel",
                value=before.channel.mention,
                inline=False
            )

            embed.set_thumbnail(url=before.author.display_avatar.url)

            await logs.send(embed=embed)

    async def on_voice_state_update(self, member, before, after):

        logs = self.get_logs_channel(member.guild)

        if not logs:
            return

        if before.channel is None and after.channel is not None:

            embed = discord.Embed(
                title="Voice Join",
                description=f"{member.mention} joined {after.channel.mention}",
                color=discord.Color.green()
            )

            embed.set_thumbnail(url=member.display_avatar.url)

            await logs.send(embed=embed)

        elif before.channel is not None and after.channel is None:

            embed = discord.Embed(
                title="Voice Leave",
                description=f"{member.mention} left {before.channel.mention}",
                color=discord.Color.red()
            )

            embed.set_thumbnail(url=member.display_avatar.url)

            await logs.send(embed=embed)

    async def on_member_update(self, before, after):
        wsparcie = self.get_boost_channel(after.guild)
        if before.premium_since is None and after.premium_since is not None:
            if wsparcie:
                embed = discord.Embed(
                    title="Dziękujemy za Wsparcie!",
                    description=f"{after.mention} zaczął nas wspierać!",
                    value=str(after.guild.premium_subscription_count),
                    color=discord.Color.blurple()
                )

                embed.set_thumbnail(url=after.display_avatar.url)

                await wsparcie.send(embed=embed)

        logs = self.get_logs_channel(after.guild)

        if not logs:
            return

        added_roles = [
            role for role in after.roles
            if role not in before.roles
        ]

        removed_roles = [
            role for role in before.roles
            if role not in after.roles
        ]

        for role in added_roles:
            embed = discord.Embed(
                title="Role Added",
                description=f"{after.mention} got role {role.mention}",
                color=discord.Color.blurple()
            )

            await logs.send(embed=embed)

        for role in removed_roles:
            embed = discord.Embed(
                title="Role Removed",
                description=f"{after.mention} lost role {role.mention}",
                color=discord.Color.blurple()
            )

            await logs.send(embed=embed)

    async def on_member_ban(self, guild, user):

        logs = self.get_logs_channel(guild)

        if logs:
            embed = discord.Embed(
                title="Member Banned",
                description=f"{user} was banned",
                color=discord.Color.red()
            )

            await logs.send(embed=embed)

    async def on_member_unban(self, guild, user):

        logs = self.get_logs_channel(guild)

        if logs:
            embed = discord.Embed(
                title="Member Unbanned",
                description=f"{user} was unbanned",
                color=discord.Color.green()
            )

            await logs.send(embed=embed)

    async def on_command(self, ctx):

        logs = self.get_logs_channel(ctx.guild)

        if logs:
            embed = discord.Embed(
                title="Command Executed",
                color=discord.Color.green()
            )

            embed.add_field(
                name="User",
                value=ctx.author.mention,
                inline=False
            )

            embed.add_field(
                name="Command",
                value=ctx.command,
                inline=False
            )

            embed.add_field(
                name="Channel",
                value=ctx.channel.mention,
                inline=False
            )

            await logs.send(embed=embed)




# =========================
# INTENTS
# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True
client = Client(command_prefix="!", intents=intents)

# =========================
# COLORS
# =========================

COLOR_CHOICES = [

    app_commands.Choice(name="Red", value="red"),
    app_commands.Choice(name="Blue", value="blue"),
    app_commands.Choice(name="Green", value="green"),
    app_commands.Choice(name="Yellow", value="yellow"),
    app_commands.Choice(name="Orange", value="orange"),
    app_commands.Choice(name="Purple", value="purple"),
    app_commands.Choice(name="Pink", value="pink"),

    app_commands.Choice(name="Dark Red", value="dark_red"),
    app_commands.Choice(name="Dark Blue", value="dark_blue"),
    app_commands.Choice(name="Dark Green", value="dark_green"),
    app_commands.Choice(name="Dark Purple", value="dark_purple"),
    app_commands.Choice(name="Dark Orange", value="dark_orange"),

    app_commands.Choice(name="Teal", value="teal"),
    app_commands.Choice(name="Dark Teal", value="dark_teal"),

    app_commands.Choice(name="Magenta", value="magenta"),
    app_commands.Choice(name="Dark Magenta", value="dark_magenta"),

    app_commands.Choice(name="Gold", value="gold"),
    app_commands.Choice(name="Dark Gold", value="dark_gold"),

    app_commands.Choice(name="Light Grey", value="light_grey"),
    app_commands.Choice(name="Dark Grey", value="dark_grey"),
    app_commands.Choice(name="Darker Grey", value="darker_grey"),

    app_commands.Choice(name="Blurple", value="blurple"),
    app_commands.Choice(name="Greyple", value="greyple"),

    app_commands.Choice(name="Brand Red", value="brand_red"),
    app_commands.Choice(name="Brand Green", value="brand_green"),

    #app_commands.Choice(name="Random", value="random")
]

COLORS = {

    "red": discord.Color.red(),
    "blue": discord.Color.blue(),
    "green": discord.Color.green(),
    "yellow": discord.Color.yellow(),
    "orange": discord.Color.orange(),
    "purple": discord.Color.purple(),
    "pink": discord.Color.pink(),

    "dark_red": discord.Color.dark_red(),
    "dark_blue": discord.Color.dark_blue(),
    "dark_green": discord.Color.dark_green(),
    "dark_purple": discord.Color.dark_purple(),
    "dark_orange": discord.Color.dark_orange(),

    "teal": discord.Color.teal(),
    "dark_teal": discord.Color.dark_teal(),

    "magenta": discord.Color.magenta(),
    "dark_magenta": discord.Color.dark_magenta(),

    "gold": discord.Color.gold(),
    "dark_gold": discord.Color.dark_gold(),

    "light_grey": discord.Color.light_grey(),
    "dark_grey": discord.Color.dark_grey(),
    "darker_grey": discord.Color.darker_grey(),

    "blurple": discord.Color.blurple(),
    "greyple": discord.Color.greyple(),

    "brand_red": discord.Color.brand_red(),
    "brand_green": discord.Color.brand_green(),

    #"random": discord.Color.random()
}

# =========================
# COMMANDS
# =========================

# Help Center
@client.tree.command(name="help", description="Centrum Pomocy")
async def help(interaction: discord.Interaction):

    embed = discord.Embed(
        title="Centrum Pomocy",
        description="Lista dostępnych komend:",
        color=discord.Color.light_grey(),
    )
    embed.add_field(title="test", value="test", inline=False)

    await interaction.response.send_message(embed=embed)

# Reaction Roles
@client.tree.command(name="colourroles", description="Create a message that lets users pick a colour role", guild=GUILD_ID)
async def colourroles(interaction: discord.Interaction):
    # Check Admin
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    description = (
        "Zareaguj na tą wiadomość aby otrzymać kolorową nazwę!\n\n"
        "❤️ Czerwony\n"
        "💙 Niebieski\n"
        "🩷 Różowy\n"
        "💚 Zielony\n"
        "💛 Żółty\n"
        "🧡 Pomarańczowy\n"
    )

    embed = discord.Embed(
        title="Wybierz swój kolor!",
        description=description,
        color=discord.Color.pink(),
    )

    message = await interaction.channel.send(embed=embed)

    emojis = [ "❤️", "💙", "🩷", "💚", "💛", "🧡" ]

    for emoji in emojis:
        await message.add_reaction(emoji)

    client.colour_role_message_id = message.id

    await interaction.followup.send("Color role message Created!", ephemeral=True)

@client.tree.command(name="verify", description="Verify message", guild=GUILD_ID)
async def verify(interaction: discord.Interaction):
    # Check Admin
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    description = (
        "Zareaguj na tą wiadomość aby się zweryfikować!\n"
        "Weryfikując się automatycznie zgadzasz się na warunki regulaminu"
        #"✅"
    )

    embed = discord.Embed(
        title="Weryfikacja",
        description=description,
        color=discord.Color.brand_green(),
    )

    message = await interaction.channel.send(embed=embed)

    emojis = ["✅"]

    for emoji in emojis:
        await message.add_reaction(emoji)

    client.verify_message_id = message.id

    await interaction.followup.send("Color role message Created!", ephemeral=True)

# Clear Command
@client.tree.command(name="clear", description="Clears messages", guild=GUILD_ID)
async def clear(interaction: discord.Interaction, num_messages: str):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "You don't have permission to use this command",
            ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True)

    # jeśli wpiszesz "*"
    if num_messages == "*":
        deleted = await interaction.channel.purge(limit=None)
        await interaction.followup.send(
            f"Deleted all messages in this channel",
            ephemeral=True
        )
        return

    # normalny tryb (liczba)
    if not num_messages.isdigit():
        await interaction.followup.send(
            "Podaj liczbę albo *",
            ephemeral=True
        )
        return

    deleted = await interaction.channel.purge(limit=int(num_messages))

    await interaction.followup.send(
        f"Deleted {len(deleted)} messages",
        ephemeral=True
    )

# Send Embeded Message Command
@client.tree.command(name="embed", description="Create embed message", guild=GUILD_ID)
@app_commands.choices(color=COLOR_CHOICES)
async def embed(interaction: discord.Interaction, title: str, description: str, field_title: str, field_content: str, footer: str, color: app_commands.Choice[str]):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)
        return
    embed = discord.Embed(
        title=title,
        description=description,
        color=COLORS[color.value]
    )

    embed.set_footer(text=footer)
    embed.add_field(name=field_title, value=field_content)
    # inline=True
    # puts fields next to each other
    #
    # inline=False
    # puts field on a new line (full width)

    embed.set_author(name=str(interaction.user), icon_url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=embed)

client.run(TOKEN)
