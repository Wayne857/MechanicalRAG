import json
import os
import time
from pathlib import Path
import dashscope
from openai import OpenAI

startTime = time.time()

messages = [
    {
        "role": "user",
        "content": [
            {"image": r"D:\pyCode\PCB_GraphLLM\PDF\1.png"},
            # {"image": r"D:\pyCode\PCB_GraphLLM\PDF\2.png"},
            {"text": "分别详细描述一下图中表格各个封装的引脚，包括引脚编号、引脚名称和引脚描述"}
        ]
    }
]
response = dashscope.MultiModalConversation.call(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen-vl-max',
    messages=messages
)
# text = json.loads(response.model_dump_json())
getText = response["output"]['choices'][0]['message']['content'][0]['text'].split('\n')
# print(getText[:])
messages = [
    {
        "role": "user",
        "content": [
            {"image": r"D:\pyCode\PCB_GraphLLM\PDF\2.png"},
            {"text": "输出每个电路图的详细引脚连接，说明引脚的连接情况同时识别电容、电阻等器件，详细描述该器件与引脚的连接关系"
             }
        ]
    }
]
graphResponse = dashscope.MultiModalConversation.call(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen-vl-max',
    messages=messages
)
getGraphResponse = graphResponse["output"]['choices'][0]['message']['content'][0]['text'].split('\n')

messages = [
    {
        "role": "user",
        "content": [
            {"text": ' '.join(getText) + ' '.join(getGraphResponse) +
                     "根据上述内容，将每个引脚的编号一一对应。"
                     "请输出电路图中的引脚连接关系，详细描述引脚与器件的连接关系"
                     "每一个电路图的输出格式例如："
                     "{"
                     "### ADP122 with Fixed Output Voltage (TSOT Version)"
                     "**VIN (1)**: 调节器输入电源。通过至少1μF的电容将VIN连接到GND。"
                     "**GND (2)**: 接地。"
                     "**EN (3)**: 使能输入。将EN驱动为高电平以开启调节器；将EN驱动为低电平以关闭调节器。对于自动启动，将EN连接到VIN。"
                     "**NC (4)**: 无连接。这些引脚未内部连接。它们可以悬空或连接到地。"
                     "**VOUT (5)**: 调节输出电压。通过至少1μF的电容将VOUT连接到GND。"
                     "其他器件连接方式：（若有）"
                     "电阻(R1): 与XX引脚和XX引脚连接"
                     "电容(C1): 与XX引脚和XX引脚连接"
                     "......}"}
        ]
    }
]

TotalResponse = dashscope.MultiModalConversation.call(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen-vl-max',
    messages=messages
)
getTotalResponse = TotalResponse["output"]['choices'][0]['message']['content'][0]['text'].split('\n')
# for i in getTotalResponse:
#     print(i)
#
# print('-------------------')


client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
file_object = client.files.create(
    file=Path(r"C:\Users\ZZQ\Desktop\PCB项目\Linear DC-DC Conversion\ADP122AUJZ-3.3-R7 V1\ADP122AUJZ-3.3-R7 V1.pdf"),
    purpose="file-extract")
completion = client.chat.completions.create(
    model="qwen-long",
    messages=[
        {'role': 'system', 'content': f'fileid://{file_object.id}'},
        {'role': 'user',
         'content': '这是一个数据手册，请你首先对整个文档进行概述，然后在输出主要内容。'
                    '其中主要内容里面首先说明命名规则并分别列举出该产品所有型号的封装，'
                    '然后将' + ' '.join(getTotalResponse) + '全部输出' +
                    '然后输出产品特点，包括电气特性、热数据、最大额定值与推荐数值等内容的详细数值信息（把数字都列出来），'
                    '接着输出该产品的应用信息，最后将其他详细信息保存在其他信息目录下，并且内容详尽。'
                    '所有内容不要以表格形式输出。'}
    ]
)
text = json.loads(completion.model_dump_json())
getText = text["choices"][0]['message']['content'].split('\n')

for i in getText:
    print(i)

finalTime = time.time()
print('总共用时：', finalTime - startTime)
