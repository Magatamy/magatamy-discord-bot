from disnake import ModalInteraction
from asyncio import wait_for, TimeoutError

from modules.redis import Users
from modules.generators import EmbedGenerator
from modules.managers import LanguageManager, ErrorManager
from modules.enums import ModalInputID


async def change_name(inter: ModalInteraction, language: LanguageManager):
    new_name = inter.text_values.get(ModalInputID.CHANGE_NAME.value)
    try:
        await wait_for(inter.author.voice.channel.edit(name=new_name), timeout=1.5)
    except TimeoutError as error:
        await ErrorManager.error_handle(inter=inter, error=error)
        return

    user = Users(key=inter.author.id)
    user.private_name = new_name
    await user.save()

    response = language.get_embed_data('change_name_response')
    await inter.response.send_message(embed=EmbedGenerator(json_schema=response, name=new_name), ephemeral=True)


async def change_limit(inter: ModalInteraction, language: LanguageManager):
    new_limit = inter.text_values.get(ModalInputID.CHANGE_LIMIT.value)

    if not new_limit.isdigit() or not (0 <= int(new_limit) <= 99):
        response = language.get_embed_data('error_change_limit_value')
    else:
        await inter.author.voice.channel.edit(user_limit=new_limit)
        response = language.get_embed_data('change_limit_response')

        user = Users(key=inter.author.id)
        user.private_limit = new_limit
        await user.save()

    await inter.response.send_message(embed=EmbedGenerator(json_schema=response, limit=new_limit), ephemeral=True)
