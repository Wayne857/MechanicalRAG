from utils.Agent import Agent
from utils.normalUtils import printMessage, printNodeLink


class workFlow:
    """
    该类用于定义工作流
    """

    def __init__(self):
        self.AgentNode = dict()
        self.AssigmentCounter = 0
        self.outerMem = None
        self.AssignmentAgent = None

    def addAgentNode(self, AgentName, llmName):
        self.AgentNode[self.AssigmentCounter] = Agent(AgentName, llmName)

    def addAgentEdge(self, startNode, endNode):
        question = startNode.globalMemory
        endNode.getResponse(question)

    def addAssigmentAgent(self, AssignmentAgent: Agent):
        self.AssignmentAgent = AssignmentAgent

    def autoGenAgent(self):
        startAgent = self.AssignmentAgent
        for i in range(int(startAgent.globalMemory[-3])):
            self.AssigmentCounter = f"{i}"
            self.addAgentNode("continue", "qwq-32b-preview")
            endAgent = self.AgentNode[self.AssigmentCounter]
            printMessage(endAgent)
            self.addAgentEdge(startAgent, endAgent)
            printNodeLink(startAgent, endAgent)
            startAgent = self.AgentNode[self.AssigmentCounter]
        self.AgentNode["FinalRes"] = Agent("FinalRes", "qwq-32b-preview")
        self.addAgentEdge(startAgent, self.AgentNode["FinalRes"])
        printNodeLink(startAgent, self.AgentNode["FinalRes"])
        return self.AgentNode["FinalRes"].getGraphResponse

    def run(self):
        for element in self.autoGenAgent():
            print(element)
        # print(self.autoGenAgent())
