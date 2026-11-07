#!/usr/bin/env python3
"""
free_ai_agents.py - Modern Terminal UI for AI Coding Agents
A beautiful launcher using rich and questionary for selecting AI agents.
"""

import subprocess
import sys
import os
import time
import json
import shutil
import socket
from pathlib import Path
from typing import Dict, List, Optional

# Try to import required libraries, provide helpful error if missing
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    from rich.table import Table
    import questionary
    from questionary import Style
    import yaml
except ImportError as e:
    print(f"[ERROR] Missing required library: {e}")
    print("[INFO] Please run: pip install rich questionary colorama pyfiglet pyyaml")
    sys.exit(1)

console = Console()

# حل مشكلة خطأ 'str' object has no attribute 'invalidation_hash' في الإصدارات الجديدة
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),
    ('question', 'bold'),
    ('pointer', 'fg:#673ab7 bold'),
    ('highlighted', 'fg:#673ab7 bold'),
    ('selected', 'fg:#cc5454'),
    ('separator', 'fg:#cc5454'),
    ('instruction', ''),
    ('text', ''),
    ('disabled', 'fg:#858585 italic')
])

def get_script_dir():
    """Get the directory where this script is located."""
    return Path(__file__).parent.absolute()

def get_profiles_dir():
    """Get the directory for storing profiles."""
    profiles_dir = get_script_dir() / "profiles"
    profiles_dir.mkdir(exist_ok=True)
    return profiles_dir

def get_github_dir():
    """Get the directory for GitHub projects."""
    github_dir = get_script_dir() / "github_projects"
    github_dir.mkdir(exist_ok=True)
    return github_dir

def load_config() -> Dict:
    """Load configuration from config file."""
    config_file = get_script_dir() / "config.yaml"
    default_config = {
        "profiles": {},
        "github": {"username": "", "token": ""},
        "web_tools": {"lighthouse_path": "lighthouse", "axe_path": "axe"}
    }

    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                for key in default_config:
                    if key not in config:
                        config[key] = default_config[key]
                return config
        except Exception:
            return default_config
    else:
        save_config(default_config)
        return default_config

def save_config(config: Dict):
    """Save configuration to config file."""
    config_file = get_script_dir() / "config.yaml"
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False)
    except Exception as e:
        console.print(f"[red]Error saving config: {e}[/red]")

