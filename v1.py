import pandas as pd
from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from tavily import TavilyClient
from langgraph.graph import StateGraph, START, END
import json
import requests
import time


Google_llm_model = "gemini-2.0-flash"
google_embedding_model="models/embedding-001"
google_api_key = "AIzaSyB5k0jYMZ9xccA6nA-Cgz2sWLDwmF7WYkM"
tavily_api_key= "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"
linkedin_scraper_username="abishekmani"
linkedin_scrapper_apikey="TWm6INEhmW1vGzKpkqVOQSBwM"


class emp_bp(TypedDict):
    org_name : str 
    emp_contact :list[dict]
    dep_list:list[str]
    pre_dep:str
    search_results:str
    source : str
    email_fmt:str
    
    
class actual_details(BaseModel):
    emp_name : str = Field(description="employee names")
    designation : str = Field(description="employee designation or title posistion")
    location : str = Field(description="employee location")
    dep:str=Field(description="guess the employee department.")
    source_link:str = Field(description="give the source link of the employee")

class email_format(BaseModel):
    email_fmt :str = Field(description="identify most commonly used email format")
    source_link:str = Field(description="get the source link of the email format")


def get_results (search_result:emp_bp) -> emp_bp:
    client = TavilyClient(tavily_api_key)
    search_results = client.search(
        query= search_result['org_name']+ " "+search_result["pre_dep"],
        max_results=10
    )
    search_result['search_results']= search_results['results']
    search_result['source']="google"
    return search_result

def contact_retriever(contact:emp_bp) -> emp_bp:
    parser = JsonOutputParser(pydantic_object=actual_details)
    llm = ChatGoogleGenerativeAI(model=Google_llm_model,google_api_key=google_api_key)
    prompt = PromptTemplate(
        template= """
        Extract all employees who strictly belong to {lead} from the provided content. Ensure that only employees from {lead} are included—no other information should be extracted.
        Extracted_content : {content}
        {format_instructions}
        Guidelines:
        Strictly extract only employees related to {lead}—do not include unrelated people.
        Use exact information from the content without any modifications or assumptions.
        Ensure accurate department categorization based on job title (e.g., "VP Product" → "Product Management").
        Provide a valid source link where each employee's name and designation appear.Give the exact source link from json.
        Do not generate or infer any fictional data—use only what is explicitly mentioned in the content.
        """,
    input_variables=['lead','content'],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    try:
        chain = prompt | llm | parser
        response_chain=chain.invoke({"lead": contact['org_name'],"content":contact["search_results"]})
        contact['emp_contact']= response_chain
        return contact
    except:
        contact['emp_contact']= []
        return contact
    

def search_results(data,job):
    client = TavilyClient(tavily_api_key)
    response = client.search(
        query= data['org_name']+ " "+job,
        max_results=10
        )
    return response

def linkedin_scrapper(contact_bp:emp_bp)->emp_bp:
    username = linkedin_scraper_username
    apiKey = linkedin_scrapper_apikey
    scraper = 'linkedinCompanyProfile'
    profile_link=search_results(data=contact_bp,job="Linkedin")
    profile_link=profile_link['results'][0]['url']
    url = profile_link + '/people/?keywords=' + contact_bp['pre_dep']
    print(url+" "+"here is the scrapping url")
    apiEndPoint = "http://api.scraping-bot.io/scrape/data-scraper"
    apiEndPointResponse = "http://api.scraping-bot.io/scrape/data-scraper-response?"
    payload = json.dumps({"url": url, "scraper": scraper})
    headers = {
        'Content-Type': "application/json"
    }
    response = requests.request("POST", apiEndPoint, data=payload, auth=(username, apiKey), headers=headers)
    raw_content=""
    if response.status_code == 200:
        responseId = response.json()["responseId"]
        pending = True
        while pending:
            time.sleep(8)
            finalResponse = requests.request("GET", apiEndPointResponse + "scraper=" + scraper + "&responseId=" + responseId
                                         , auth=(username, apiKey))
            result = finalResponse.json()
            if type(result) is list:
                pending = False
                raw_content=(finalResponse.text)
                contact_bp['search_results']=raw_content
                contact_bp['source']="linkedin"
            elif type(result) is dict:
                if "status" in result and result["status"] == "pending":
                    print(result["message"])
                    continue
                elif result["error"] is not None:
                    pending = False
                    raw_content=(json.dumps(result, indent=4))
                    contact_bp['search_results']=raw_content
                    contact_bp["source"]="linkedin"
    else:
        return "No results found"
    return contact_bp


def email_fmt_finder(state:emp_bp) -> emp_bp:
    content=search_results(data=state,job="email format")
    parser = JsonOutputParser(pydantic_object=email_format)
    llm = ChatGoogleGenerativeAI(model=Google_llm_model,google_api_key=google_api_key)
    prompt = PromptTemplate(
        template= """
        From the given content, identify the most commonly used email format for {lead} . Ensure that the email format strictly belongs to {lead}
        Extracted_content : {content}
        {format_instructions}
        first.last,first_initiallast,flast,first_last,first_initial.last,firstlast_initial,first.last_initial,first,last,first_initiallast_initial,first_initial.last_initial,firstlast,f.last,
        lastfirst,first_l,first_last_initial,f_last,last_f,last.first,last_first,l_first,l.first

        """,
    input_variables=['lead','content'],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    try:
        chain = prompt | llm | parser
        response_chain=chain.invoke({"lead": state['org_name'],"content":content})
        state['email_fmt']= response_chain
        return state
    except:
        state['email_fmt']= []
        return state



def router(checklist:emp_bp):
    if checklist['source'] == "google" and checklist["emp_contact"] == []:
        return "linkedin scrapper"
    if checklist['source'] == "linkedin" and checklist['emp_contact'] == []:
        return "end"
    if checklist['emp_contact'] != []:
        return "format_finder"


workflow = StateGraph(emp_bp)
workflow.add_node("search_node", get_results)
workflow.add_node("contact_retriever_node", contact_retriever)
workflow.add_node("linkedin_scrapper_node",linkedin_scrapper)
workflow.add_node("email_format_finder_node",email_fmt_finder)


workflow.add_edge(START, "search_node")
workflow.add_edge("search_node", "contact_retriever_node")
workflow.add_edge("linkedin_scrapper_node","contact_retriever_node")

workflow.add_conditional_edges("contact_retriever_node",router,
                               {
                                   "linkedin_scrapper":"linkedin_scrapper_node",
                                   "end":END,
                                   "format_finder":"email_format_finder_node"
                               })



app = workflow.compile()
result = app.invoke({"org_name": "AMRUT SOFTWARE PRIVATE LIMITED", "pre_dep": "HR"})
print(result)





    

