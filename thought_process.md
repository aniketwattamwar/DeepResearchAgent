
# Steps and Approach(Brain Dump on what first comes to mind):

1. Take the input query/topic.(Some parameters can be configured, if i get time to make it or will put in code for now)
2. Generate a set of questions maybe 3 optimized based on the input(use small but good LLM for this, maybe gemma 2b or deepseek models from hugginface?)
3. These sub questions are searched separately (search limit 3 or more? will try and check based on the latency) with tools like web search api, duckduckgo or tavily
4. Now once the context is received, we now use the paid LLM model which in this case is the open ai model (allison gave me key). This model will do the actual thinking where it will compare the context with the question and try to make it the best possible answer. Reflect on the content. (similar from the langchain examples ollama local researcher). Iterate.
5. Once it figures out everything, then it can use the structure of the report and generate the report
6. All these steps can we show to the user (links, sources) or keep in logs(all that can be stored like llm, tokens, etc)?
7. Report is generated and shown to the user.




## Revist few things if time permits:
- RAG works everytime?
- Reranking with open source model( saves money and get relevant docs at top)
- Does the tool like tavily do it for me? need to check this
- Tracing of all these steps? use langtrace itself.





