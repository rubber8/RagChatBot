from langchain_community.chat_models import ChatTongyi
from langchain_community.docstore import document
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
import config_data as config
from vector_stores import VectorStoreService
from file_history_store import get_history
import os


def pprint(prompt):
    print('='*10,'\n')
    print(prompt.to_string())
    print('='*10,'\n')
    return prompt

class RagService(object):
    def __init__(self):
        self.template_prompt = ChatPromptTemplate.from_messages(
            [
                ('system','请根据提供的资料:\n{reference}\n'),
                ('system', '以及用户的对话历史:\n{history}\n'),
                ('user','简洁地回答如下问题:{input}\n')
            ]
        )
        self.model = ChatTongyi(model = config.chat_model)

        self.retriever = VectorStoreService(embedding = DashScopeEmbeddings(model = config.embedding_model)
                                            ).get_retriever()
        self.chain = self.__get_chain()


    def __get_chain(self):

        def format_str(docs:list[document]) -> str:
            if not docs:
                return '无参考资料'
            formatted_docs = ""
            for doc in docs:
                formatted_docs += f"content:{doc.page_content}; metadata:{doc.metadata} \n\n"
            return formatted_docs
        def format_2_retriever(value)->str:
            return value['input']
        def format_2_template_prompt(value):
            new_value = {}
            new_value['input'] = value['input']['input']
            new_value['history'] = value['input']['history']
            new_value['reference'] = value['reference']
            return new_value

        chain = ({'input':RunnablePassthrough(), 'reference': RunnableLambda(format_2_retriever) |
                 self.retriever| format_str } | RunnableLambda(format_2_template_prompt) |
                 self.template_prompt | pprint | self.model | StrOutputParser())

        new_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key='input',
            history_messages_key='history',
        )
        return new_chain

if __name__ == '__main__':
    session_config = {
        'configurable':{
            'session_id':'user_001',
        }
    }
    res = RagService().chain.invoke({"input":"我身高170,给我推荐衣服尺码"}, session_config)
    print(res)