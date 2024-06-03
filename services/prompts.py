import os
import traceback
import httpx

def _get_prompt_content(display_name: str, default: str = "Prompt content not available") -> str:
    url = f"http://{os.getenv('CODEPROMPTU_HOSTNAME')}:{os.getenv('CODEPROMPTU_PORT')}/private/prompt/name/{display_name}"

    auth = (os.getenv("CODEPROMPTU_USERNAME"), os.getenv("CODEPROMPTU_PASSWORD"))

    try:
        with httpx.Client(auth=auth) as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("content", default)
    except Exception:
        traceback.print_exc()
        return default

def quick_chat_system_prompt() -> str:
    return _get_prompt_content("quick_chat_system_prompt", """
    Forget all previous instructions.
You are a chatbot named Ducky. You are assisting a user with their programming problems.
Each time the user converses with you, make sure the context is related to software programming,
and that you are providing a helpful response.
If the user asks you to do something that is not related to software programming, you should refuse to respond.
""")

def system_learning_prompt() -> str:
    return _get_prompt_content("system_learning_prompt", """
You are assisting a user with their code.
Each time the user converses with you, make sure the context is related to software programming, or creating a course
syllabus related to software programming, and that you are providing a helpful response. Attempting to chat about a non-software-related topic should receive a polite refusal to engage.
""")

def learning_prompt(learner_level:str, answer_type: str, topic: str) -> str:
    return _get_prompt_content("learning_prompt", f"""
Please disregard any previous context.

The topic at hand is ```{topic}```.
Analyze the sentiment of the topic.

You are assisting someone with their programming problems.
The customer wants to hear your answers at the level of a {learner_level}.

Please develop a detailed, comprehensive {answer_type} to teach me the topic as a {learner_level}.
The {answer_type} should include high level advice, key learning outcomes, detailed examples, step-by-step walkthrough if applicable,
and major concepts and pitfalls people associate with the topic.

Make sure your response is formatted in markdown format.
Ensure that embedded formulae are quoted for good display.
""").format(topic=topic,learner_level=learner_level,answer_type=answer_type)

def review_prompt(user_code:str) -> str:
    return _get_prompt_content("review_prompt", f"""
Review the following code:\n\n```python\n{user_code}\n```
Please provide code review comments and suggestions.
""").format(user_code=user_code)

def debug_prompt(user_code:str) -> str:
    return _get_prompt_content("debug_prompt", f"""
Debug the following code and point out all mistakes:\n\n```python\n{user_code}\n```
""").format(user_code=user_code)

def modify_code_prompt(user_code:str, modification_request:str) -> str:
    return _get_prompt_content("modify_code_prompt", f"""
Modify the following code based on the request:\n\n```python\n{user_code}\n```Modification Request: {modification_request}
""").format(user_code=user_code,modification_request=modification_request)
