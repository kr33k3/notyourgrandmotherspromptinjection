# notyourgrandmotherspromptinjection






# Anamtor of the Lab

## Narrative
We are tony pajamas pajama store. We sell AI Powered pajamas. 
Users can order AI powered Pajamas that come with built in AI for all your AI needs. 

The whole site is just using the AI word too much. 
This leads to them using AI for wayyyy too much on their platform. 
We'll show legitimate business use cases in this lab, but also over extensions that can lead to pwnage. 

## Pages

#### Orders Page
Chat bot model that can tell you about your order and its status

#### Ordering Page
Click through ordering of some project




### Chat model Actions
- Retrieve order details
#### Retrieving Order details
- Builds context of what your order is from being signed in or what you say your name. 
- First an obvious thing exploit is "Prompt Injection".
  - Lets say we didn't use a system prompt first and we just ask the chat to dump what was said so far. This way we get what the instructions are.
  - Overwrite the userId by prompt injection
  - 
 Instead of telling me 

#### Contact / Outreach 
- Sends emails. Would you like an email as a reminder? This can be used to exfil data. 
- 


## Attack Paths
### 




# Crazy Ideas 
On user create we generate a flag for a user and then people can try to steal someone elses flags that are stored in the DB or the vector DB? I don't know. Giving people their own data and then others being able to do things to it. Could be fun.
