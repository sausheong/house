import os
from dotenv import load_dotenv, find_dotenv
from langchain.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.chat_models import AzureChatOpenAI, ChatVertexAI, ChatOpenAI
from langchain.llms import OpenAI, AzureOpenAI, VertexAI

from specs import Specification, house_specs, moderator_specs

load_dotenv(find_dotenv())
openai_api_key=os.getenv('OPENAI_API_KEY')
azure_api_key=os.getenv('AZURE_API_KEY')
azure_deployment_name=os.getenv('AZURE_DEPLOYMENT_NAME')
azure_api_version=os.getenv('AZURE_API_VERSION')
azure_base_url=os.getenv('AZURE_API_BASE')
model_name=os.getenv('PALM_MODEL')
location=os.getenv('PALM_LOCATION')
max_tokens=int(os.getenv('MAX_TOKENS', 128))
max_retries=int(os.getenv('MAX_RETRIES', 3)) 

# we only use the search tool here, but you can add other tools
def get_tools():
    search_tool = DuckDuckGoSearchRun()
    return [
        search_tool,
    ] + load_tools(["requests_all"])    

# setting up the LLM to use, add other LLMs later
def get_llm(provider, model_name, max_tokens_generated):
    if provider == "openai":
        if model_name.startswith("gpt-4") or model_name.startswith("gpt-3.5"):
            llm = ChatOpenAI(
                temperature=0.7,
                model_name=model_name,
                openai_api_key=openai_api_key,
                max_tokens=max_tokens_generated,
                max_retries=max_retries,
            )
        else:
            llm = OpenAI(
                temperature=0.7,
                model_name=model_name,
                openai_api_key=openai_api_key,
                max_tokens=max_tokens_generated,
                max_retries=max_retries,
            )

    if provider == "azure":
        if model_name.startswith("gpt-4") or model_name.startswith("gpt-3.5"):
            llm = AzureChatOpenAI(
                temperature=0.7,
                openai_api_base=azure_base_url,
                openai_api_version=azure_api_version,
                model_name=model_name,
                deployment_name=azure_deployment_name,
                openai_api_key=azure_api_key,
                openai_api_type="azure",
                max_tokens=max_tokens_generated,
                max_retries=max_retries,
            )
        else:
            llm = AzureOpenAI(
                temperature=0.7,
                openai_api_base=azure_base_url,
                openai_api_version=azure_api_version,
                model_name=model_name,
                deployment_name=azure_deployment_name,
                openai_api_key=azure_api_key,
                openai_api_type="azure",
                max_tokens=max_tokens_generated,
                max_retries=max_retries,
            )

    if provider == "palm":
        if model_name == "chat-bison":
            llm = ChatVertexAI(
                temperature=0.7,
                model_name=model_name,
                location=location,
                max_output_tokens=max_tokens_generated,
                max_retries=max_retries,
            )
        else:
            llm = VertexAI(
                temperature=0.7,
                model_name=model_name,
                location=location,
                max_output_tokens=max_tokens_generated,
                max_retries=max_retries,
            )    
    
    return llm

# create the agent
def create_agent(specs: Specification):
    # persona has a larger number of tokens
    if specs.persona == "Moderator":
        max_tokens_generated = 4096
    else:
        max_tokens_generated = max_tokens

    agent = initialize_agent(
        get_tools(),
        get_llm(specs.provider, specs.model_name, max_tokens_generated),
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=ConversationBufferMemory(memory_key="chat_history", 
            return_messages=True, ai_prefix=specs.persona, human_prefix="Moderator"),
        handle_parsing_errors="Check output and make sure it conforms to format. Remove backticks.",
        verbose=True,
    )
    agent.run(specs.context)
    return agent

# setup the house with participants and also the moderator
house = []
for spec in house_specs:
    house.append(create_agent(spec))

moderator = create_agent(moderator_specs)