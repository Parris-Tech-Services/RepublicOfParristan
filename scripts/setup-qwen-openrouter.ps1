# Parristan Windows Pi + Qwen developer bootstrap, PowerShell 5.1+.
# Run from any folder. Does not capture API keys or push anything.
[CmdletBinding()]
param([string]$Model = "qwen/qwen3-coder-30b-a3b-instruct")
$ErrorActionPreference = "Stop"
$restart = $false

function Ensure-Tool {
    param([string]$Command, [string]$Package)
    if (Get-Command $Command -ErrorAction SilentlyContinue) {
        Write-Host "[OK] $Command"
        return
    }
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "winget not found. Install Windows Package Manager before this script."
    }
    Write-Host "[INSTALL] $Package"
    & winget install --id $Package --exact --source winget --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { throw "winget failed installing $Package" }
    $script:restart = $true
}

Ensure-Tool "git.exe" "Git.Git"
Ensure-Tool "node.exe" "OpenJS.NodeJS.LTS"
Ensure-Tool "gh.exe" "GitHub.cli"
if ($restart) {
    Write-Host "Open a NEW PowerShell and run this script again to refresh PATH."
    exit 0
}
if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) {
    throw "npm.cmd missing. Reopen PowerShell after Node.js installation."
}
& npm.cmd install --global @mariozechner/pi-coding-agent
if ($LASTEXITCODE -ne 0) { throw "npm failed installing Pi." }
$prefix = (& npm.cmd prefix --global).Trim()
$pi = Join-Path $prefix "pi.cmd"
if (-not (Test-Path $pi)) {
    $found = Get-Command pi.cmd -ErrorAction SilentlyContinue
    if (-not $found) { throw "Pi installed, but pi.cmd was not found. Check the global npm directory." }
    $pi = $found.Source
}
& $pi --version
if ($LASTEXITCODE -ne 0) { throw "Pi CLI version check failed." }

$target = Join-Path (Join-Path $HOME "source") "RepublicOfParristan"
if (-not (Test-Path $target)) {
    New-Item -ItemType Directory -Force (Split-Path $target -Parent) | Out-Null
    & git.exe clone "https://github.com/Parris-Tech-Services/RepublicOfParristan.git" $target
    if ($LASTEXITCODE -ne 0) { throw "Git clone failed." }
} elseif (-not (Test-Path (Join-Path $target ".git"))) {
    throw "The target exists but is not a git clone: $target"
} else {
    Write-Host "[OK] Existing checkout preserved: $target"
}
Write-Host ""
Write-Host "[READY] Paste these two commands:"
Write-Host ('Set-Location "' + $target + '"')
Write-Host ('& "' + $pi + '" --provider openrouter --model ' + $Model)
Write-Host "Inside Pi: /login openrouter if needed, then /model to confirm Qwen."
Write-Host "For GitHub write access: gh auth login"
