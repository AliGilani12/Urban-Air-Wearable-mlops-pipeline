# Helper script to use npm from custom location
# Usage: .\use-npm.ps1 install
#        .\use-npm.ps1 run dev
#        .\use-npm.ps1 <any-npm-command>

$npmPath = "D:\Coding softwares\npm.cmd"

if ($args.Count -eq 0) {
    Write-Host "Usage: .\use-npm.ps1 <npm-command>" -ForegroundColor Yellow
    Write-Host "Example: .\use-npm.ps1 install" -ForegroundColor Yellow
    Write-Host "Example: .\use-npm.ps1 run dev" -ForegroundColor Yellow
    exit 1
}

& $npmPath $args

