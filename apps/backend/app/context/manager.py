from typing import List, Dict, Any
from app.routing.strategy import AnswerMode

class ContextManager:
    """
    Manages prompt construction, candidate persona grounding, and context synthesis.
    Embeds Santosh Neelappagol's real background (~4 years Python Full Stack + AI)
    and formats answers using proven interview structures.
    """

    @staticmethod
    def get_system_prompt() -> str:
        return """You are Santosh Neelappagol, an accomplished Python Full Stack & AI Developer with ~4 years of production experience.
You are currently answering real-time technical interview questions. You must speak in the FIRST PERSON ("I", "my team", "in my project").

### CANDIDATE PROFILE & WORK EXPERIENCE:
- **Current Role**: Software Engineer at True Blue Technology Pvt Ltd, Bengaluru.
- **Previous Roles**: Full Stack AI Developer at AXA Insurance; Full Stack / AI Backend Developer at Nexuvo.
- **Core Technical Stack**:
  - Backend: Python, FastAPI, REST APIs, Microservices, Asynchronous programming (async/await), Pydantic, Dependency Injection.
  - Frontend: React.js, TypeScript, JavaScript, Redux Toolkit, HTML5, CSS3, Tailwind.
  - Databases & Caching: PostgreSQL, MongoDB, Redis, SQLAlchemy.
  - AI / LLM / RAG: Generative AI, OpenAI/Gemini/Groq APIs, LangChain, RAG (Retrieval Augmented Generation), Prompt Engineering, Sentence Transformers, ChromaDB, PyMuPDF, OCR.
  - Data & Messaging: Apache Kafka, Pandas, NumPy, Scikit-learn, Requests, BeautifulSoup.
  - DevOps & Tools: Docker, Git/GitHub, CI/CD pipelines (Jenkins), AWS, Azure, Swagger/OpenAPI, PyTest, Postman.

### SIGNATURE PRODUCTION PROJECTS:
1. **Trade News Analyser**:
   - AI-powered financial market intelligence platform for real-time news extraction, summarization, entity recognition, and sentiment signals.
   - Built with FastAPI, Kafka for event-driven asynchronous ingestion, Requests/BeautifulSoup for scraping, PostgreSQL for metadata, MongoDB for raw articles, Redis caching, and LangChain + LLM APIs for summarization.
2. **Nexuvo AI Chatbots**:
   - Scalable conversational AI service handling user queries and business workflow automation.
   - Built with FastAPI microservices, MongoDB for session context/conversational memory, PostgreSQL for business entities, RAG pipeline with vector search, and OpenAI/LLM APIs.
3. **AXA Insurance Document & Claims Processing**:
   - Document extraction (PDFs, claims, forms) using PyMuPDF and OCR, automated validation, and FastAPI backend microservices.

### SPEAKING STYLE & TONE GUIDELINES:
- **First Person**: Always use "I designed...", "In my project...", "Coming to my role in this...", "When it comes to...".
- **Structured & Natural**: Use clear spoken signposts ("When it comes to...", "Coming to the backend implementation...", "In my projects...", "One challenge we faced...", "In short...").
- **Grounded in Real Engineering**: Explain architectural trade-offs (e.g., why Kafka for async queue, why Postgres + Mongo hybrid, why Redis caching, why async/await vs multiprocessing, why RAG over fine-tuning).
- **Never Break Character**: Never mention you are an AI, an LLM, or reading from prompt context. Speak as the actual experienced candidate."""

    @staticmethod
    def build_generation_prompt(
        question: str,
        conversation_context: List[str],
        document_chunks: List[Dict[str, Any]],
        mode: str,
    ) -> str:
        prompt_parts = []

        # 1. Mandatory Document Knowledge Context (Candidate's actual past transcripts & notes)
        if document_chunks:
            prompt_parts.append("### MANDATORY CANDIDATE KNOWLEDGE BASE (YOUR RESUME & PAST INTERVIEW EXPERIENCE):")
            prompt_parts.append("Integrate facts from these references directly into your response as YOUR OWN actual experience:")
            for idx, chunk in enumerate(document_chunks, 1):
                source = chunk.get("metadata", {}).get("filename", "Uploaded Knowledge Base")
                text = chunk.get("text", "").strip()
                prompt_parts.append(f"[{idx}] (Source: {source}):\n{text}")
            prompt_parts.append("")
        else:
            prompt_parts.append("### CANDIDATE KNOWLEDGE BASE:\nRely on your core experience at True Blue Technology, Nexuvo, and AXA Insurance.\n")

        # 2. Recent Conversation Context
        if conversation_context:
            prompt_parts.append("### RECENT INTERVIEW DIALOGUE:")
            for turn in conversation_context[-4:]:
                prompt_parts.append(f"- {turn}")
            prompt_parts.append("")

        # 3. Target Question
        prompt_parts.append(f"### INTERVIEWER'S QUESTION:\n{question}\n")

        # 4. Mode-specific Formatting & Delivery Instructions
        if mode == "fast":
            prompt_parts.append(
                "### DELIVERY FORMAT (FAST MODE - SUB-2s REAL-TIME VOICE ANSWER):\n"
                "- Provide a crisp, spoken response (under 120-150 words) that can be delivered naturally out loud.\n"
                "- Begin directly with a strong 1-sentence definition/answer.\n"
                "- Follow with 2-3 concise bullet points with bold headers (e.g. **When it comes to...**, **In my project...**).\n"
                "- Conclude with a quick summary sentence (**In short...**)."
            )
        elif mode == "reasoning":
            prompt_parts.append(
                "### DELIVERY FORMAT (REASONING MODE - IN-DEPTH ARCHITECTURE & CODING):\n"
                "- Provide a structured, senior-level response explaining architecture, trade-offs, and implementation details.\n"
                "- Structure into clear sections:\n"
                "  1. **Core Concept / Problem Statement**: Clear high-level explanation.\n"
                "  2. **Architecture & Implementation**: How you build it in FastAPI, PostgreSQL, Kafka, or React.\n"
                "  3. **Challenges & Trade-offs**: Real edge cases, performance bottlenecks, and how you solved them.\n"
                "  4. **In My Projects**: Concrete reference to Trade News Analyser, Nexuvo Chatbots, or AXA Insurance.\n"
                "- If coding is requested, provide clean, idiomatic Python code with error handling."
            )
        else:  # research mode
            prompt_parts.append(
                "### DELIVERY FORMAT (RESEARCH MODE - EXHAUSTIVE SYSTEM DESIGN & DEEP DIVE):\n"
                "- Provide an exhaustive, end-to-end breakdown covering architecture, data modeling, concurrency, scaling, security, and edge cases.\n"
                "- Contrast multiple architectural approaches and justify your choice with metrics and real-world trade-offs."
            )

        return "\n".join(prompt_parts)

context_manager = ContextManager()
