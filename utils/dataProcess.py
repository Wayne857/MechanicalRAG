import os
from uuid import uuid4
from langchain_core.documents import Document
import yaml
from chromadb.utils import embedding_functions
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from modelscope import snapshot_download
from sentence_transformers import SentenceTransformer
from pathlib import Path


def getdir(path) -> list:
    fileName = os.listdir(path)
    fullFileName = []
    for file in fileName:
        fullFileName.append(os.path.join(path, file))
    return fullFileName


# embedding格式转换
class SentenceTransformerEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, documents):
        # 使用 numpy 的 ravel 方法来扁平化嵌入向量数组，然后转换为列表
        embeddings = self.model.encode(documents)
        flat_embeddings = [embedding.ravel().tolist() for embedding in embeddings]
        return flat_embeddings

    def embed_query(self, query):
        # 对于单个查询，同样扁平化数组并转换为列表
        embedding = self.model.encode(query).ravel().tolist()
        return embedding


# 将已经读取的文件写入yaml文件
def writeYamlFile(path, data):
    with open(path, 'a', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)


# 读取yaml文件
def readYaml(path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


# 数据库初始化
def initChromaDB():
    current_directory_path = Path(__file__).parent.resolve()
    current_directory_path = str(current_directory_path)[:-5] + 'models'+'/all-MiniLM-L6-v2'
    model_dir = snapshot_download('AI-ModelScope/all-MiniLM-L6-v2', local_dir=current_directory_path)
    # 创建嵌入函数实例
    embedding_function = SentenceTransformerEmbeddingFunction(model_dir)
    persist_directory = './chroma_db'
    if os.path.exists(persist_directory):
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_function
        )

    else:
        # 创建 Chroma 向量存储，并将数据持久化到指定目录
        vectorstore = Chroma(
            collection_name="example_collection",
            embedding_function=embedding_function,
            persist_directory=persist_directory,  # Where to save data locally, remove if not necessary
        )
    return vectorstore


# 数据库更新
def addDoc2ChromaDB(vectorstore, doc, fileName):
    document = Document(
        page_content=doc,
        metadata={"source": fileName},
        id=10
    )
    documents = [
        document,
    ]
    uuids = [str(uuid4()) for _ in range(len(documents))]
    vectorstore.add_documents(documents=documents, ids=uuids)


# 创建数据库
def createChromaDB(path, current_directory_path):
    #模型下载
    vectorstore = None
    fullFilePath = getdir(path)
    loadedFileDir = os.path.join(current_directory_path, "loadedFile.yaml")
    lodedData = readYaml(loadedFileDir)
    for file_path in fullFilePath:
        print(file_path)
        # if file_path in lodedData or not file_path.endswith('.pdf'):
        #     continue
        # else:
        #     loader = PyPDFLoader(file_path)
        #     docs = loader.load()
        #     text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100, add_start_index=True)
        #     splits = text_splitter.split_documents(docs)
        #     vectorstore = initChromaDB()
        #     addDoc2ChromaDB(vectorstore, splits)
        #     writeYamlFile(loadedFileDir, file_path)
        fileName = file_path.split('/')[-1]
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100, add_start_index=True)
        splits = text_splitter.split_documents(docs)
        vectorstore = initChromaDB()
        addDoc2ChromaDB(vectorstore, splits, fileName)
        writeYamlFile(loadedFileDir, file_path)

    retriever = vectorstore.as_retriever()
    return retriever
