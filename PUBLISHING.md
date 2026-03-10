# PyPI Publishing Guide

## 🔑 Get Your API Token

1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Give it a name (e.g., "asciify-upload")
4. Select scope: "Entire account" or specific project
5. Copy the generated token (starts with `pypi-`)

## 🔐 Setup Environment Variables

### Option 1: Using .env file (Recommended)

1. Edit the `.env` file in this directory
2. Replace the placeholder with your actual token:
   ```
   TWINE_USERNAME=__token__
   TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmcCJ...your-actual-token-here
   ```

### Option 2: Set environment variables manually (PowerShell)

```powershell
$env:TWINE_USERNAME="__token__"
$env:TWINE_PASSWORD="pypi-your-actual-token-here"
```

### Option 3: Set environment variables manually (Command Prompt)

```cmd
set TWINE_USERNAME=__token__
set TWINE_PASSWORD=pypi-your-actual-token-here
```

## 📦 Build and Upload

### Using the automated script (Recommended):
```powershell
.\upload.ps1
```

### Manual steps:
```powershell
# Install build tools (if not already installed)
pip install hatchling twine

# Build the package
hatch build

# Upload to PyPI
twine upload dist/*
```

## ✅ Verify Upload

After uploading, verify your package at:
- https://pypi.org/project/asciify/

## 🚀 Install from PyPI

Once uploaded, users can install with:
```bash
pip install asciify
```

## 🔒 Security Notes

- ⚠️ **NEVER** commit your `.env` file to Git (already in `.gitignore`)
- ⚠️ **NEVER** share your API token publicly
- 🔐 Keep your token secure and regenerate if compromised
- 📝 Use different tokens for different projects

## 🆘 Troubleshooting

### Error: 403 Forbidden
- Check that your token is correct and not expired
- Ensure you're using `__token__` as username
- Verify you have permission to upload to the project

### Error: Package already exists
- Increment the version number in `pyproject.toml`
- Run `hatch build` again
- Try uploading again

### Error: Invalid classifier
- Check that all classifiers in `pyproject.toml` are valid
- See https://pypi.org/classifiers/ for valid options
