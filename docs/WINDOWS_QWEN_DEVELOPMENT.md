# Windows PowerShell: Qwen + OpenRouter + Pi for software development

Checked 19 November 2026. This recreates the previous **Pi coding agent / OpenRouter / Qwen** workflow, without downloading Qwen or requiring a local GPU. OpenRouter inference may incur token charges.

## Quick start in PowerShell

Install missing dependencies (skip any already installed):

~~~powershell
winget install --id Git.Git --exact --source winget
winget install --id OpenJS.NodeJS.LTS --exact --source winget
winget install --id GitHub.cli --exact --source winget
~~~

Close and reopen PowerShell to refresh PATH. Then:

~~~powershell
npm.cmd install -g @mariozechner/pi-coding-agent
New-Item -ItemType Directory -Force "$HOME\source" | Out-Null
Set-Location "$HOME\source"
git clone https://github.com/Parris-Tech-Services/RepublicOfParristan.git
Set-Location .\RepublicOfParristan
pi.cmd --provider openrouter --model qwen/qwen3-coder-30b-a3b-instruct
~~~

When the repository already exists, go directly to its folder instead of cloning again. Inside Pi, run **/login openrouter** if authentication is needed, then **/model** to confirm the active OpenRouter/Qwen choice. Use an OpenRouter **inference** credential, not a management credential: our previous mistaken key type produced a 401 User not found error.

You can also run the repo's repeatable bootstrap script, once this repository is cloned:

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup-qwen-openrouter.ps1
~~~

It installs missing Git, Node and GitHub CLI via winget, installs Pi via npm, and clones or preserves the local checkout. It does not obtain/store credentials, push code or change public civic records. Read the script first.

## GitHub code workflow

Sign in for write access using:

~~~powershell
gh auth login
git status --short
git switch -c feature/first-civic-app
~~~

After editing and testing, review every change and open a pull request:

~~~powershell
git diff
py -3 scripts/validate_gazette.py
git add -A
git commit -m "feat: implement Parristan prototype"
git push -u origin HEAD
gh pr create --fill
~~~

No credentials, identities, citizen records or private data belong in this public repository. Merge only after reviewing the changed files and relevant checks.

## Good first instruction to Pi

> Read AGENTS.md, the public Gazette, the founding checklist and the reference stack matrix. Implement a small accessible working prototype for an exportable Markdown/JSON public decision register, preserving the distinction between proposed and ratified measures. Do not fabricate elections, citizenship, ministerial appointments or statehood. Test the changes, show the diff and open a PR only when verified.

**Default model:** [Qwen3 Coder 30B A3B Instruct](https://openrouter.ai/qwen/qwen3-coder-30b-a3b-instruct), provider/model: qwen/qwen3-coder-30b-a3b-instruct. The earlier fast alternative was qwen/qwen3.7-flash; use /model to confirm availability before selecting it.

Sources: [Pi coding agent](https://github.com/badlogic/pi-mono), [OpenRouter available models](https://openrouter.ai/models), [OpenRouter API key console](https://openrouter.ai/settings/keys).
