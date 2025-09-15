import pandas as pd 
import requests
from main_processing import app


clean_list=[]
full_list=[]

inputs=[
    "AMRUT SOFTWARE PRIVATE LIMITED",
    "ENTRUST SOFTWARE & SERVICES PRIVATE LIMITED",
    "Abiraju Pvt ltd"
]

input_dep="HR"

def person_email_formatting(email_format, emp_name):
    email_format = email_format.lower().strip()
    for char in ['[', ']', '{', '}', ' ']:
        email_format = email_format.replace(char, '')
    
    emp_name = emp_name.lower().strip()
    en_list = emp_name.split()
    first, last = en_list[0], en_list[-1]  
    domain = email_format.split('@')[-1]
    email_pattern = email_format.split('@')[0]
    
    format_map = {
        "first.last": f"{first}.{last}@{domain}",
        "first_initiallast": f"{first[0]}{last}@{domain}",
        "flast": f"{first[0]}{last}@{domain}",
        "first_last": f"{first}_{last}@{domain}",
        "first_initial.last": f"{first[0]}.{last}@{domain}",
        "firstlast_initial": f"{first}{last[0]}@{domain}",
        "first.last_initial": f"{first}.{last[0]}@{domain}",
        "first": f"{first}@{domain}",
        "last": f"{last}@{domain}",
        "first_initiallast_initial": f"{first[0]}{last[0]}@{domain}",
        "first_initial.last_initial": f"{first[0]}.{last[0]}@{domain}",
        "firstlast": f"{first}{last}@{domain}",
        "f.last": f"{first[0]}.{last}@{domain}",
        "lastfirst": f"{last}{first}@{domain}",
        "first_l": f"{first}{last[0]}@{domain}",
        "first_last_initial": f"{first}_{last[0]}@{domain}",
        "f_last": f"{first[0]}_{last}@{domain}",
        "last_f": f"{last}_{first[0]}@{domain}",
        "last.first": f"{last}.{first}@{domain}",
        "last_first": f"{last}_{first}@{domain}",
        "l_first": f"{last[0]}_{first}@{domain}",
        "l.first": f"{last[0]}.{first}@{domain}",
    }
    return format_map.get(email_pattern, "format missing")

def verify_email(email):
    url = "https://api.verified.email/v1/verifications"
    params = {"email": email}
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer api_b1676fec2ebd42e183b4491296c00da0"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

for x in inputs:
    results = app.invoke({"org_name":x,"pre_dep": input_dep})
    results['emp_contact'] = (
    results['emp_contact'] if isinstance(results['emp_contact'], list) else [results['emp_contact']]
    )
    if results['emp_contact'] != []:
        print(results)
        for y in results['emp_contact']:
            p_email = person_email_formatting (email_format=results['email_fmt']['email_fmt'],emp_name=y['emp_name'])
            if p_email != "format missing":
                verified_email_details = verify_email(email=p_email)
                y['employee_email'] = p_email    
                y['email_score'] = verified_email_details['verifications'][0]['score']
                y['email_delivery_status'] = verified_email_details['verifications'][0]['result']
                y['overall_source_of_contact']= results['source']
                clean_list.append({"org_name":results["org_name"],"emp_contact":results["emp_contact"]})
                full_list.append(results)
                print(str(x)+ "  is completed")

print(clean_list)

                
