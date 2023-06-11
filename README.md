# Unreal Python plugin template
A minimalism template for pure Python plugins in Unreal.<br>
Example repo using this template: [unrealScriptEditor-plugin](https://github.com/hannesdelbeke/unrealScriptEditor-plugin)

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

### (OPTIONAL) Add Plugget install support
To support 1-click install & automatically install all dependencies in the `requirements.txt` file, you can add [plugget](https://github.com/hannesdelbeke/plugget) support.
1. Upload your plugin to a repo.
2. Create a plugget manifest ([sample manifest](https://github.com/hannesdelbeke/plugget-pkgs/blob/main/unreal/unreal-script-editor/latest.json)) that points to your repo, and make a PR in [plugget-pkgs](https://github.com/hannesdelbeke/plugget-pkgs)
3. Add the plugget-install instructions to your README: 

> Installation with plugget automatically installs all dependencies.
> 1. Install the [plugget Unreal plugin](https://github.com/hannesdelbeke/plugget-unreal)
> 2. Run these 2 Python commands: (in the bottom left of the Unreal editor) 
> ```python
> import plugget
> plugget.install("unreal-script-editor")
> ```

### Community
- unreal forum [thread](https://forums.unrealengine.com/t/made-a-python-plugin-template/1089878)
