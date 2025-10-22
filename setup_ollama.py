"""
Quick setup script to configure the chatbot for Ollama (free local LLM)
Run this after installing Ollama from https://ollama.com/download
"""
import os
import subprocess
import sys

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        return response.status_code == 200
    except:
        return False

def pull_model(model_name='llama3.2'):
    """Pull a model from Ollama"""
    print(f"\n🔽 Pulling {model_name} model...")
    print("This may take a few minutes depending on your internet speed.")
    result = subprocess.run(['ollama', 'pull', model_name])
    return result.returncode == 0

def update_server_jac():
    """Update server.jac to use Ollama"""
    server_file = 'server.jac'
    
    if not os.path.exists(server_file):
        print(f"❌ Error: {server_file} not found in current directory")
        return False
    
    with open(server_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already using Ollama
    if 'ollama/' in content:
        print("✅ server.jac is already configured for Ollama")
        return True
    
    # Replace the model configuration
    old_line = "glob llm = Model(model_name='gpt-4o-mini', verbose=True);"
    new_line = "glob llm = Model(model_name='ollama/llama3.2', verbose=True, base_url='http://localhost:11434');"
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        
        # Create backup
        with open(server_file + '.backup', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Write updated file
        with open(server_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {server_file} to use Ollama")
        print(f"📝 Backup saved as {server_file}.backup")
        return True
    else:
        print(f"⚠️  Warning: Could not find the exact line to replace in {server_file}")
        print("Please manually update line 8 to:")
        print(new_line)
        return False

def main():
    print("=" * 60)
    print("🚀 JAC MCP Chatbot - Ollama Setup")
    print("=" * 60)
    
    # Step 1: Check Ollama installation
    print("\n📦 Step 1: Checking Ollama installation...")
    if not check_ollama_installed():
        print("❌ Ollama is not installed!")
        print("\n📥 Please install Ollama first:")
        print("   Windows: https://ollama.com/download/windows")
        print("   Mac: https://ollama.com/download/mac")
        print("   Linux: https://ollama.com/download/linux")
        print("\nAfter installation, run this script again.")
        sys.exit(1)
    print("✅ Ollama is installed")
    
    # Step 2: Check if Ollama is running
    print("\n🔌 Step 2: Checking if Ollama is running...")
    if not check_ollama_running():
        print("⚠️  Ollama service is not running")
        print("Starting Ollama... (this happens automatically on most systems)")
        print("If you see errors, try running: ollama serve")
    else:
        print("✅ Ollama service is running")
    
    # Step 3: Pull model
    print("\n🤖 Step 3: Checking for llama3.2 model...")
    if not pull_model('llama3.2'):
        print("❌ Failed to pull model")
        print("Try manually: ollama pull llama3.2")
        sys.exit(1)
    print("✅ Model ready")
    
    # Step 4: Update server.jac
    print("\n⚙️  Step 4: Updating server.jac configuration...")
    if not update_server_jac():
        sys.exit(1)
    
    # Done!
    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    print("=" * 60)
    print("\n🎉 Your chatbot is now configured to use Ollama (free local LLM)")
    print("\n📝 Next steps:")
    print("   1. Restart your MCP server (if running):")
    print("      jac run mcp_server.jac")
    print("\n   2. Restart your chatbot server:")
    print("      jac serve server.jac")
    print("\n   3. Start the frontend:")
    print("      jac streamlit client.jac")
    print("\n💡 Tip: To use a smaller/faster model, run:")
    print("   ollama pull llama3.2:1b")
    print("   Then update server.jac to use 'ollama/llama3.2:1b'")

if __name__ == '__main__':
    main()