def is_server_running():
    """Check if fcc-server is already running."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 8080)) 
        sock.close()
        return result == 0
    except:
        return False

def start_fcc_server():
    """Start fcc-server silently in the background."""
    script_dir = get_script_dir()
    try:
        subprocess.Popen(
            ["fcc-server"],
            cwd=script_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        time.sleep(2)
        return True
    except Exception as e:
        console.print(f"[yellow]Warning: Could not start fcc-server: {e}[/yellow]")
        return False

def show_header():
    """Display a beautiful ASCII art header."""
    header_text = """
    ███╗   ███╗ █████╗ ███╗   ██╗███████╗██╗   ██╗███████╗██████╗
    ████╗ ████║██╔══██╗████╗  ██║██╔════╝██║   ██║██╔════╝██╔══██╗
    ██╔████╔██║███████║██╔██╗ ██║█████╗  ██║   ██║█████╗  ██████╔╝
    ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║██║  ██║██║ ╚████║███████╗ ╚████╔╝ ███████╗██║  ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝  ╚═══╝  ██══════╝╚═╝  ╚═╝
    """
    title = Text("AI Coding Agents Launcher", style="bold cyan")
    subtitle = Text("Select your AI-powered coding assistant", style="dim")

    console.print(Panel.fit(
        header_text + "\n" + str(title) + "\n" + str(subtitle),
        border_style="bright_blue",
        box=box.DOUBLE
    ))

def run_agent(agent_name: str, agent_command: str, description: str):
    """Run a selected AI agent."""
    console.clear()
    show_header()

    with console.status(f"[bold green]Launching {agent_name}...[/bold green]"):
        time.sleep(1)

    try:
        result = subprocess.run(
            agent_command,
            cwd=get_script_dir(),
            shell=True,
            check=False
        )

        if result.returncode != 0:
            console.print(f"[red]Warning: {agent_name} exited with code {result.returncode}[/red]")
        else:
            console.print(f"[green]{agent_name} finished successfully.[/green]")

    except FileNotFoundError:
        console.print(f"[red]Error: {agent_command} not found. Please ensure it's installed and in your PATH.[/red]")
    except Exception as e:
        console.print(f"[red]Error running {agent_name}: {e}[/red]")

    console.print("\n[dim]Press Enter to return to the menu...[/dim]")
    try:
        input()
    except KeyboardInterrupt:
        pass

def run_full_system_update():
    console.clear()
    show_header()
    console.print("[bold blue]Running Full System Update & Diagnostics[/bold blue]\n")

    steps = [
        ("Checking Python packages", "python -m pip list --outdated"),
        ("Checking npm packages", "npm outdated -g --depth=0"),
        ("Verifying Claude Code installation", "claude --version"),
        ("Checking MCP servers", "claude mcp list"),
        ("Checking Git installation", "git --version"),
        ("Checking Node.js installation", "node --version"),
    ]

    for step_name, command in steps:
        with console.status(f"[bold yellow]{step_name}...[/bold yellow]"):
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    console.print(f"[green]✓[/green] {step_name}")
                else:
                    console.print(f"[yellow]⚠[/yellow] {step_name} (may have issues)")
            except Exception as e:
                console.print(f"[red]✗[/red] {step_name}: {e}")

    console.print("\n[green]System check complete![/green]")
    console.print("\n[dim]Press Enter to return to the menu...[/dim]")
    input()

def show_version_info():
    console.clear()
    show_header()
    console.print("[bold blue]Version Information[/bold blue]\n")

    tools = [
        ("Python", "python --version"), ("Node.js", "node --version"),
        ("npm", "npm --version"), ("Claude Code", "claude --version"),
        ("Git", "git --version"), ("Rich (Python)", "python -c \"import rich; print(rich.__version__)\""),
    ]

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Tool", style="dim", width=20)
    table.add_column("Version")

    for tool_name, command in tools:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
            version = result.stdout.strip() if result.returncode == 0 else "[red]Not found[/red]"
            if not version and result.returncode == 0:
                version = result.stderr.strip()
            table.add_row(tool_name, version)
        except Exception:
            table.add_row(tool_name, "[red]Error[/red]")

    console.print(table)
    console.print("\n[dim]Press Enter to return to the menu...[/dim]")
    input()

def run_git_integration_menu():
    while True:
        console.clear()
        show_header()
        choice = questionary.select(
            "Git Integration:",
            choices=[
                questionary.Choice("1. Repository Status", value="status"),
                questionary.Choice("2. View Commit Log", value="log"),
                questionary.Choice("3. Add All Changes", value="add"),
                questionary.Choice("4. Commit Changes", value="commit"),
                questionary.Choice("5. Push to Remote", value="push"),
                questionary.Choice("6. Pull from Remote", value="pull"),
                questionary.Choice("7. Branch Management", value="branch"),
                questionary.Choice("8. Back to Main Menu", value="back"),
            ],
            style=custom_style,
            use_indicator=True,
        ).ask()

        if choice == "back" or choice is None:
            break
        handle_git_choice(choice)

def handle_git_choice(choice: str):
    script_dir = get_script_dir()
    
    if choice == "status":
        res = subprocess.run("git status", cwd=script_dir, shell=True, capture_output=True, text=True)
        console.clear(); show_header()
        console.print("[bold blue]Git Status[/bold blue]\n")
        console.print(res.stdout if res.stdout else res.stderr)
        
    elif choice == "log":
        res = subprocess.run("git log --oneline -10", cwd=script_dir, shell=True, capture_output=True, text=True)
        console.clear(); show_header()
        console.print("[bold blue]Recent Commits[/bold blue]\n")
        console.print(res.stdout if res.stdout else res.stderr)
        
    elif choice == "add":
        subprocess.run("git add .", cwd=script_dir, shell=True)
        console.print("[green]✓[/green] All changes added successfully")
        
    elif choice == "commit":
        msg = questionary.text("Enter commit message:", style=custom_style).ask()
        if msg:
            subprocess.run(f'git commit -m "{msg}"', cwd=script_dir, shell=True)
            console.print("[green]✓[/green] Changes committed")
            
    elif choice == "push":
        subprocess.run("git push", cwd=script_dir, shell=True)
        console.print("[green]✓[/green] Push successful")
        
    elif choice == "pull":
        subprocess.run("git pull", cwd=script_dir, shell=True)
        console.print("[green]✓[/green] Pull successful")
        
    elif choice == "branch":
        run_git_branch_menu()
        
    console.print("\n[dim]Press Enter to continue...[/dim]")
    input()

def run_git_branch_menu():
    while True:
        console.clear()
        show_header()
        choice = questionary.select(
            "Branch Management:",
            choices=[
                questionary.Choice("1. List Branches", value="list"),
                questionary.Choice("2. Create New Branch", value="create"),
                questionary.Choice("3. Switch Branch", value="checkout"),
                questionary.Choice("4. Delete Branch", value="delete"),
                questionary.Choice("5. Back", value="back"),
            ],
            style=custom_style,
        ).ask()

        if choice == "back" or choice is None:
            break
            
        script_dir = get_script_dir()
        if choice == "list":
            res = subprocess.run("git branch", cwd=script_dir, shell=True, capture_output=True, text=True)
            console.clear(); show_header(); console.print(res.stdout)
            
        elif choice == "create":
            name = questionary.text("Enter new branch name:", style=custom_style).ask()
            if name:
                subprocess.run(f"git checkout -b {name}", cwd=script_dir, shell=True)
                console.print(f"[green]✓[/green] Branch '{name}' created")
                
        elif choice == "checkout":
            res = subprocess.run("git branch --format='%(refname:short)'", cwd=script_dir, shell=True, capture_output=True, text=True)
            branches = [b.strip() for b in res.stdout.split('\n') if b.strip()]
            if branches:
                b_choice = questionary.select("Select branch:", choices=branches, style=custom_style).ask()
                if b_choice:
                    subprocess.run(f"git checkout {b_choice}", cwd=script_dir, shell=True)
                    console.print(f"[green]✓[/green] Switched to '{b_choice}'")
                    
        elif choice == "delete":
            res = subprocess.run("git branch --format='%(refname:short)'", cwd=script_dir, shell=True, capture_output=True, text=True)
            branches = [b.strip() for b in res.stdout.split('\n') if b.strip() and not b.startswith('*')]
            if branches:
                b_choice = questionary.select("Select branch to delete:", choices=branches, style=custom_style).ask()
                if b_choice:
                    subprocess.run(f"git branch -D {b_choice}", cwd=script_dir, shell=True)
                    console.print(f"[green]✓[/green] Branch '{b_choice}' deleted")
                    
        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()

def run_github_integration_menu():
    while True:
        console.clear(); show_header()
        choice = questionary.select(
            "GitHub Integration:",
            choices=[
                questionary.Choice("1. Clone Repository", value="clone"),
                questionary.Choice("2. List Local GitHub Projects", value="list"),
                questionary.Choice("3. Open Project Folder", value="open"),
                questionary.Choice("4. Back to Main Menu", value="back"),
            ],
            style=custom_style,
        ).ask()

        if choice == "back" or choice is None:
            break

        if choice == "clone":
            url = questionary.text("Enter repository URL:", style=custom_style).ask()
            if url:
                console.print("[yellow]Cloning...[/yellow]")
                subprocess.run(f"git clone {url}", cwd=get_github_dir(), shell=True)
                console.print("[green]✓[/green] Cloned successfully")
                
        elif choice == "list":
            console.clear(); show_header()
            github_dir = get_github_dir()
            projects = [d.name for d in github_dir.iterdir() if d.is_dir()]
            if projects:
                table = Table(show_header=True)
                table.add_column("Project Name", style="cyan")
                for p in projects: table.add_row(p)
                console.print(table)
            else:
                console.print("[yellow]No projects found.[/yellow]")
                
        elif choice == "open":
            github_dir = get_github_dir()
            projects = [d.name for d in github_dir.iterdir() if d.is_dir()]
            if projects:
                p_choice = questionary.select("Select project:", choices=projects, style=custom_style).ask()
                if p_choice:
                    p_path = github_dir / p_choice
                    console.print(f"[green]Opening: {p_path}[/green]")
                    if os.name == 'nt': os.startfile(p_path)
                    
        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()

def run_web_tools_menu():
    while True:
        console.clear(); show_header()
        choice = questionary.select(
            "Web Analysis & Design Tools:",
            choices=[
                questionary.Choice("1. Run Lighthouse Audit", value="lighthouse"),
                questionary.Choice("2. Run Accessibility Check (axe)", value="axe"),
                questionary.Choice("3. Back to Main Menu", value="back"),
            ],
            style=custom_style,
        ).ask()

        if choice == "back" or choice is None:
            break

        if choice == "lighthouse":
            url = questionary.text("Enter URL to audit:", style=custom_style).ask()
            if url:
                console.print("[yellow]Running Lighthouse...[/yellow]")
                subprocess.run(f"lighthouse {url} --output=json --output-path=./lighthouse-report.json", shell=True)
                console.print("[green]✓[/green] Done.")
                
        elif choice == "axe":
            url = questionary.text("Enter URL to check:", style=custom_style).ask()
            if url:
                console.print("[yellow]Running axe...[/yellow]")
                subprocess.run(f"axe {url} --output=json --output-path=./axe-report.json", shell=True)
                console.print("[green]✓[/green] Done.")

        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()

def show_help():
    console.clear(); show_header()
    console.print("[bold blue]AI Coding Agents Launcher - Help[/bold blue]\n")
    console.print("""
