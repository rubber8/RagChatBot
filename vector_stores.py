from langchain_chroma import Chroma
import config_data as config


class VectorStoreService(object):
    """
    提供向量搜索接口，一切为了入链
    """
    def __init__(self,embedding):
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs = {'k':config.similarity_threshold})

if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings
    vss = VectorStoreService(DashScopeEmbeddings(model = 'text-embedding-v4')).get_retriever()
    res = vss.invoke("我喜欢宽松的衣服")
    print(res[0].page_content)