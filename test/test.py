from utils.Agent import Agent
from utils.prompt import Prompt

agent_2 = Agent("inputAnalysis", "qwen-vl-max")
agent_2.img = ["/Users/404jinggao/Desktop/LLM/MechanicalRAG/PDF/imgs/originIron.jpg",
               "/Users/404jinggao/Desktop/LLM/MechanicalRAG/PDF/imgs/processedIron.jpg"]
agent_2.getResponse("图一是原料，图二是加工后的产品，材料是45号钢")
agent_2.printResponse()

question = agent_2.globalMemory
agent_1 = Agent("test", "qwq-32b-preview")

agent_1.getResponse(question)
agent_1.printResponse()

agent_3 = Agent("COT", "qwq-32b-preview")
question = agent_1.globalMemory
agent_3.getResponse(question+"输出第一个工序的每一个详细工步，包括刀具选型、切削参数、工序顺序等详细参数")
agent_3.printResponse()


