# from autogen import AssistantAgent, UserProxyAgent
import autogen
import config as myconfig

config_list = [
    {
        "model": "gpt-3.5-turbo",
        "api_key": myconfig.api_key,
    }
]
# config_list = [{"model": "gpt-4", "api_key": myconfig.api_key}]


llm_config = {
    "request_timeout": 600,
    "seed": 9150,
    "config_list": config_list,
    "temperature": 0,
}


user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "interview", "use_docker": False},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
journalist making an interview with two participants.""",
)

ceo = autogen.AssistantAgent(
    name="CEO",
    llm_config=llm_config,
    system_message="You play a role in game as CEO of big corporate having a scandal about ecological disaster. You're arogant psychopath, manipulative and charming. You need to cover up at all cost. You have magnetic personality that draws people to them, making it easier to sway public opinion and manage the company's image.",
)

ea = autogen.AssistantAgent(
    name="environmental_activist",
    system_message="You're environmental activists. Believe in communism and have mega corporations. You're also snowflake. you need to show that The renewable projects were never completed, and the tree-planting drives were massively exaggerated. Give argumetns to supprt this",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, ea, ceo], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)


task = """
we have a disscussion between CEO  and environmental activists. Lead this 
disscussion and make an interview for newspapper from it. Output is
completed interview.

ask questions one by one and lead discussion:

Question 1:
To the CEO - MegaCorp has been a proponent of eco-friendliness with its Green Mirage initiative. However, recent investigations suggest that the renewable projects were never completed. Could you provide some insight into these allegations?
"""


user_proxy.initiate_chat(manager, message=task)


task = """
Question 2:
To the Environmental Activists - You have claimed that the tree-planting drives were massively exaggerated. Could you share the evidence you have gathered regarding this?
"""

user_proxy.initiate_chat(manager, message=task)

task = """

Question 3:
To the CEO - How does MegaCorp plan to address the discrepancies between its eco-friendly claims and the findings of the environmental activists?
"""

user_proxy.initiate_chat(manager, message=task)

# user_proxy.initiate_chat(assistant, message=task2)

# task2 = """
# Change the code in the file test1.py you just created to output numbers 111 to 131
# """

# user_proxy.initiate_chat(assistant, message=task2)
