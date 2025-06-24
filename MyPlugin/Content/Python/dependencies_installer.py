import sys
from pathlib import Path
import unreal


def project_site_dir() -> Path:
    """
    Return the site-packages path for the current project
    Note: this folder might not exist
    """
    content_path = unreal.Paths.project_content_dir()  # '../../../Users/USER/MyProject/Content/'
    content_path = unreal.Paths.convert_relative_path_to_full(content_path)  # 'C:/Users/USER/MyProject/Content/'
    return Path(content_path) / r"Python\Lib\site-packages"  # 'C:/Users/USER/MyProject/Content/Python/Lib/site-packages'


def setup_vendor_module():
    """
    Try to import vendored module, and if it fails, 
    add Python-vendor to PATH and try again.
    """
    try:
        # First try to import normally
        import py_pip
        print("py_pip imported successfully from system path")
        return py_pip
    except ImportError:
        print("py_pip not found in system path, trying vendored version...")
        
        # Get the plugin content directory
        current_file = Path(__file__)
        vendor_path = current_file.parent.parent / "Python-vendor"
        vendor_path = vendor_path.resolve()
        if not vendor_path.exists():
            raise ImportError("Could not find Python-vendor path")
        
        # Add vendor path to sys.path temporarily
        vendor_path_str = str(vendor_path)
        path_added = False
        if vendor_path_str not in sys.path:
            sys.path.insert(0, vendor_path_str)
            path_added = True
            print(f"Added vendor path to sys.path: {vendor_path}")
        
        # Try to import from vendor path
        import py_pip
        print("py_pip imported successfully from vendor path")

        # Set the interpreter and install folder
        py_pip.default_target_path = project_site_dir()
        py_pip.python_interpreter = unreal.get_interpreter_executable_path()
        # print(f"py_pip - Set default target path to: {py_pip.default_target_path}")
        # print(f"py_pip - Set Python interpreter to: {py_pip.python_interpreter}")
    
        # # Update py_pip itself
        # print("Updating py_pip...")
        # py_pip.install("py_pip", upgrade=True)  # Update py_pip itself
        
        # Remove vendor path from sys.path if we added it
        if path_added and vendor_path_str in sys.path:
            sys.path.remove(vendor_path_str)
            print("Removed vendor path from sys.path")

        # # Reload any vendored modules to ensure we're using the latest versions
        # module_name = 'py_pip'
        # module = sys.modules[module_name]
        # del sys.modules[module_name]
        
        # # Clear the local py_pip reference to force fresh import
        # if 'py_pip' in locals():
        #     del py_pip
        
        # # Now import py_pip fresh (this will import the updated version)
        # import py_pip
        # print("py_pip imported fresh after cleanup")
        
        return py_pip
            

def install_dependencies():
    """Install dependencies from requirements.txt."""
    print("Starting dependency installation...")
    
    # Initialize
    print("Setting up py_pip...")
    py_pip = setup_vendor_module()
    py_pip.default_target_path = project_site_dir()
    py_pip.python_interpreter = unreal.get_interpreter_executable_path()
    
    # Find requirements.txt file
    current_file = Path(__file__)
    requirements_path = current_file.parent.parent / "requirements.txt"
    
    # Install requirements
    print(f"Installing requirements from {requirements_path}...")
    py_pip.install(requirements=requirements_path)
    print("Dependencies installed successfully.")
