# code in init_unreal.py wil run on startup if the plugin is enabled
import unreal


def create_script_editor_button():
    """Add a tool button to the tool bar"""

    section_name = 'Plugins'
    se_command = 'import my_module;my_module.show()'  # todo replace with your code
    label = 'My Plugin'
    tooltip = "my tooltip"

    menus = unreal.ToolMenus.get()
    level_menu_bar = menus.find_menu('LevelEditor.LevelEditorToolBar.PlayToolBar')
    level_menu_bar.add_section(section_name=section_name, label=section_name)

    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
    entry.set_label(label)
    entry.set_tool_tip(tooltip)
    entry.set_icon('EditorStyle', 'DebugConsole.Icon')
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type=unreal.Name(''),  # not sure what this is
        string=se_command
    )
    level_menu_bar.add_menu_entry(section_name, entry)
    menus.refresh_all_widgets()

## uncomment to add a button to the toolbar to launch your tool
## don't forget to modify the function
# create_script_editor_button()

## TODO add code to add to menu

print("My plugin is enabled")
