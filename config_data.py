md5_path = './md5.txt'
chroma_path = './chroma_db'
collection_name = 'rag'
persist_directory = './chroma_db'
history_path  = './history'

chunk_size = 1000
chunk_overlap = 100
separators = ['\n\n','\n','.','。','!']
max_spliter_str_number = 1000

similarity_threshold = 2

chat_model = 'qwen3-max'
embedding_model = 'text-embedding-v4'

session_config = {
        'configurable':{
            'session_id':'user_001',
        }
    }