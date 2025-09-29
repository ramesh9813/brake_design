@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

rem === Get repo name from current folder ===
for %%I in ("%cd%") do set repo_name=%%~nxI

rem === Get GitHub username from gh CLI ===
for /f "tokens=*" %%u in ('gh api user --jq ".login"') do set gh_user=%%u

echo.
echo Create repository as:
echo [1] Public
echo [2] Private
echo.
set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" (
    set visibility=--public
    echo Creating PUBLIC repository...
) else if "%choice%"=="2" (
    set visibility=--private
    echo Creating PRIVATE repository...
) else (
    echo Invalid choice! Defaulting to PUBLIC.
    set visibility=--public
)

echo.
if not exist .git (
    echo Initializing git repository...
    git init
    set fresh_init=1
) else (
    echo Git repository already initialized.
    set fresh_init=0
)

echo.
echo Checking for changes...
git diff-index --quiet HEAD -- 2>nul
if %errorlevel% neq 0 (
    echo Changes detected. Committing...
    set /p commit_msg="Enter commit message (press Enter for 'first commit'): "
    if "!commit_msg!"=="" set commit_msg=first commit
    git add .
    git commit -m "!commit_msg!"
) else (
    echo No changes to commit.
)

echo.
echo Checking if GitHub repository exists for %gh_user%/%repo_name%...
gh repo view %gh_user%/%repo_name% >nul 2>&1
if %errorlevel% neq 0 (
    echo Repository not found. Creating on GitHub...
    gh repo create %repo_name% %visibility% --source=. --remote=origin --push
) else (
    echo Repository already exists on GitHub. Pushing changes...
    git remote add origin https://github.com/%gh_user%/%repo_name%.git 2>nul
    git push -u origin master
)

endlocal
