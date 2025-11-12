# API Key Setup Guide

## Do You Need an API Key?

**Short answer: NO, but it's recommended for better results.**

The project works without an API key, but adding one improves the quality of embeddings and enables real AI-generated answers.

## What Works Without API Key

✅ **Semantic Search** - Fully functional using SentenceTransformers  
✅ **Vector Database** - FAISS works perfectly  
✅ **Knowledge Graph** - Visualization works  
✅ **Search Results** - Returns ranked documents  
⚠️ **RAG Answers** - Uses template responses (not AI-generated)

## What's Better With API Key

🚀 **Better Embeddings** - OpenAI's embedding models (text-embedding-3-small/large)  
🚀 **AI-Generated Answers** - Real GPT-3.5/GPT-4 responses via LangChain  
🚀 **Better Search Quality** - More accurate semantic matching

## How to Add API Key (Optional)

### Step 1: Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy the key (starts with `sk-...`)

### Step 2: Create .env File

```bash
cd backend
cp .env.example .env
```

### Step 3: Add Your Key

Edit `backend/.env` and add:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
DATABASE_URL=sqlite:///./knowledge_base.db
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo
```

### Step 4: Restart Backend

The backend will automatically detect the API key on startup.

## Cost Considerations

- **Embeddings**: ~$0.0001 per 1K tokens (very cheap)
- **GPT-3.5-turbo**: ~$0.0015 per 1K tokens (cheap)
- **For testing**: Usually costs less than $1-2 for extensive testing

## Testing Without API Key

You can test the entire system without an API key:

```bash
# Backend will show:
# "No OpenAI API key found, using SentenceTransformers"
# "Warning: OpenAI API key not found. RAG will return template responses."

# But everything else works perfectly!
```

## Recommendation

1. **Start without API key** - Test the system first
2. **Add API key later** - When you want better answers
3. **Monitor usage** - Set spending limits on OpenAI dashboard

