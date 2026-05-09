from dotenv import load_dotenv
from llm_client.llm_client import HelloAgentsLLM
from tools.tool_executor import ToolExecutor
from tools.search import search
from agent.re_act_agent import ReActAgent
from agent.plan_and_solve_agent import PlanAndSolveAgent


# 加载 .env 文件中的环境变量
load_dotenv()

# --- PlanAndSolve使用示例 ---
if __name__ == "__main__":
    try:
        # 1. 初始化LLM客户端
        llmClient = HelloAgentsLLM()

        # 2. 初始化工具执行器并注册工具
        toolExecutor = ToolExecutor()
        search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
        toolExecutor.registerTool("Search", search_description, search)

        # 3. 创建PlanAndSolve智能体实例
        agent = PlanAndSolveAgent(llm_client=llmClient)

        # 4. 运行智能体来回答一个问题
        question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
        agent.run(question)

    except ValueError as e:
        print(e)

# --- ReAct使用示例 ---
# if __name__ == "__main__":
#     try:
#         # 1. 初始化LLM客户端
#         llmClient = HelloAgentsLLM()

#         # 2. 初始化工具执行器并注册工具
#         toolExecutor = ToolExecutor()
#         search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
#         toolExecutor.registerTool("Search", search_description, search)

#         # 3. 创建ReAct智能体实例
#         agent = ReActAgent(llm_client=llmClient, tool_executor=toolExecutor)

#         # 4. 运行智能体来回答一个问题
#         question = "华为手机最新型号是什么？"
#         agent.run(question)

#     except ValueError as e:
#         print(e)


# --- 客户端使用示例 ---
# if __name__ == "__main__":
#     try:
#         llmClient = HelloAgentsLLM()

#         exampleMessages = [
#             {
#                 "role": "system",
#                 "content": "You are a helpful assistant that writes Python code.",
#             },
#             {"role": "user", "content": "写一个快速排序算法"},
#         ]

#         print("--- 调用LLM ---")
#         responseText = llmClient.think(exampleMessages)
#         if responseText:
#             print("\n\n--- 完整模型响应 ---")
#             print(responseText)

#     except ValueError as e:
#         print(e)

# --- 工具初始化与使用示例 ---
# if __name__ == "__main__":
#     # 1. 初始化工具执行器
#     toolExecutor = ToolExecutor()

#     # 2. 注册我们的实战搜索工具
#     search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
#     toolExecutor.registerTool("Search", search_description, search)

#     # 3. 打印可用的工具
#     print("\n--- 可用的工具 ---")
#     print(toolExecutor.getAvailableTools())

#     # 4. 智能体的Action调用，这次我们问一个实时性的问题
#     print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
#     tool_name = "Search"
#     tool_input = "英伟达最新的GPU型号是什么"

#     tool_function = toolExecutor.getTool(tool_name)
#     if tool_function:
#         observation = tool_function(tool_input)
#         print("--- 观察 (Observation) ---")
#         print(observation)
#     else:
#         print(f"错误:未找到名为 '{tool_name}' 的工具。")
