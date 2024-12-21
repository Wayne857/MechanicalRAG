import os
from pathlib import Path
import dashscope
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from utils.dataProcess import read_yaml_file_paths, createChromaDB
from utils.prompt import Prompt


class Agent:

    def __init__(self, AgentName, llmName):
        self.getGraphResponse = []
        self.initAgentPrompt = None
        self.llm = None
        self.llmName = llmName  #llmName是模型的型号
        self.AgentName = AgentName
        self.promptFull = " "
        self.globalMemory = " "
        self.img = None
        self.api_key = read_yaml_file_paths("./config/config.yaml")[0]

    def getPrompt(self):
        self.initAgentPrompt = Prompt.prompt[self.AgentName]

    def getMessage(self, question):
        self.getPrompt()

        if self.img:
            imgPackeg = [{"image": singleImg} for singleImg in self.img]
            text = {"text": self.promptMix(self.initAgentPrompt)}
            messages = [
                {
                    "role": "user",
                    "content": [
                    ]
                }
            ]
            messages[0]["content"].extend(imgPackeg)
            messages[0]["content"].append(text)
        else:
            docMessage = "文档查询结果：" + self.searchDoc("查询与" + question + "有关的内容") + "文档查询结果结束"
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"text": docMessage + self.promptMix(self.initAgentPrompt)}
                    ]
                }
            ]
        return messages

    def promptMix(self, initAgentPrompt):
        self.promptFull = self.globalMemory + initAgentPrompt
        return self.promptFull

    def getResponse(self, question):

        messages = self.getMessage(question)
        # print([element["text"] for element in messages[0]["content"] if "text" in element][0])
        # print(text_content))
        # print(messages)

        if not self.img:
            messages[0]["content"][0]["text"] += question
            self.llm = dashscope.Generation.call(
                api_key=self.api_key,
                model=self.llmName,
                messages=messages
            )
            self.getGraphResponse = self.llm["output"]['text'].split('\n')
        else:
            keytext = [element["text"] for element in messages[0]["content"] if "text" in element][0]
            keytext += question
            for element in messages[0]["content"]:
                if "text" in element:
                    element["text"] = keytext
            self.llm = dashscope.MultiModalConversation.call(
                api_key=self.api_key,
                model=self.llmName,
                messages=messages
            )
            self.getGraphResponse = self.llm["output"]['choices'][0]['message']['content'][0]['text'].split('\n')

        self.globalMemory = ''.join(self.getGraphResponse)
        # print(''.join(self.getGraphResponse))
        return self.getGraphResponse

    def printResponse(self):
        for element in self.getGraphResponse:
            print(element)

    def searchDoc(self, question):
        # startTime = time.time()
        # current_directory_path = Path(__file__).parent.resolve()[:-5]+'PDF'
        current_directory_path = str(Path(__file__).parent.resolve())[:-5] + 'PDF'
        # print(str(current_directory_path))
        path = os.path.join(current_directory_path, "docs")
        retriever = createChromaDB(path, current_directory_path)

        llm = ChatOpenAI(
            model=self.llmName,
            temperature=0,
            openai_api_key=self.api_key,
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

        results = rag_chain.invoke({"input": question})
        # print(results["answer"])
        return results["answer"]
