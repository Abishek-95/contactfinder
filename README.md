I’ve noticed that in most organizations and startups, one of the biggest challenges is finding clients, generating leads, or reaching out for partnerships. A lot of the time, you need to contact a large number of people, and while there are plenty of third-party tools out there to find inperson’s contact details but they usually come with a heavy pricing and some updated data.

I started looking for a simpler way. The method I’m sharing here helps you extract real, in-person emails, and so far, I’ve found it to be one of the more up-to-date and effective approaches.

This approach is actually super simple. I got this while randomly Googling around, and honestly, big thanks to LLMs — they make data cleaning so much easier. Most of the messy cleanup work gets reduced, which saves a ton of time and effort.

Here’s the data pipeline I used (check out the flowchart below). This is just my first version of getting it done, and I had a few challenges — I’ll share those later in the blog.

Press enter or click to view image in full size

For most of the data collection, I just use Google search. So here’s how I try to find in-person emails. First, I put together a search query like company name + department + location and run it on Google. That usually brings up people working in that spot. For example, if I search for Apple Inc HR manager, I’ll get results like the one shown in the image below.

Press enter or click to view image in full size

Next, I need the email format that the company mostly uses. For this, I again use Google to figure it out. For example, for Apple Inc, I got the result shown below.

Press enter or click to view image in full size

Then the next step is simply grab the text from the page and pass it to the LLM. With the right prompt and a few easy tricks, it pulls out the info from the search results

For my use case, I built this tool completely on LangChain. I’ve uploaded the first version of the code on GitHub, so you can check it out there.

To get better results, I used Pydantic BaseModel for defining the data structure and validating the data. A bit of prompt engineering helps in pulling the right details from messy, unstructured text. After that, I added a small validation function to make sure the email format is correct. Finally, I used a third-party tool (VerifiedEmail) to check if the email is actually deliverable.

Drawbacks I found
Instead of just using a SERP API, directly crawling websites with tools like Selenium can give more and better results.
Extracting data from websites needs careful prompt engineering. I noticed some data is hard to understand unless you use strong LLMs like ChatGPT or Gemini, because they’re better at named entity recognition (like finding the right names and roles)
Verification and validation are very important. Sometimes you also need the source link to double-check the data. (In my real version, I even added an extra step using LLM to review and verify the results.)
For emails, you always need a third-party service to check if the extracted email is real or not.
Google search also depends on the right keywords. To get the correct people, I added a set of keywords for each department and role.
Email format itself needs another round of validation to avoid mistakes.
Email format extraction can also be skipped fully if you use third-party tools like ZeroBounce, RocketReach, AlphaEmail, etc.
Somethimes on search engine results past experienced person also included cross check with the snippet will give more accurate result.
I can say this method works about 60–70% of the time unless we take care of the extraction and validation parts. Step by step, I improved it, learned from the drawbacks, and built a better pipeline to handle most of the edge cases. Now, I’m able to extract emails with almost 90% accuracy.

Here’s the pipeline I built

Press enter or click to view image in full size
