# DeepResearchAgent

Deep Research Agent developed with LangGraph

![Deep Research LangGraph](deep_research_langgraph.jpg)

## Features

- Multi-step research using LangGraph
- Web search integration with DuckDuckGo
- LangSmith tracing support
- Interactive Gradio UI

## Steps to Run Code

1. **Install required libraries**
   ```bash
   pip install -U langchain langsmith ddgs numpy gradio langgraph langchain-huggingface langchain-openai langchain-community langchain-core huggingface_hub duckduckgo-search
   ```

2. **Configure API Keys**
   - Add your `OPENAI_API_KEY` to the code
   - Add your LangSmith API key to enable tracing

3. **Run the agent**
   ```bash
   python deep_research_agent.py
   ```
   or
   ```bash
   python deep_research_agent_V2.py
   ```

4. **Usage**
   - Enter your research query
   - Configure settings or use defaults

## Steps to Run with UI

Run the V2 version with Gradio interface:
```bash
python deep_research_agent_V2.py
```

The UI will open in your browser automatically.

## Demo

Check out the demo video:

https://github.com/user-attachments/langchain_demo_agent.mp4


## LangSmith Tracing

View detailed execution traces in LangSmith:

![Trace Example](trace_example.png) 




