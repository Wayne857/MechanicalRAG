from utils.Agent import Agent
from utils.workFlow import workFlow


def main():
    agent_1 = Agent("inputAnalysis", "qwen-vl-max")
    agent_1.img = ["/Users/404jinggao/Desktop/LLM/MechanicalRAG/PDF/imgs/originIron.jpg",
                   "/Users/404jinggao/Desktop/LLM/MechanicalRAG/PDF/imgs/processedIron.jpg"]
    agent_1.getResponse("图一是原料，直径为50长度为300，图二是加工后的产品，材料是45号钢")
    # agent_1.printResponse()
    # print("------------------------------------------------>")

    question = agent_1.globalMemory
    agent_2 = Agent("COT", "qwq-32b-preview")
    agent_2.getResponse(question)
    # agent_2.printResponse()
    # print("------------------------------------------------>")
    # print(agent_2.globalMemory[-3])

    workFlow_ = workFlow()
    workFlow_.addAssigmentAgent(AssignmentAgent=agent_2)
    workFlow_.run()


if __name__ == '__main__':
    main()
