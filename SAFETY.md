# NovaStrap Safety & Security Information

## 🛡️ Is NovaStrap Safe?

**YES! NovaStrap is 100% safe to use.**

### Why You Can Trust NovaStrap

✅ **Open Source** - All code is publicly available for review
✅ **No Malware** - Completely clean, no viruses or trojans
✅ **No Data Collection** - Zero telemetry, no tracking
✅ **No Network Access** - Operates locally only
✅ **No Admin Required** - Runs with normal user permissions
✅ **Transparent Operations** - All actions logged clearly

---

## 🔍 What NovaStrap Does

NovaStrap is a simple file editor that:
1. Edits a local JSON file (`IxpSettings.json`)
2. Creates backups automatically
3. Launches Roblox (optional)
4. Logs everything to a local file

**That's it!** No hidden features, no background processes, no data sent anywhere.

---

## ⚠️ Windows Defender Warning

### "Windows protected your PC"

You might see this warning when running NovaStrap.exe:

```
Windows protected your PC
Microsoft Defender SmartScreen prevented an unrecognized app from starting.
```

**This is a FALSE POSITIVE.** Here's why:

### Why This Happens
1. **PyInstaller apps** are often flagged by antivirus (common issue)
2. **New files** without digital signatures trigger warnings
3. **Windows SmartScreen** blocks apps from unknown publishers
4. **NovaStrap is new** - not yet recognized by Microsoft

### How to Run It Safely

**Option 1: Click "More info" → "Run anyway"**
```
1. Click "More info" on the warning
2. Click "Run anyway" button
3. NovaStrap will open normally
```

**Option 2: Add to Exclusions**
```
1. Open Windows Security
2. Go to "Virus & threat protection"
3. Click "Manage settings"
4. Scroll to "Exclusions"
5. Add NovaStrap.exe
```

**Option 3: Build It Yourself**
```
If you're still worried, build from source:
1. Download the source code
2. Run: python main.py
3. Or build: pyinstaller NovaStrap.spec
```

---

## 🔐 Security Features

### What NovaStrap DOES NOT Do

❌ **No Internet Connections** - Never connects to any server
❌ **No Data Collection** - Doesn't track your usage
❌ **No Keylogging** - Doesn't record your keyboard
❌ **No Screenshots** - Doesn't capture your screen
❌ **No File Access** - Only touches Roblox ClientSettings folder
❌ **No Registry Changes** - Doesn't modify Windows registry
❌ **No Admin Access** - Runs with normal permissions
❌ **No Hidden Processes** - No background services

### What NovaStrap DOES Do

✅ **Edits One File** - `%LOCALAPPDATA%\Roblox\ClientSettings\IxpSettings.json`
✅ **Creates Backups** - Saves old versions with timestamps
✅ **Validates JSON** - Checks your input before saving
✅ **Logs Operations** - Records what it does (locally)
✅ **Launches Roblox** - Uses standard Windows process launching

---

## 🧪 Verification

### Scan It Yourself

Feel free to scan NovaStrap.exe with:
- **Windows Defender** (built-in)
- **VirusTotal.com** (upload and scan)
- **Any antivirus software**

You'll find it's completely clean.

### Check the Source Code

All source code is available:
- Review every line on GitHub
- No obfuscation or hidden code
- Well-commented and documented
- Standard Python libraries only

### Build It Yourself

Don't trust pre-built executables? Build your own:

```bash
1. git clone https://github.com/YourName/NovaStrap
2. pip install -r requirements.txt
3. python create_icon.py
4. pyinstaller NovaStrap.spec
5. dist/NovaStrap.exe (your own build!)
```

---

## 📝 Privacy

### What Data Does NovaStrap Store?

**Locally on your PC:**
- Log file (`fflag_editor.log`) with operation timestamps
- Backup files (`.bak.YYYYMMDD_HHMMSS.json`)
- Your JSON settings (what you paste in the editor)

**That's all!** Everything stays on your computer.

### What Data Does NovaStrap Send?

**NOTHING.** Zero data sent anywhere.
- No analytics
- No crash reports
- No usage statistics
- No telemetry
- No network connections at all

---

## 🎯 What NovaStrap Accesses

### File System
- **Reads**: `%LOCALAPPDATA%\Roblox\ClientSettings\IxpSettings.json`
- **Writes**: Same file (with backups)
- **Creates**: Log file in NovaStrap folder
- **Nothing else**

### Processes
- **Checks** if Roblox is running (read-only)
- **Launches** RobloxPlayerBeta.exe (if you click Launch button)
- **Nothing else**

### Network
- **NONE** - NovaStrap makes zero network connections

---

## ⚖️ Legal & Disclaimer

### Use at Your Own Risk

NovaStrap modifies Roblox configuration files:
- This may violate Roblox Terms of Service
- Incorrect FFlags can cause Roblox to crash
- Use responsibly and at your own discretion

### No Warranty

NovaStrap is provided "AS-IS" without warranty:
- Not responsible for game bans
- Not responsible for crashes
- Not responsible for data loss
- Use at your own risk

### Open Source

NovaStrap is open source software:
- Free to use, modify, and distribute
- MIT License (permissive)
- Contributions welcome
- No hidden costs or fees

---

## 🚨 Reporting Issues

### Found a Bug?
- Open an issue on GitHub
- Describe what happened
- Include log file if relevant

### Security Concern?
- Contact the maintainer directly
- Provide details privately
- Responsible disclosure appreciated

---

## 📚 Additional Resources

### Documentation
- **README.md** - Full feature documentation
- **QUICKSTART.md** - Getting started guide
- **BUILD_INSTRUCTIONS.md** - Build from source

### Community
- **GitHub Issues** - Bug reports and questions
- **GitHub Discussions** - General chat
- **Source Code** - Review and contribute

---

## ✅ Summary

**NovaStrap is safe because:**
1. ✅ Open source - all code visible
2. ✅ Local-only - no network access
3. ✅ No data collection - complete privacy
4. ✅ Simple operations - just file editing
5. ✅ Transparent logging - see everything it does
6. ✅ Can build yourself - verify safety personally

**Windows Defender warnings are false positives** - common with PyInstaller apps.

**You're in control** - review code, scan files, or build yourself.

---

## 🙋 Still Have Concerns?

**Don't trust pre-built .exe files?**
→ Build from source using Python!

**Want to verify safety?**
→ Scan with VirusTotal or any antivirus

**Need to review code?**
→ Check GitHub repository

**Have questions?**
→ Ask in GitHub Discussions

---

**NovaStrap - Safe, Open, Transparent**

Made with ❤️ by Nova

