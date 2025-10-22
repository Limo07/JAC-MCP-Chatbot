# Windows Path Unicode Escape Fix for jac-streamlit

## Problem
When running `jac streamlit client.jac` on Windows, the following error occurred:

```
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 2-3: truncated \UXXXXXXXX escape
```

## Root Cause
The error was caused by the `jac-streamlit` plugin generating a temporary Python file with Windows paths containing backslashes. When the path contained `\U` (like in `C:\Users`), Python interpreted it as a Unicode escape sequence instead of a literal backslash.

## The Bug Location
File: `jaclang_streamlit/commands.py` (in the jac-streamlit package)

**Original problematic code (line 36):**
```python
py_lines = [
    "from jaclang_streamlit import run_streamlit",
    f'run_streamlit("{basename}", "{dirname}")',  # ❌ dirname has backslashes
]
```

When this generated code like:
```python
run_streamlit("client", "C:\Users\kiplimo\OneDrive\Desktop\AI STUDY\Git JAC Chatbot\Agentic-AI\jac-mcp-chatbot")
```

Python tried to interpret `\U` as a Unicode escape, causing the syntax error.

## The Fix
**Modified code (line 36):**
```python
py_lines = [
    "from jaclang_streamlit import run_streamlit",
    f'run_streamlit("{basename}", r"{dirname}")',  # ✅ Using raw string (r"")
]
```

The fix adds `r` before the dirname string, making it a raw string literal. This tells Python to treat backslashes as literal characters rather than escape sequences.

Now it generates:
```python
run_streamlit("client", r"C:\Users\kiplimo\OneDrive\Desktop\AI STUDY\Git JAC Chatbot\Agentic-AI\jac-mcp-chatbot")
```

## Files Modified
1. **Backup created:**
   - `C:\Users\kiplimo\OneDrive\Desktop\AI STUDY\jac-env\Lib\site-packages\jaclang_streamlit\commands.py.backup`

2. **Fixed file:**
   - `C:\Users\kiplimo\OneDrive\Desktop\AI STUDY\jac-env\Lib\site-packages\jaclang_streamlit\commands.py`

## Testing
After applying the fix, you can run:
```bash
cd "C:\Users\kiplimo\OneDrive\Desktop\AI STUDY\Git JAC Chatbot\Agentic-AI\jac-mcp-chatbot"
jac streamlit client.jac
```

The Unicode escape error should no longer occur.

## Workaround Script
Additionally created `run_streamlit.py` in the jac-mcp-chatbot directory as an alternative way to launch the app:
```bash
python run_streamlit.py
```

## Contributing the Fix Upstream
This fix should be contributed back to the jac-streamlit project on GitHub to help other Windows users. The change is minimal and ensures cross-platform compatibility.

## Technical Details
- **Package:** jac-streamlit v0.0.4
- **Python Version:** 3.12
- **OS:** Windows
- **Issue Type:** Windows path handling in dynamically generated Python code
- **Fix Type:** Raw string literal (r"") for Windows paths
