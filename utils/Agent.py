import os
import dashscope
from utils.dataProcess import read_yaml_file_paths
from utils.prompt import Prompt


class Agent:

    def __init__(self, AgentName, llmName):
        self.initAgentPrompt = None
        self.llm = None
        self.llmName = llmName  #llmName是模型的型号
        self.AgentName = AgentName
        self.promptFull = " "
        self.globalMemory = " "
        self.img = None

    def getPrompt(self):
        self.initAgentPrompt = Prompt.prompt[self.AgentName]

    def getMessage(self):
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
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"text": self.promptMix(self.initAgentPrompt)}
                    ]
                }
            ]
        return messages

    def promptMix(self, initAgentPrompt):
        self.promptFull = self.globalMemory + initAgentPrompt
        return self.promptFull

    def getResponse(self, question):
        messages = self.getMessage()
        # print([element["text"] for element in messages[0]["content"] if "text" in element][0])
        # print(text_content))
        # print(messages)
        api_key = read_yaml_file_paths("../config/config.yaml")[0]
        if not self.img:
            messages[0]["content"][0]["text"] += question
            self.llm = dashscope.Generation.call(
                api_key=api_key,
                model=self.llmName,
                messages=messages
            )
            getGraphResponse = self.llm["output"]['text'].split('\n')
        else:
            keytext = [element["text"] for element in messages[0]["content"] if "text" in element][0]
            keytext += question
            for element in messages[0]["content"]:
                if "text" in element:
                    element["text"] = keytext
            self.llm = dashscope.MultiModalConversation.call(
                api_key=api_key,
                model=self.llmName,
                messages=messages
            )
            getGraphResponse = self.llm["output"]['choices'][0]['message']['content'][0]['text'].split('\n')
        print(''.join(getGraphResponse))
        return ''.join(getGraphResponse)
