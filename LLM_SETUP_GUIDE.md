# Fixing OpenAI Billing Error - Alternative LLM Setup

## Problem
Your OpenAI account is not active or has billing issues:
```
Error code: 429 - Your account is not active, please check your billing details
```

## Solutions

### Option 1: Use Ollama (Free, Local LLM) ⭐ RECOMMENDED

Ollama runs AI models locally on your machine - completely free!

#### Step 1: Install Ollama
Download and install from: https://ollama.com/download

#### Step 2: Pull a Model
Open a new terminal and run:
```bash
ollama pull llama3.2
```

Or for a smaller/faster model:
```bash
ollama pull llama3.2:1b
```

#### Step 3: Update server.jac
Change line 8 in `server.jac` from:
```jac
glob llm = Model(model_name='gpt-4o-mini', verbose=True);
```

To:
```jac
glob llm = Model(model_name='ollama/llama3.2', verbose=True, base_url='http://localhost:11434');
```

#### Step 4: Restart the Server
```bash
jac serve server.jac
```

---

### Option 2: Use Groq (Free API, Cloud-based) 🚀

Groq offers free, fast LLM API access!

#### Step 1: Get Free API Key
1. Go to https://console.groq.com/
2. Sign up (free)
3. Get your API key from "API Keys" section

#### Step 2: Set Environment Variable
```bash
# PowerShell
$env:GROQ_API_KEY="your-groq-api-key-here"

# Or add to your .env file
GROQ_API_KEY=your-groq-api-key-here
```

#### Step 3: Update server.jac
Change line 8 in `server.jac` from:
```jac
glob llm = Model(model_name='gpt-4o-mini', verbose=True);
```

To:
```jac
glob llm = Model(model_name='groq/llama-3.3-70b-versatile', verbose=True);
```

#### Step 4: Restart the Server
```bash
jac serve server.jac
```

---

### Option 3: Use Google Gemini (Free Tier Available) 🌟

Google's Gemini has a generous free tier!

#### Step 1: Get Free API Key
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"

#### Step 2: Set Environment Variable
```bash
# PowerShell
$env:GEMINI_API_KEY="your-gemini-api-key-here"

# Or add to your .env file
GEMINI_API_KEY=your-gemini-api-key-here
```

#### Step 3: Update server.jac
Change line 8 in `server.jac` from:
```jac
glob llm = Model(model_name='gpt-4o-mini', verbose=True);
```

To:
```jac
glob llm = Model(model_name='gemini/gemini-2.0-flash-exp', verbose=True);
```

#### Step 4: Restart the Server
```bash
jac serve server.jac
```

---

### Option 4: Fix OpenAI Billing

If you still want to use OpenAI:

1. **Check your API key**: Make sure `OPENAI_API_KEY` is set correctly
   ```bash
   echo $env:OPENAI_API_KEY  # PowerShell
   ```

2. **Add billing**: Go to https://platform.openai.com/account/billing
   - Add a payment method
   - Add credits (minimum $5)

3. **Verify account status**: https://platform.openai.com/settings/organization/billing/overview

---

## Quick Start: Ollama Setup (Easiest)

```bash
# 1. Install Ollama from https://ollama.com/download

# 2. Pull a model
ollama pull llama3.2

# 3. Test it works
ollama run llama3.2 "Hello"

# 4. Update your server.jac (see Option 1 above)

# 5. Restart your server
jac serve server.jac
```

---

## Supported Model Providers in byllm

Your chatbot uses `byllm` which supports:
- OpenAI (gpt-4, gpt-3.5-turbo, etc.)
- Ollama (local models)
- Groq (llama, mixtral, gemma)
- Google (gemini models)
- Anthropic (claude models)
- Together AI
- And many more via LiteLLM

Check the full list: https://docs.litellm.ai/docs/providers
