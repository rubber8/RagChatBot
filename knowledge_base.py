import hashlib
import os

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import datetime

import config_data as config


def md5_check(md5:str)->bool:
    if not os.path.exists(config.md5_path):
        open(config.md5_path,'w',encoding='utf-8').close()
        return False
    with open(config.md5_path,'r',encoding='utf-8') as f:
        for line in f.readlines():
            if md5 == line.strip():
                return True
        return False

def md5_save(md5):
    open(config.md5_path,'a',encoding='utf-8').write(md5+'\n')

def get_string_md5(md5,encoding='utf-8'):
    md5_cod = md5.encode(encoding=encoding)
    hl = hashlib.md5()
    hl.update(md5_cod)
    md5_hex = hl.hexdigest()
    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model = 'text-embedding-v4'),
            persist_directory=config.persist_directory,
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators = config.separators,
            length_function=len,
        )

    def upload_by_str(self,data:str,filename):
        md5_hex = get_string_md5(data)
        if md5_check(md5_hex):
            return '[pass] this message has already existed!'

        metadata = {
            'source': filename,
            'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operator':'Jeffrey'
        }
        if len(data) > config.max_spliter_str_number:
            split_res = self.spliter.split_text(data)
        else:
            split_res = [data]

        self.chroma.add_texts(
            split_res,
            metadatas = [metadata for _ in range(len(split_res))],
        )
        md5_save(md5_hex)
        return '[success] this message has already stored!'


if __name__ == '__main__':
    service = KnowledgeBaseService()
    res = service.upload_by_str('i love you','filename')
    print(res)