
<div align="center">
  
  <h1>🤖 AI Coding Agents - Smart Launcher</h1>
  
  <p>A professional and beautifully designed Terminal UI (TUI) for managing and launching AI coding agents with a single click.</p>

  <!-- قم بتغيير image_name.png إلى اسم الصورة التي سترفعها على المستودع -->
  <img src="[image_name.png](https://github.com/user-attachments/assets/1559ce17-aa71-4483-be7a-fee0b353e67b)" alt="AI Agents Launcher Terminal UI" width="750">

  <br><br>
</div>


## ✨ Features
- **Beautiful Terminal Interface**: Built using `Rich` and `Questionary`.
- **AI Agent Management**: Launch Claude Code, Codex, DeepSeek, Aider, Cline, and OpenCode.
- **Git & GitHub Integration**: Manage repositories, branches, commits, and pushes directly from the UI.
- **Web Analysis Tools**: Run Lighthouse and axe audits.
- **System Diagnostics**: Check for outdated packages and verify tool versions.
- **Automated Setup**: The `.bat` script automatically installs all prerequisites (Python packages, Node.js tools, Claude plugins, and MCP servers) on the first run.

## 🛠️ Prerequisites
- **Windows OS** (The `.bat` script is Windows-specific).
- **Python 3.8+**
- **Node.js & npm**
- **Git**

## 🚀 Getting Started
1. Clone or download this repository.
2. Ensure both `free_ai_agents.bat` and `free_ai_agents.py` are in the same directory.
3. Double-click `free_ai_agents.bat`.
4. The script will automatically install dependencies on the first run (this may take a few minutes).
5. Enjoy the launcher!

## 📁 Project Structure
- `free_ai_agents.bat`: Windows setup and launch script.
- `free_ai_agents.py`: Main Python TUI application.
- `CLAUDE.md`: Custom guidelines and instructions for AI agents (Design & Database architecture).
- `settings.local.json`: Local permissions configuration.
- `requirements.txt`: Python dependencies for the project.

## ⚠️ Important Notes
- Commands like `fcc-claude` and `fcc-codex` must be configured in your system's Environment Variables or as Aliases. If they differ on your system, you may need to edit them in `free_ai_agents.py`.
- `config.yaml` and `.setup_complete` are generated automatically and ignored by Git to protect your personal data (e.g., GitHub tokens).

## 📝 License
This project is open-source and available for personal and commercial use.
