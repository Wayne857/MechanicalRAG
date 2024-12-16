from utils.Agent import Agent
from utils.prompt import Prompt

agent_1 = Agent("test", "qwq-32b-preview")

agent_1.getResponse("铣削加工要注意什么？")


agent_2 = Agent("test", "qwen-vl-max")
agent_2.img = ["/Users/404jinggao/Desktop/LLM/MechanicalRAG/PDF/imgs/originIron.jpg",
               "/Users/404jinggao/Desktop/LLM/MechanicalRAG/PDF/imgs/processedIron.jpg"]
agent_2.getResponse("讲一下这两个图？")
