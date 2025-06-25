# Unreal Python plugin template
A minimalistic template for pure Python plugins in Unreal.<br>
Example repos using this template: 
- [unrealScriptEditor-plugin](https://github.com/hannesdelbeke/unrealScriptEditor-plugin)
- [texture-browser-unreal-plugin](https://github.com/hannesdelbeke/texture-browser-unreal-plugin)
- [unreal-qt-plugin](https://github.com/hannesdelbeke/unreal-qt-plugin)
- [plugget-unreal-plugin](https://github.com/plugget/plugget-unreal-plugin)


### Content
```python
📂 MyPlugin
├── 📂 Content
│   └── 📂 Python
│       └── 📄 init_unreal.py  # customise startup logic
│       └── 📄 my_module.py  # customise this Qt Widget
│       └── 📄 requirements.txt  # add your dependencies
│       └── 📂 dependencies_installer
│           └── 📄 __init__.py
│           └── 📂 vendor
│               └── 📂 py_pip
├── 📂 Resources
│   └── 🖼️ icon128.png
└── 📄 MyPlugin.uplugin  # customise uplugin settings
📄 .gitignore
📄 README.md  # create a nice readme for your plugin
```

### Info
- `MyPlugin` rename the folder to your plugin name. Unreal's naming convention uses PascalCase.
- `MyPlugin.uplugin` Rename this file to your plugin name, and open it with a text editor & edit the content.
- `.gitignore` is setup to prevent unneeded python files from being commit to your git-repo.
- `requirements.txt` Add your pip/pypi dependencies to this file, delete it if not used.
- `README.md`: include an image & description, so people see what's your plugin about.
- `Python` This folder is added to the PYTHONPATH, put the modules you want to import in here
- `dependencies_installer` This Python packages auto installs all your dependencies on startup from the `requirements.txt`, it ships with `py_pip` for the installation.


# Installation

### Manual install
1. Place the plugin in Unreal's `MyProject/Plugins` folder
2. Enable the plugin in Unreal 
   1. open `Edit > Plugins`
   2. search for `MyPlugin` (capital sensitive) and enable it
3. Restart Unreal

### (OPTIONAL) Add Plugget install support
To support 1-click install & automatically install all dependencies in the `requirements.txt` file, you can add [plugget](https://github.com/plugget/plugget) support.
It's a bit more work for you, the developer. But it removes the technical steps for the end user. And makes your plugin discoverable to other users.

1. Upload your plugin to a repo. ([example repo](https://github.com/hannesdelbeke/unreal-python-plugin-template))
2. Create a plugget manifest ([sample manifest](https://github.com/plugget/plugget-pkgs/blob/main/unreal/hello-world-template/latest.json)) that points to your repo,
3. Make a PR in [plugget-pkgs](https://github.com/plugget/plugget-pkgs) to merge it in the public Plugget database.
4. Add the plugget-install instructions to your README:
```
Installation with plugget automatically installs all dependencies.
1. Install the [plugget Qt Unreal plugin](https://github.com/plugget/plugget-unreal-plugin)
2. Install the package:
   - go to the menu `Edit > Plugget Packages` to open the package manager
   - search & install `unreal-script-editor` <=========== EDIT THIS TEXT ⚠️
```

<details>
 <summary>example of a more advanced plugin made from this template, and installable through plugget</summary>
   
- [repo](https://github.com/hannesdelbeke/unreal-plugin-python-script-editor)
- [plugget manifest](https://github.com/plugget/plugget-pkgs/blob/main/unreal/python-script-editor/latest.json)
- plugget package name `unreal-script-editor`
</details>


### Community
- unreal forum [thread](https://forums.unrealengine.com/t/made-a-python-plugin-template/1089878)
- [tech-art.org thread](https://www.tech-artists.org/t/free-a-python-unreal-plugin-template/17995)
