# LeadGen - Contact Scrapper

A simple tool to extract employee contacts (name, role, location, email format) using LangChain + LLMs + Google search.

**Description**
Finding leads and reaching out to the right people is often expensive using third-party tools. This project shows how LLMs can help clean, extract, and validate data from search results in a cost-effective way.


**Main_processing.py** handles below steps.

1)Search company + department + location.

2)Extract employee details (name, role, location).

3)Detect the organization’s email format.

**app.py** handles the below steps:

4)Generate valid emails for employees.

5)Verify emails with a third-party API.

# Tools Used :
**LangChain** for pipeline orchestration.

**Pydantic** for data structure & validation.

**Tavily** for search results.

**Verified Email API** for checking deliverability.

# Limitations:

1)Instead of just using a SERP API, directly crawling websites with tools like Selenium can give more and better results.
2)Extracting data from websites needs careful prompt engineering. I noticed some data is hard to understand unless you use strong LLMs like ChatGPT or Gemini, because they’re better at named entity recognition (like finding the right names and roles)
3)Verification and validation are very important. Sometimes you also need the source link to double-check the data. (In my real version, I even added an extra step using LLM to review and verify the results.)
4)For emails, you always need a third-party service to check if the extracted email is real or not.
5)Google search also depends on the right keywords. To get the correct people, I added a set of keywords for each department and role.
6)Email format itself needs another round of validation to avoid mistakes.
7)Email format extraction can also be skipped fully if you use third-party tools like ZeroBounce, RocketReach, AlphaEmail, etc.
8)Somethimes on search engine results past experienced person also included cross check with the snippet will give more accurate result.


I can say this method works about 60–70% of the time unless we take care of the extraction and validation parts. Step by step, I improved it, learned from the drawbacks, and built a better pipeline to handle most of the edge cases. Now, I’m able to extract emails with almost 90% accuracy.

Here’s the pipeline I built.

![image](https://github.com/user-attachments/assets/bdf5ff96-d603-47dd-ac29-41ee7640ec83)

Additinally Please out look at my blog here : https://medium.com/@abishekm1995/contact-finder-a-simple-way-to-find-emails-using-ai-85c6885b1676
