"""RAG pipeline using LangChain."""
import os
from typing import List, Dict
from dotenv import load_dotenv
try:
    from langchain_openai import ChatOpenAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
except ImportError:
    # Fallback for older langchain versions
    try:
        from langchain.chat_models import ChatOpenAI
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
    except ImportError:
        ChatOpenAI = None
        PromptTemplate = None
        LLMChain = None

load_dotenv()

class RAGPipeline:
    """Retrieval-Augmented Generation pipeline."""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and ChatOpenAI:
            try:
                self.llm = ChatOpenAI(
                    model_name=os.getenv("LLM_MODEL", "gpt-3.5-turbo"),
                    temperature=0.7,
                    openai_api_key=api_key
                )
                self.enabled = True
            except Exception as e:
                print(f"Warning: Could not initialize LLM: {e}")
                self.llm = None
                self.enabled = False
        else:
            self.llm = None
            self.enabled = False
            if not api_key:
                print("Warning: OpenAI API key not found. RAG will return template responses.")
    
    def generate_answer(self, question: str, context_docs: List[Dict]) -> str:
        """Generate answer using retrieved context."""
        if not self.enabled:
            # Fallback template response
            return self._template_response(question, context_docs)
        
        # Combine context from retrieved documents
        context = "\n\n".join([
            f"Document {i+1}: {doc.get('title', 'Unknown')}\n{doc.get('content', '')[:1000]}"
            for i, doc in enumerate(context_docs)
        ])
        
        # Create prompt template
        prompt_template = PromptTemplate(
            input_variables=["question", "context"],
            template="""You are a helpful AI assistant. Answer the question based on the provided context documents.

Context:
{context}

Question: {question}

Provide a clear, concise answer based on the context. If the context doesn't contain enough information, say so.

Answer:"""
        )
        
        try:
            if LLMChain and self.llm:
                # Generate answer
                chain = LLMChain(llm=self.llm, prompt=prompt_template)
                answer = chain.run(question=question, context=context)
                return answer.strip()
            else:
                return self._template_response(question, context_docs)
        except Exception as e:
            print(f"Error in RAG generation: {e}")
            return self._template_response(question, context_docs)
    
    def _template_response(self, question: str, context_docs: List[Dict]) -> str:
        """Fallback template response when LLM is not available."""
        if not context_docs:
            return "I couldn't find relevant information to answer your question."
        
        titles = [doc.get('title', 'Unknown') for doc in context_docs]
        return f"Based on the retrieved documents ({', '.join(titles[:3])}), here's what I found related to your question: '{question}'. Please review the search results for detailed information."

