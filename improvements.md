# Improvements

- Using different models for different nodes. Example like to generate questions one can use smaller models even open source if works well.
- Use multiple sources rather than search tool that searches arxiv, IEEE, springer links and then another one to going to general web search. This can improve the response well and accurate.
- Token improvement can be done with TOON rather than json as new things are getting developed. Might not work everywhere but saving as much as we can using it.
- Use MCP servers wherever possible.
- Use smaller models for sub questions generation or intent identification and more.
- Add multiple search tools to get more context like API, MCP servers, inbuilt langchain tools
- Moderator Node that can smartly assign which tools can be best for which sub question.
- Separate out the code of UI and the actual node implementation
- Follow OOPs for each node creation as complexity increases
