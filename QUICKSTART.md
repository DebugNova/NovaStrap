# NovaStrap - Quick Start Guide

**Made by Nova**

## Getting Started in 3 Steps

### 1. Install Python
- Download Python 3.10+ from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"
- Verify installation: Open Command Prompt and type `python --version`

### 2. Install Dependencies
Open Command Prompt in this folder and run:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
**Option A:** Double-click `run.bat`

**Option B:** In Command Prompt:
```bash
python main.py
```

## First Use

1. **Accept the disclaimer** about risks and terms of service
2. **The path will be auto-detected** - you should see something like:
   ```
   C:\Users\YourName\AppData\Local\Roblox\ClientSettings\IxpSettings.json
   ```

3. **Paste your FFlags** - Example:
   ```json
   {
     "FFlagDebugGraphicsPreferVulkan": "True",
     "DFIntTaskSchedulerTargetFps": "144"
   }
   ```

4. **Click "🔍 Validate"** to check for errors

5. **Click "💾 Save & Apply"** to save the configuration

6. **Click "🚀 Launch Roblox"** to start the game with your settings!
   - Or restart Roblox manually for changes to take effect

## Important Notes

⚠️ **Always close Roblox before saving FFlags**

✅ **Backups are automatic** - every save creates a timestamped backup

🔒 **Files are set to read-only** - this is normal and intentional

## Common FFlag Examples

### Enable Vulkan Graphics
```json
{
  "FFlagDebugGraphicsPreferVulkan": "True"
}
```

### Set Custom FPS Cap
```json
{
  "DFIntTaskSchedulerTargetFps": "144"
}
```

### Multiple FFlags
```json
{
  "FFlagDebugGraphicsPreferVulkan": "True",
  "DFIntTaskSchedulerTargetFps": "144",
  "FFlagDebugDisableTelemetryEphemeralCounter": "True"
}
```

## Troubleshooting

### "Failed to resolve Roblox paths"
- Install Roblox first
- Ensure it's in the default location

### "ModuleNotFoundError: No module named 'PyQt6'"
- Run: `pip install -r requirements.txt`

### Changes not working
1. Close Roblox completely (check Task Manager)
2. Save FFlags again
3. Restart Roblox

## Need Help?

- Check `fflag_editor.log` for detailed error messages
- See full documentation in `README.md`
- Verify your JSON syntax at [jsonlint.com](https://jsonlint.com)

---

**Ready to go?** Just double-click `run.bat` or run `python main.py`!