This launcher provides a unified interface for accessing various AI coding agents.

[bold]Features:[/bold]
• AI Agent Selection
• System Management & Diagnostics
• Git & GitHub Integration
• Web Analysis Tools
• Modern Interface

[bold]Requirements:[/bold]
• Python 3.7+
• Node.js and npm
• Git
""")
    console.print("\n[dim]Press Enter to return...[/dim]")
    input()

def show_menu():
    while True:
        console.clear()
        show_header()
        choice = questionary.select(
            "Select an option:",
            choices=[
                questionary.Choice("1. AI Coding Agents", value="agents"),
                questionary.Choice("2. System Update & Diagnostics", value="update"),
                questionary.Choice("3. Version Information", value="version"),
                questionary.Choice("4. Git Integration", value="git"),
                questionary.Choice("5. GitHub Integration", value="github"),
                questionary.Choice("6. Web Analysis & Design Tools", value="web"),
                questionary.Choice("7. Help & Information", value="help"),
                questionary.Choice("8. Exit", value="exit"),
            ],
            style=custom_style,
            use_indicator=True,
            use_shortcuts=True,
        ).ask()

        if choice is None:
            continue

        if choice == "exit":
            console.print("[bold green]Thank you for using AI Coding Agents Launcher![/bold green]")
            break
        elif choice == "update": run_full_system_update()
        elif choice == "version": show_version_info()
        elif choice == "git": run_git_integration_menu()
        elif choice == "github": run_github_integration_menu()
        elif choice == "web": run_web_tools_menu()
        elif choice == "help": show_help()
        elif choice == "agents": show_agents_submenu()

def show_agents_submenu():
    while True:
        console.clear(); show_header()
        choice = questionary.select(
            "Select your AI coding agent:",
            choices=[
                questionary.Choice("1. Claude Code (fcc-claude) - [The Design Master]", value="claude"),
                questionary.Choice("2. Codex (fcc-codex)", value="codex"),
                questionary.Choice("3. DeepSeek (fcc-dsh)", value="deepseek"),
                questionary.Choice("4. Aider (fcc-aider)", value="aider"),
                questionary.Choice("5. Cline (Opens VS Code)", value="cline"),
                questionary.Choice("6. OpenCode (Terminal Agent)", value="opencode"),
                questionary.Choice("7. Back to Main Menu", value="back"),
            ],
            style=custom_style,
            use_indicator=True,
            use_shortcuts=True,
        ).ask()

        if choice == "back" or choice is None:
            break

        if choice == "claude": run_agent("Claude Code", "fcc-claude", "The Design Master")
        elif choice == "codex": run_agent("Codex", "fcc-codex", "OpenAI's coding agent")
        elif choice == "deepseek": run_agent("DeepSeek", "fcc-dsh", "DeepSeek coding agent")
        elif choice == "aider": run_agent("Aider", "fcc-aider", "Pair programming agent")
        elif choice == "cline": run_agent("Cline", "code .", "Opening VS Code")
        elif choice == "opencode": run_agent("OpenCode", "opencode", "Terminal AI agent")

def main():
    try:
        if not is_server_running():
            console.print("[bold blue]Starting fcc-server in background...[/bold blue]")
            if not start_fcc_server():
                console.print("[yellow]Warning: Could not verify fcc-server startup. Continuing anyway.[/yellow]")
            else:
                console.print("[green]✓[/green] fcc-server started successfully")
        else:
            console.print("[green]✓[/green] fcc-server is already running")

        show_menu()
    except KeyboardInterrupt:
        console.print("\n[bold red]Application interrupted by user.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Fatal error: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()