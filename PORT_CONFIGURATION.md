# Port Configuration Guide

## Quick Start Options

### Option 1: Start on Fixed Port (8502)
```bash
.\start.bat
```
- Opens app at http://localhost:8502
- Fails if port 8502 is already in use

### Option 2: Auto-Find Available Port (Recommended)
```bash
.\start_auto_port.bat
```
**OR** (PowerShell - more reliable):
```powershell
.\start_auto_port.ps1
```
- Automatically tries ports 8502-8510
- Uses the first available port
- Shows which port was selected

### Option 3: Manual Port Selection
```bash
py -3 -m streamlit run main.py --server.port=YOUR_PORT
```
Replace `YOUR_PORT` with any port number (e.g., 8503, 8504, etc.)

## Common Port Conflicts

**Problem:** "Port 8501 is already in use"
**Solution:** Use one of the scripts above, or manually specify a different port

**Problem:** Multiple Streamlit apps running
**Solution:** Use `start_auto_port.ps1` - it will find the next available port

## Configuration Files

### `.streamlit/config.toml`
Current configuration:
- **Default Port:** 8502 (changed from 8501 to avoid conflicts)
- **Headless:** true (required for Streamlit Cloud)
- **File Watcher:** poll (works with OneDrive)
- **Auto-reload:** enabled

### For Local Development Only
If you want the browser to auto-open when running locally, you can temporarily change:
```toml
headless = false
```

⚠️ **Important:** Change it back to `true` before pushing to GitHub/Streamlit Cloud!

## Troubleshooting

### Check What's Using a Port
**PowerShell:**
```powershell
Get-NetTCPConnection -LocalPort 8502 | Select-Object OwningProcess, State
```

**Command Prompt:**
```cmd
netstat -ano | findstr :8502
```

### Kill Process on Specific Port
Find the PID from the command above, then:
```powershell
Stop-Process -Id PID_NUMBER -Force
```

### Clear Streamlit Cache
If the app behaves strangely:
1. Press **C** in the running terminal
2. Or manually: `streamlit cache clear`

## Deployment to Streamlit Cloud

When deploying to Streamlit Cloud:
- Port configuration is **ignored** (Cloud assigns automatically)
- `headless = true` is **required**
- The app uses the settings from `.streamlit/config.toml` in your repo

## Quick Reference

| Script | Port Selection | Best For |
|--------|---------------|----------|
| `start.bat` | Fixed (8502) | Single app, quick start |
| `start_auto_port.bat` | Auto (8502-8510) | Multiple apps |
| `start_auto_port.ps1` | Auto (8502-8510) | Most reliable option |
| Manual command | Your choice | Custom setup |

---
**Last Updated:** 2025-11-04
