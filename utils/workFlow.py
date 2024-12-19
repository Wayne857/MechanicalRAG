from utils.Agent import Agent


class workFlow:
    """
    该类用于定义工作流
    """

    def __init__(self, name, steps):
        self.name = name
        self.AgentNode = dict()
        self.steps = steps

    def addAgentNode(self, AgentName, llmName):
        self.AgentNode[AgentName] = Agent(AgentName, llmName)

    def addEdge(self, start, end):
        startAgent = self.AgentNode[start]
        endAgent = self.AgentNode[end]
        endAgent.getResponse(startAgent.self.globalMemory)

    def run(self):
        for step in self.steps:
            step.run()
