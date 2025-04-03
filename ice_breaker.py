from dotenv import load_dotenv

# from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parser import summary_parser


def ice_break_with(name: str) -> str:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)

    print("Hello LangChain")

    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    \n{format_instruction}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instruction": summary_parser.get_format_instructions()
        },
    )

    # formatted_prompt = summary_prompt_template.format(information=information)
    # res = llm.invoke(formatted_prompt)

    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.0-flash")

    chain = summary_prompt_template | llm | summary_parser
    res = chain.invoke(input={"information": linkedin_data})

    # for chunk in chain.stream(input={"information": linkedin_data}):
    #     print(chunk.content, end="", flush=True)  # Cetak konten chunk secara streaming

    return res, linkedin_data.get("photoUrl")
    # print(type(res))


if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker")
    ice_break_with("fiqri fernando tiras")
