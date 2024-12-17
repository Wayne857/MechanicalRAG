import os
import time

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from sentence_transformers import SentenceTransformer
from pathlib import Path
from utils.dataProcess import createChromaDB


def searchDoc(llm, system_prompt):
    # startTime = time.time()
    current_directory_path = Path(__file__).parent.resolve()
    path = os.path.join(current_directory_path, "docs")
    retriever = createChromaDB(path, current_directory_path)

    llm = ChatOpenAI(
        model='qwq-32b-preview',
        temperature=0,
        openai_api_key="sk-371c7d0cd5df4f788fff6e0d46863188",
        openai_api_base='https://dashscope.aliyuncs.com/compatible-mode/v1',
    )

    system_prompt = (
        """
        你是一个优秀的机械工程师，精通各种机械加工工艺，尤其是车削加工和铣削加工；
        不要回答与你的专业无关的问题，只回答与机械加工有关的问题；
        对于不知道的问题，可以回答“不知道”。
        {context}
        """

    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    # agent = create_react_agent(models, tools, prompt)
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    # question_answer_chain = create_stuff_documents_chain(llm)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    results = rag_chain.invoke({"input": "我想用原料车一个阶梯轴，需要哪几个工序？将结果组装成一个json"})

    # print(results["context"][0].page_content)
    print(results["answer"])
