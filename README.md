# Unreal Python plugin template
A minimalism template for pure Python plugins in Unreal.<br>
For more advanced C++ templates see [UnrealExtenstionPluginsTemplates](https://github.com/laycnc/UnrealExtenstionPluginsTemplates)

### Content
```
📂 MyPlugin
├── 📂 Content
│   └── 📂 Python
│       └── 📄 init_unreal.py
├── 📂 Resources
│   └── 🖼️ icon128.png
└── 📄 MyPlugin.uplugin
📄 .gitignore
📄 README.md
📄 requirements.txt
```

### Info
- `MyPlugin` rename the folder to your plugin name. Unreal's naming convention uses PascalCase.
- `MyPlugin.uplugin` Rename this file to your plugin name, and open it with a text editor & edit the content.
- `.gitignore` is setup to prevent unneeded python files from being commit to your git-repo.
- `requirements.txt` Add your pip/pypi dependencies to this file, delete it if not used.
- `README.md`: include an image & description, so people see what's your plugin about.
