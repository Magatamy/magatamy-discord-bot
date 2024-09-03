from disnake.ext import commands
from disnake import AuditLogAction, Member, Guild
from datetime import datetime, timedelta
from collections import Counter

from modules.managers import LanguageManager
from modules.generators import EmbedGenerator
from modules.database import AntiNukeTable, UsersTable


class OnMemberRemove(commands.Cog):
    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        guild = member.guild
        await self.check_antinuke(guild=guild)

    @staticmethod
    async def check_antinuke(guild: Guild):
        time_now = datetime.utcnow()
        anti_nuke = AntiNukeTable(guild_id=guild.id)
        await anti_nuke.load()

        async def get_audit_entries(action: AuditLogAction, timeout) -> list[Member]:
            time_after = time_now - timedelta(
                hours=timeout.hour,
                minutes=timeout.minute,
                seconds=timeout.second
            )
            clear_time = time_after.replace(tzinfo=None)
            entries = []
            async for entry in guild.audit_logs(action=action, limit=None, after=time_after):
                if entry.created_at.replace(tzinfo=None) >= clear_time:
                    entries.append(entry.user)

            return entries

        users_ban = await get_audit_entries(AuditLogAction.ban, anti_nuke.timeout_for_ban)
        users_kick = await get_audit_entries(AuditLogAction.kick, anti_nuke.timeout_for_kick)

        async def process_users(users: list[Member], protection_count: int, action_key: str):
            counter = Counter(users)
            for user, count in counter.items():
                print(count, protection_count)
                if count >= protection_count:
                    role = guild.get_role(anti_nuke.block_role_id)
                    if role in user.roles:
                        await user.edit(roles=[role])
                        continue

                    await user.edit(roles=[role])

                    log_channel = guild.get_channel(anti_nuke.log_channel_id)
                    language = LanguageManager(locale=guild.preferred_locale)
                    user_response, log = language.get_embed_data(
                        json_key=[action_key, f'{action_key}_log'])

                    await user.send(embed=EmbedGenerator(json_schema=user_response))
                    await log_channel.send(embed=EmbedGenerator(json_schema=log, user=user.name, user_id=user.id))

        await process_users(users_ban, anti_nuke.ban_protection_count, 'anti_nuke_ban_blocked')
        await process_users(users_kick, anti_nuke.kick_protection_count, 'anti_nuke_kick_blocked')


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnMemberRemove(client))
