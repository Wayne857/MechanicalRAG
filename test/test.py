from utils.Agent import Agent
from utils.prompt import Prompt

agent_1 = Agent("test", "qwq-32b-preview")

# agent_1.getResponse("铣削加工要注意什么？")
print(agent_1.searchDoc("我想用45号钢原料车一个阶梯轴，需要哪几个工序？将结果组装成一个json"))


# agent_2 = Agent("inputAnalysis", "qwen-vl-max")
# agent_2.img = ["/Users/404jinggao/Desktop/LLM/MechanicalRAG/PDF/imgs/originIron.jpg",
#                "/Users/404jinggao/Desktop/LLM/MechanicalRAG/PDF/imgs/processedIron.jpg"]
# print(agent_2.getResponse("图一是原料，图二是加工后的产品，材料是45号钢"))
