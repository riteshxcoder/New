from pyrogram import filters
from pyrogram.types import Message


async def check_admin(client, message: Message) -> bool:
    """Check if the user is admin/creator in the group."""
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status in ("administrator", "creator"):
            return True
        return False
    except Exception:
        return False


# Custom filter for admin-only commands
admin_filter = filters.create(lambda _, __, message: check_admin(_, message))


# Backward compatibility (in case of old imports)
AdminRightsCheck = admin_filter
