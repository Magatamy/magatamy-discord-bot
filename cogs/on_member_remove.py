from disnake.ext import commands
from disnake import AuditLogAction, Member
from datetime import datetime

from modules.database import AntiNukeTable, UsersTable


class OnReady(commands.Cog):
    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        guild = member.guild
        time_now = datetime.utcnow()

        anti_nuke = AntiNukeTable(guild_id=guild.id)
        await anti_nuke.load()
        limit = anti_nuke.ban_protection_count * 5
        
        async for entry in guild.audit_logs(action=AuditLogAction.ban, user=member, limit=limit):
            if entry.target == member and (time_now - entry.created_at).total_seconds() < 10:
                print(f"{member} был забанен {entry.user}")


                break


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnReady(client))
