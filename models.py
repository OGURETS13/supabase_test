import inspect
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


class Chat:
    def __init__(self, chat_id, created_at, role):
        self.chat_id = chat_id
        self.created_at = created_at
        self.role = role

    def __repr__(self):
        return f"Chat(chat_id={self.chat_id}, created_at={self.created_at}, role={self.role})"


class Thread:
    def __init__(self, thread_id, chat_id, created_at, status):
        self.chat_id = chat_id
        self.created_at = created_at
        self.status = status
        self.thread_id = thread_id

    def __repr__(self):
        return f"Thread(chat_id={self.chat_id}, created_at={self.created_at}, status={self.status}, thread_id={self.thread_id})"


class Message:
    def __init__(
        self, chat_id, created_at, role, id, thread_id, text, original_message
    ):
        self.chat_id = chat_id
        self.created_at = created_at
        self.role = role
        self.thread_id = thread_id
        self.id = id
        self.text = text
        self.original_message = original_message

    def __repr__(self):
        return f"Message(chat_id={self.chat_id}, created_at={self.created_at}, role={self.role}, thread_id={self.thread_id}, id={self.id}, text={self.text}, original_message={self.original_message})"


def create_instance(cls, data):
    """
    Creates an instance of a given class and populates it with data from a dictionary.

    Parameters:
        cls (type): The class to instantiate.
        data (dict): A dictionary containing the data to populate the class with.

    Returns:
        An instance of the specified class populated with the provided data.
    """
    if not data:
        return None

    # Get the parameters of the class's __init__ method
    params = inspect.signature(cls).parameters

    # Filter the data dictionary to only include keys that match the class's __init__ parameters
    filtered_data = {key: value for key, value in data.items() if key in params}

    # Create an instance of the class with the filtered data
    instance = cls(**filtered_data)
    return instance
