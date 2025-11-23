# ⚠️ Node.js Installation Required

## Current Status

Node.js and npm are **not installed** on your system. You need to install them before you can run the frontend.

## Quick Fix

### Option 1: Install Node.js (Recommended - 5 minutes)

1. **Download Node.js:**
   - Visit: https://nodejs.org/
   - Download the **LTS version** (recommended)
   - File will be something like: `node-v20.x.x-x64.msi`

2. **Install:**
   - Run the downloaded `.msi` file
   - Follow the installation wizard (click Next, Next, Install)
   - **Make sure "Add to PATH" is checked** ✅
   - Finish installation

3. **Restart Terminal:**
   - **Close your current PowerShell window**
   - **Open a new PowerShell window**
   - This is important! PATH changes require a new terminal session

4. **Verify Installation:**
   ```powershell
   node --version
   npm --version
   ```
   Should show version numbers.

5. **Install Dependencies:**
   ```powershell
   npm install
   ```

### Option 2: Check if Already Installed Elsewhere

Sometimes Node.js is installed but not in PATH. Check:

```powershell
# Check common installation locations
Test-Path "C:\Program Files\nodejs\node.exe"
Test-Path "C:\Program Files (x86)\nodejs\node.exe"
```

If either returns `True`, Node.js is installed but not accessible. You can either:
- Add it to PATH manually
- Use full path: `"C:\Program Files\nodejs\npm.cmd" install`

## After Installation

Once Node.js is installed, come back to this folder and run:

```powershell
npm install
```

Then follow the instructions in `QUICK_START.md` to run the application.

## Need Detailed Instructions?

See `../INSTALL_NODEJS.md` for complete installation guide with troubleshooting.

---

**Status**: ⏸️ Waiting for Node.js installation
**Next Step**: Install Node.js from https://nodejs.org/

