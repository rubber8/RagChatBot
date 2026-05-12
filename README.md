# RagChatBot

A RAG-based intelligent Q&A assistant with a freely interchangeable knowledge base — built on LangChain + TongYi QianWen. Simply upload your .txt documents to switch to any Q&A domain.

---

## Environment Setup
We suggest the following Python and LangChain versions:
```
Python --> 3.10.20
LangChain --> 1.2.13
```
And you need an Aliyun DashScope API Key [Get it here](https://dashscope.console.aliyun.com/)

---

## QuickStart
###### 1. Install dependencies
```
pip install -r requirements.txt
```
###### 2. Configure API Key
**Windows:**
```
set DASHSCOPE_API_KEY = YOUR_API_KEY
```
**Linux/Mac:**
```
export DASHSCOPE_API_KEY = YOUR_API_KEY
```
###### 3. Start Q&A
```
streamlit run app_qa.py
```

---

## Notes
1. There is no need to manually create folders for this project.
2. Relevant configurations can be modified in `./config_data.py`
3. If you want to switch the database, first clear:
```
├── data/               # Stores knowledge documents
├── chroma_db/          # Vector database
└── history/            # User conversation history
```
Then upload files (only `.txt` files) to `./data`

