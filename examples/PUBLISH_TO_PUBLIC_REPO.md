# Publishing to Public GitHub Repo

This guide contains the commands to publish the SDK and examples from the private repo to the public GradientCast organization repo.

**Private repo:** `https://github.com/giulioGC/gradientcast.git`
**Public repo:** `https://github.com/GradientCast/gradientcast.git`

---

## Prerequisites

1. Create the public repo at https://github.com/organizations/GradientCast/repositories/new
   - Name: `gradientcast`
   - Public visibility
   - No README, .gitignore, or license (we'll push everything)

2. Make sure you have push access to the public repo

---

## Commands (Windows PowerShell)

```powershell
# 1. Create temp directory and initialize git
cd c:/Users/giuli
mkdir gradientcast-public
cd gradientcast-public
git init

# 2. Copy SDK source code
Copy-Item -Recurse ../gradientcast/gradientcast-sdk/gradientcast ./gradientcast
Copy-Item ../gradientcast/gradientcast-sdk/pyproject.toml .
Copy-Item ../gradientcast/gradientcast-sdk/setup.py .
Copy-Item ../gradientcast/gradientcast-sdk/LICENSE .
Copy-Item ../gradientcast/gradientcast-sdk/requirements.txt .

# 3. Copy examples (excluding the org readme and this file)
Copy-Item -Recurse ../gradientcast/examples ./examples
Remove-Item ./examples/GITHUB_ORG_README.md
Remove-Item ./examples/PUBLISH_TO_PUBLIC_REPO.md

# 4. Use landing page README
Copy-Item ../gradientcast/examples/GITHUB_ORG_README.md ./README.md

# 5. Create .gitignore
@"
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.ipynb_checkpoints/
.env
"@ | Out-File -FilePath .gitignore -Encoding utf8

# 6. Commit and push to public repo
git add .
git commit -m "Initial public release: SDK + examples"
git branch -M main
git remote add origin https://github.com/GradientCast/gradientcast.git
git push -u origin main
```

---

## Updating the Public Repo

When you make changes to the SDK or examples in the private repo and want to update the public repo:

```powershell
# Navigate to the public repo directory
cd c:/Users/giuli/gradientcast-public

# Remove old files (keep .git)
Get-ChildItem -Exclude .git | Remove-Item -Recurse -Force

# Re-copy everything
Copy-Item -Recurse ../gradientcast/gradientcast-sdk/gradientcast ./gradientcast
Copy-Item ../gradientcast/gradientcast-sdk/pyproject.toml .
Copy-Item ../gradientcast/gradientcast-sdk/setup.py .
Copy-Item ../gradientcast/gradientcast-sdk/LICENSE .
Copy-Item ../gradientcast/gradientcast-sdk/requirements.txt .
Copy-Item -Recurse ../gradientcast/examples ./examples
Remove-Item ./examples/GITHUB_ORG_README.md
Remove-Item ./examples/PUBLISH_TO_PUBLIC_REPO.md
Copy-Item ../gradientcast/examples/GITHUB_ORG_README.md ./README.md

# Recreate .gitignore
@"
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.ipynb_checkpoints/
.env
"@ | Out-File -FilePath .gitignore -Encoding utf8

# Commit and push
git add .
git commit -m "Update SDK and examples"
git push
```

---

## Public Repo Structure

```
gradientcast/                  # repo root
├── README.md                  # Landing page (from GITHUB_ORG_README.md)
├── gradientcast/              # SDK source code
│   ├── __init__.py
│   ├── client.py
│   ├── types.py
│   ├── _base.py
│   ├── _exceptions.py
│   ├── _pandas.py
│   └── _version.py
├── examples/                  # Tutorials and notebooks
│   ├── quickstart.ipynb
│   ├── README.md
│   ├── forecasting/
│   ├── anomaly_detection/
│   └── utils/
├── pyproject.toml
├── setup.py
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

## Notes

- The `GITHUB_ORG_README.md` file has been updated with relative links that work in the single-repo structure
- Private files (model deployments, configs) are NOT copied to the public repo
- This file (`PUBLISH_TO_PUBLIC_REPO.md`) is excluded from the public repo
