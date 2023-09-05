# Syspons
 AI agent for question answering in a document

#Terminology

### **LLM**
LLM stands for Large Language Model. There are multiple options exists, during this proejct we would refers to ChatGPT-4 (openAI) as the LLM.


### **AI**
An interface with LLM:
The porject interface includes system messages, user meesage and agent meesage.
Why we are using this interface?
For locall run LLAMA-2 is probably the best solution. LLAMA-2 (Meta - license: https://ai.meta.com/resources/models-and-libraries/llama-downloads/) is the start-of-the-art open model that most likely to compete with ChatGPT-4 also contains the same interfaces.
For future use interface can include history (user messages and agent messages)


### **Agent**
A wrapper which wrapper AI with the following functionallity:
1. Predefined system message
2. Convert content into user message
3. Triggeres the AI interface
4. Returns answer in Json format


### **Flow**
An FSM [Finite State Machine] which describe the process of calling agents and based on agents' response.
#### **State**
A state in flow is built from 2 parts: (1) Agent interface and (2) Command execution.

Example: TBD


### **Domain**
* At bussines point of view: a Domain is a unique content (which clear definitions and requiremetns). The product is expected to identify this content in document and generate a summary relate to the domain unique requirements.

* At technical point of view: a Domain is a set of requiremtns which should be identify in the document and summary based on pre-defined requriments.

# Specifics
## Flows
we will use up to 2 flows for POC:
1. Domain Extraction
2. optional Domain Summary

### Flow 1: Domain Extraction
Extract domain information from chunks of text. For POC we will start with naive FSM which contains 2 states.

**State 1: Detect**

An agent will verify if domain information exists in current chunk. Return Json with 3 options:
1. Yes - content exists --> State 2: Extract
2. No - content doesn't exists --> End flow
3. Flag - content partially exists --> Manually review (estimation, partially exists in current chunk and can be automatically fix if chunk will extend with next/previous information)

**State 2: Extract**

An agent will summarize the chunk based on domain requirements and end flow.

### [Optional] Flow 2: Domain Summary
Summary texts which were summarized from flow 1.

**State**

Based on pre-define domain requirements agent will summary concatinated sumamrized from Flow 1: Domain Extraction.

### Open questions
1. Success criterion?
2. Validation
*  suggestion: use previously parsed text and compare results / can we get help with human advisor here?
* How do you currently validation?
3. Verification
* Suggestion: Fine tune model
* Suggestion: model-self feedback
* Manually review

### Notes
* Agent history - not for POC
* Should consier self-feedback to reduce mistakes
