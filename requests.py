import asyncio
from models import Chat, create_instance, Message, supabase, Thread


async def get_chat(chat_id):
    data = (
        supabase.table("chats")
        .select("*")
        .eq("chat_id", chat_id)
        .execute()
    ).data

    if not data:
        supabase.table("chats").insert({"chat_id": chat_id}).execute()
        data = (
            supabase.table("chats")
            .select("*")
            .eq("chat_id", chat_id)
            .execute()
        ).data

    chat = create_instance(Chat, data[0])

    return chat


async def create_thread_obj(chat_id, thread_id):
    await get_chat(chat_id)
    supabase.table("threads").insert(
        {"chat_id": chat_id, "thread_id": thread_id}
        ).execute()


async def get_thread_obj(chat_id):
    data = (
        supabase.table("threads")
        .select("*")  # Select all columns from the Thread table
        .eq("status", "active")  # Filter for active threads
        .eq("chat_id", chat_id)  # Filter for the specific chat_id in the Chat table
        .order("created_at", desc=True)  # Order by created_at in descending order
        .limit(1)  # Limit to one result
        .execute()
        ).data

    if not data:
        return None

    thread_obj = create_instance(Thread, data[0])

    return thread_obj


async def close_thread_obj(chat_id):
    (
        supabase.table("threads")
        .update({"status": "closed"})
        .eq("chat_id", chat_id)
        .eq("status", "active")
        .execute()
    )


async def add_message(chat_id, thread_id, text, role, original_message=None):
    data = (
        supabase.table('messages')
        .insert({
            "chat_id": chat_id,
            "thread_id": thread_id,
            "text": text,
            "role": role,
            "original_message": original_message
        }).execute()
    ).data

    if not data:
        return None

    message = create_instance(Message, data[0])

    return message.id


if __name__ == "__main__":
    asyncio.run(add_message(15, 'f123', 'tulula', 'user'))
