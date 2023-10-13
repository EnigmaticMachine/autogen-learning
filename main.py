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

assistant = autogen.AssistantAgent(
    name="CTO",
    llm_config=llm_config,
    system_message="Chief technical officer of a tech company. Interact with system through python scripts to done tasks",
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web", "use_docker": False},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
)

# task = """
# Write basic api with FastAPI. Add two endpoints /hello which is get request to respond 'hello there!' and /bye to respond 'go..'
# """

task = """
Make and save a bash script to Create this project structure inside our root work_dir:
project_directory/
|-- app/
    |-- __init__.py
    |-- main.py
|-- tests/
    |-- test_main.py
|-- .gitignore
|-- requirements.txt
|-- README.md
"""


user_proxy.initiate_chat(assistant, message=task)

task = """
Make simple fastapi app and save it here:
project_directory/
|-- app/
    |-- main.py

"""


user_proxy.initiate_chat(assistant, message=task)


# task2 = """
# Change the code in the file test1.py you just created to output numbers 1 to 200
# """

# user_proxy.initiate_chat(assistant, message=task2)

# task2 = """
# Change the code in the file test1.py you just created to output numbers 111 to 131
# """

# user_proxy.initiate_chat(assistant, message=task2)
