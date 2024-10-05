from disnake import MessageInteraction

from modules.generators import EmbedGenerator
from modules.redis import PrivateChannels, Users
from modules.managers import LanguageManager
from modules.decorators import click_timeout

from utils.modals import ModalChangeLimit, ModalChangeName
from utils.menus import MenuViewKickUser, MenuViewGetOwner, MenuViewMuteUser, MenuViewUserAccess


@click_timeout(timeout_duration=3)
async def change_name(inter: MessageInteraction, language: LanguageManager):
    private_channel = await check_and_get_private(inter=inter, language=language)
    if not private_channel:
        return

    await inter.response.send_modal(ModalChangeName(language=language))


@click_timeout(timeout_duration=3)
async def new_limit(inter: MessageInteraction, language: LanguageManager):
    private_channel = await check_and_get_private(inter=inter, language=language)
    if not private_channel:
        return

    await inter.response.send_modal(ModalChangeLimit(language=language))


@click_timeout(timeout_duration=3)
async def user_access(inter: MessageInteraction, language: LanguageManager):
    private_channel = await check_and_get_private(inter=inter, language=language)
    if not private_channel:
        return

    response = language.get_embed_data('user_access_response')
    view = MenuViewUserAccess(channel_id=inter.author.voice.channel.id, language=language)

    await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True, view=view)


@click_timeout(timeout_duration=3)
async def open_close_room(inter: MessageInteraction, language: LanguageManager):
    private_channel = await check_and_get_private(inter=inter, language=language)
    if not private_channel:
        return

    overwrite = inter.author.voice.channel.overwrites_for(inter.guild.default_role)
    if overwrite.connect is None:
        response = language.get_embed_data('close_room_response')
        overwrite.connect = False
    else:
        response = language.get_embed_data('open_room_response')
        overwrite.connect = None

    user = Users(key=inter.author.id)
    user.private_close = overwrite.connect
    await user.save()

    await inter.author.voice.channel.set_permissions(target=inter.guild.default_role, overwrite=overwrite)
    await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)


@click_timeout(timeout_duration=3)
async def hide_show_room(inter: MessageInteraction, language: LanguageManager):
    private_channel = await check_and_get_private(inter=inter, language=language)
    if not private_channel:
        return

    overwrite = inter.author.voice.channel.overwrites_for(inter.guild.default_role)
    if overwrite.view_channel is None:
        response = language.get_embed_data('hide_room_response')
        overwrite.view_channel = False
    else:
        response = language.get_embed_data('show_room_response')
        overwrite.view_channel = None

    user = Users(key=inter.author.id)
    user.private_hide = overwrite.view_channel
    await user.save()

    await inter.author.voice.channel.set_permissions(target=inter.guild.default_role, overwrite=overwrite)
    await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)


@click_timeout(timeout_duration=3)
async def mute_user(inter: MessageInteraction, language: LanguageManager):
    private_channel = await check_and_get_private(inter=inter, language=language)
    if not private_channel:
        return

    response = language.get_embed_data('mute_user_response')
    view = MenuViewMuteUser(channel_id=inter.author.voice.channel.id, language=language)

    await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True, view=view)


@click_timeout(timeout_duration=3)
async def kick_user(inter: MessageInteraction, language: LanguageManager):
    private_channel = await check_and_get_private(inter=inter, language=language)
    if not private_channel:
        return

    response = language.get_embed_data('kick_user_response')
    view = MenuViewKickUser(channel_id=inter.author.voice.channel.id, language=language)

    await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True, view=view)


@click_timeout(timeout_duration=3)
async def get_owner(inter: MessageInteraction, language: LanguageManager):
    private_channel = await check_and_get_private(inter=inter, language=language)
    if not private_channel:
        return

    response = language.get_embed_data('get_owner_response')
    view = MenuViewGetOwner(channel_id=inter.author.voice.channel.id, language=language)

    await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True, view=view)


@click_timeout(timeout_duration=3)
async def clear_setting(inter: MessageInteraction, language: LanguageManager):
    private_channel = await check_and_get_private(inter=inter, language=language)
    if not private_channel:
        return

    user = Users(key=inter.author.id)
    await user.delete()

    overwrite = inter.author.voice.channel.overwrites_for(inter.guild.default_role)
    overwrite.connect = None
    overwrite.view_channel = None
    await inter.author.voice.channel.set_permissions(target=inter.guild.default_role, overwrite=overwrite)
    await inter.author.voice.channel.edit(user_limit=None)

    response = language.get_embed_data('clear_setting_response')
    await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)


@click_timeout(timeout_duration=3)
async def mute_all_user(inter: MessageInteraction, language: LanguageManager):
    private_channel = await check_and_get_private(inter=inter, language=language)
    if not private_channel:
        return

    overwrite = inter.author.voice.channel.overwrites_for(inter.guild.default_role)
    overwrite_owner = inter.author.voice.channel.overwrites_for(inter.author)
    if overwrite.speak is False:
        overwrite.speak = None
        overwrite_owner.speak = None
        response = language.get_embed_data('unmute_all_user_response')
    else:
        overwrite.speak = False
        overwrite_owner.speak = True
        response = language.get_embed_data('mute_all_user_response')

    await inter.author.voice.channel.set_permissions(target=inter.author, overwrite=overwrite_owner)
    await inter.author.voice.channel.set_permissions(target=inter.guild.default_role, overwrite=overwrite)

    for member in inter.author.voice.channel.members:
        if member.id == inter.author.id:
            continue
        await member.move_to(member.voice.channel)

    user = Users(key=inter.author.id)
    user.private_mute_all = overwrite.speak
    await user.save()

    await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)


async def check_and_get_private(inter: MessageInteraction, language: LanguageManager) -> PrivateChannels | None:
    error_not_in_voice, error_not_in_private, error_not_is_owner = language.get_embed_data([
        'error_private_not_in_voice',
        'error_private_not_in_private',
        'error_channel_not_is_owner'
    ])

    if not inter.author.voice:
        await inter.response.send_message(embed=EmbedGenerator(json_schema=error_not_in_voice), ephemeral=True)
        return

    private_channel = PrivateChannels(key=inter.author.voice.channel.id)
    if not await private_channel.load():
        await inter.response.send_message(embed=EmbedGenerator(json_schema=error_not_in_private), ephemeral=True)
        return

    if private_channel.owner_id != inter.author.id:
        await inter.response.send_message(embed=EmbedGenerator(json_schema=error_not_is_owner), ephemeral=True)
        return

    return private_channel
