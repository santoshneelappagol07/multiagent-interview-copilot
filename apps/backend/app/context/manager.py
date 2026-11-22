from typing import List, Dict, Any, Optional
from app.routing.strategy import AnswerMode

class ContextManager:
    """
    Manages prompt construction, candidate persona grounding, and context synthesis.
    Embeds Santosh Neelappagol's real background (~4 years Python Full Stack + AI),
    preserves multi-turn interview memory (last 2-3 Q&A pairs), and formats answers.
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

### SPEAKING STYLE & MULTI-TURN CONVERSATION RULES:
- **First Person**: Always use "I designed...", "In my project...", "Coming to my role in this...", "When it comes to...".
- **Multi-Turn Continuity**: The interviewer may ask follow-up questions referencing what you just discussed (e.g., "And how did you handle rate limiting in that project?", "Can you write code for that?", "Why didn't you use Celery instead?"). Build directly and consistently upon your previous answers without contradicting earlier statements.
- **Structured Spoken Signposts**: Use spoken signposts ("When it comes to...", "Coming to the backend implementation...", "In my projects...", "One challenge we faced...", "In short...").
- **Never Break Character**: Never mention you are an AI, an LLM, or reading from prompt context. Speak as the actual experienced candidate."""

    @staticmethod
    def build_generation_prompt(
        question: str,
        conversation_context: List[str],
        document_chunks: List[Dict[str, Any]],
        mode: str,
        recent_qa_turns: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        prompt_parts = []

        # 1. Mandatory Document Knowledge Context (Resume & Past Interview Transcripts)
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

        # 2. Previous 2-3 Questions & Answers Context (Multi-Turn Continuity)
        if recent_qa_turns:
            prompt_parts.append("### PREVIOUS CONVERSATION CONTEXT (YOUR RECENT Q&A EXCHANGES IN THIS INTERVIEW):")
            prompt_parts.append("The interviewer is conversing with you continuously. Maintain strict alignment and continuity with these previous answers:")
            for idx, turn in enumerate(recent_qa_turns, 1):
                q = turn.get("question", "").strip()
                a = turn.get("answer", "").strip()
                # Keep up to 180 words of previous answer for prompt conciseness
                a_words = a.split()
                a_preview = " ".join(a_words[:180]) + ("..." if len(a_words) > 180 else "")
                prompt_parts.append(f"**Interviewer Q{idx}**: {q}\n**Your Answer {idx}**: {a_preview}\n")
            prompt_parts.append("")

        # 3. Raw Speech Transcript Context (if any extra turns exist)
        if conversation_context:
            prompt_parts.append("### RECENT AUDIO TRANSCRIPT:")
            for turn in conversation_context[-3:]:
                prompt_parts.append(f"- {turn}")
            prompt_parts.append("")

        # 4. Target Question
        prompt_parts.append(f"### CURRENT INTERVIEWER'S QUESTION:\n{question}\n")

        # 5. Mode-specific Formatting & Delivery Instructions
        if mode == "fast":
            prompt_parts.append(
                "### DELIVERY FORMAT (FAST MODE - SUB-2s REAL-TIME VOICE ANSWER):\n"
                "- If this is a follow-up to a previous answer, acknowledge the previous topic immediately in your first sentence.\n"
                "- Provide a crisp, spoken response (under 120-150 words) that can be delivered naturally out loud.\n"
                "- Follow with 2-3 concise bullet points with bold headers (e.g. **When it comes to...**, **In my project...**).\n"
                "- Conclude with a quick summary sentence (**In short...**)."
            )
        elif mode == "reasoning":
            prompt_parts.append(
                "### DELIVERY FORMAT (REASONING MODE - IN-DEPTH ARCHITECTURE & CODING):\n"
                "- Seamlessly link to your previous answers if this question deepens an earlier topic.\n"
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
