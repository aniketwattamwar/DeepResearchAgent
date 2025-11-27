
# Tried few things within the time limit

1. My Laptop is ARM64 had issues with rust and pip installing the langchain libraries and hugging face. Use kaggle notebook also to reverify working.
2. Using different model for generating the questions like kimi k2, deepseek or any other good open source models. Gave issues because of langchain hugging face imports. Code is commented for that.
3. Custom logger to show all the traces of the flow of the nodes, it kept failing. Langrace is open source so tried that. The current code has langsmith with my API key. The project show the traces on the Langsmith UI. Image included
4. Time ran out but tried to make a simple UI with gradio which is in the file deep_research_agent_V2.py. The streaming needs to be fixed a bit
5. MCP server connection
