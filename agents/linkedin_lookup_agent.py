from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.tools import get_profile_url_tavily


def lookup(name: str) -> str:
    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.0-flash")
    template = """
  given the full name {name_of_person} i want you to get it me me a link to ther linkedin profile page. Your answer should contain only URL
  """

    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )
    tools_for_agent = [
        Tool(
            name="Crawl google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful when you need get the linkedin page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]

    return linkedin_profile_url


if __name__ == "__main__":
    print(lookup("Eden Marco"))
