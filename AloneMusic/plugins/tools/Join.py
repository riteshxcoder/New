import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait

from AloneMusic.core.call import Alone
from AloneMusic.utils.database import group_assistant
from AloneMusic import app

# Cache for tracking VC members
VC_CACHE = {}
VC_MONITOR_TASKS = {}


async def monitor_vc_changes(chat_id: int):
    """Background task to monitor voice chat joins/leaves."""
    try:
        assistant = await group_assistant(Alone, chat_id)
        if not assistant:
            return

        # Initial state
        try:
            participants = await assistant.get_participants(chat_id)
        except Exception:
            return
        VC_CACHE[chat_id] = set(p.user_id for p in participants)

        # Loop forever
        while True:
            await asyncio.sleep(5)

            try:
                participants = await assistant.get_participants(chat_id)
            except Exception:
                continue

            current_ids = set(p.user_id for p in participants)
            old_ids = VC_CACHE.get(chat_id, set())
            VC_CACHE[chat_id] = current_ids

            joined = current_ids - old_ids
            left = old_ids - current_ids

            messages = []

            for user_id in joined:
                try:
                    user = await app.get_users(user_id)
                    name = user.mention if user else f"<code>{user_id}</code>"
                except Exception:
                    name = f"<code>{user_id}</code>"
                messages.append(f"✅ <b>Joined VC:</b> {name}")

            for user_id in left:
                try:
                    user = await app.get_users(user_id)
                    name = user.mention if user else f"<code>{user_id}</code>"
                except Exception:
                    name = f"<code>{user_id}</code>"
                messages.append(f"❌ <b>Left VC:</b> {name}")

            if messages:
                text = "\n".join(messages)
                try:
                    msg = await app.send_message(chat_id, text)
                    await asyncio.sleep(20)
                    await msg.delete()
                except FloodWait as fw:
                    await asyncio.sleep(fw.value)
                except Exception:
                    pass

    except Exception:
        pass
    finally:
        VC_CACHE.pop(chat_id, None)
        VC_MONITOR_TASKS.pop(chat_id, None)


async def start_vc_logger(chat_id: int):
    """Start monitoring VC for a group."""
    if chat_id not in VC_MONITOR_TASKS:
        task = asyncio.create_task(monitor_vc_changes(chat_id))
        VC_MONITOR_TASKS[chat_id] = task
