from typing import Optional

import aitools_autogen.utils as utils
from aitools_autogen.agents import WebPageScraperAgent
from aitools_autogen.blueprint import Blueprint
from aitools_autogen.config import llm_config_openai as llm_config, config_list_openai as config_list, WORKING_DIR
from autogen import ConversableAgent

class CoreClientTestBlueprint(Blueprint):

    def __init__(self, work_dir: Optional[str] = WORKING_DIR):
        super().__init__([], config_list=config_list, llm_config=llm_config)
        self._work_dir = work_dir or "code"
        self._summary_result: Optional[str] = None

    @property
    def summary_result(self) -> str | None:
        """The getter for the 'summary_result' attribute."""
        return self._summary_result

    @property
    def work_dir(self) -> str:
        """The getter for the 'work_dir' attribute."""
        return self._work_dir

    async def initiate_work(self, message: str):
        utils.clear_working_dir(self._work_dir)
        agent0 = ConversableAgent("a0",
                                  max_consecutive_auto_reply=0,
                                  llm_config=False,
                                  human_input_mode="NEVER")

        scraper_agent = WebPageScraperAgent()

        summary_agent = ConversableAgent("summary_agent",
                                         max_consecutive_auto_reply=6,
                                         llm_config=llm_config,
                                         human_input_mode="NEVER",
                                         code_execution_config=False,
                                         function_map=None,
                                         system_message="""You are a helpful AI assistant.
        You can summarize OpenAPI specifications.  When given an OpenAPI specification,
        output a summary in bullet point form for each endpoint.
        Let's make it concise in markdown format.
        It should include short descriptions of parameters,
        and list expected possible response status codes.
        Return `None` if the OpenAPI specification is not valid or cannot be summarized.
            """)

        aiohttp_client_agent = ConversableAgent("aiohttp_client_agent",
                                                max_consecutive_auto_reply=6,
                                                llm_config=llm_config,
                                                human_input_mode="NEVER",
                                                code_execution_config=False,
                                                function_map=None,
                                                system_message="""
    You are a data scientist tasked with building a data preprocessing pipeline for a machine learning project. Your goal is to develop a set of functions that preprocess raw data into a format suitable for training machine learning models. Your pipeline should include steps for handling missing values, encoding categorical variables, scaling numerical features, and splitting the data into training and testing sets.

When you receive a message, it will contain information about the raw dataset, including its structure and any preprocessing requirements specified by the user.

Your task is to generate Python code that implements the data preprocessing pipeline.

The code should consist of multiple modular functions, each responsible for a specific preprocessing task.
These functions should be organized into separate files.
You must indicate the script type in the code block.
Do not suggest incomplete code which requires users to modify.
Always put # filename: coding/<filename> as the first line of each code block.

Feel free to include multiple code blocks in one response. Do not ask users to copy and paste the result.

Ensure that your code is well-documented with clear explanations of each function's purpose and usage.

Additionally, include comments throughout the code to enhance readability and maintainability. And name the files appropriately based on the function.

Remember to provide a main script that demonstrates how to use the preprocessing pipeline with example data.
This script should load the raw dataset, apply the preprocessing functions, and output the processed data ready for model training.

Your solution should enable users to efficiently preprocess diverse datasets for machine learning tasks, saving them time and effort in the data preparation phase.
        """)

        agent0.initiate_chat(scraper_agent, True, True, message=message)

        message = agent0.last_message(scraper_agent)

        agent0.initiate_chat(summary_agent, True, True, message=message)

        api_description_message = agent0.last_message(summary_agent)

        # api_description = api_description_message["content"]
        # print(api_description)

        agent0.initiate_chat(aiohttp_client_agent, True, True, message=api_description_message)

        llm_message = agent0.last_message(aiohttp_client_agent)["content"]
        utils.save_code_files(llm_message, self.work_dir)

        self._summary_result = utils.summarize_files(self.work_dir)


if __name__ == "__main__":
    import asyncio

    task = """
     Your task is to generate Python code that implements the data preprocessing pipeline.
     The code should consist of multiple modular functions, each responsible for a specific preprocessing task.
     These functions should be organized into separate files within the aitools_autogen/coding directory and that these files are named based following the format "data-1.py", following a logical structure.
    """
    # Create an instance of CoreClientExample = CoreClientExample()
    blueprint = CoreClientTestBlueprint()

    # Run the blueprint asynchronously
    asyncio.run(blueprint.initiate_work(task))

    print(blueprint.summary_result)
