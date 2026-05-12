import os, json
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
import config_data as config


def get_history(session_id):
    return FileChatMessageHistory(session_id,config.history_path)

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,path):
        self.session_id = session_id
        self.path = path
        self.file_path = os.path.join(self.path, self.session_id)
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    def add_messages(self, message) -> None:
        all_messages = list(self.messages)
        all_messages.extend(message)
        new_messages = [message_to_dict(message) for message in all_messages]
        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump(new_messages, f)

    @property
    def messages(self)-> list[BaseMessage]:
        try:
            with open(self.file_path,'r',encoding='utf-8') as f:
                json_data = json.load(f)
                return messages_from_dict(json_data)
        except FileNotFoundError:
            return []

    def clear(self)->None:
        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump([], f)