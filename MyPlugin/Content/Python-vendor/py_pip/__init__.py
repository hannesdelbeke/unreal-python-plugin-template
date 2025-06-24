import sys
import subprocess
import pkgutil
import os
from importlib.metadata import distribution, PackageNotFoundError
import importlib
import logging
from pathlib import Path

default_target_path = ""
python_interpreter = sys.executable  # can be changed externally, e.g. in Maya

_cached_installed_packages = []


def _prep_env() -> dict:
    """Add custom python paths to the environment, to support dynamically added paths """
    my_env = os.environ.copy()

    # avoid paths not in sys.path passed to pip,
    # e.g. paths set in PYTHONPATH, are ignored in apps like Blender. So shouldn't be passed to pip
    my_env["PYTHONPATH"] = os.pathsep.join(sys.path)

    # find git in our path and keep that
    git_path = None
    for folder in my_env["PATH"].split(os.pathsep):
        if (Path(folder) / "git.exe").exists():
            git_path = folder
            break

    # clear paths, to avoid passing external python modules to pip
    for key in ["PATH", "PYTHONHOME", "PYTHONUSERBASE"]:
        if key in my_env:
            del my_env[key]

    # add git_path back to PATH
    if git_path:
        my_env["PATH"] = git_path + os.pathsep + my_env.get("PATH", "")
    else:
        logging.warning("git not found in PATH, installing git dependencies might fail.")

    # prevent pip from using the user site
    my_env["PYTHONNOUSERSITE"] = "1"

    return my_env


def run_command_process(command) -> subprocess.Popen:
    """returns the subprocess, use to capture the output of the command while running"""
    my_env = _prep_env()
    print(F"run_command_process command: {command}")
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)


def run_command(command, timeout=-1) -> (str, str):
    """
    Run command and return output and error
    Returns (stdOut, stdErr) output and error are bytes, use .decode() to convert to string
    """
    process = run_command_process(command)
    if timeout == -1:  # skip
        output, error = process.communicate()
    else:
        try:
            output, error = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            logging.warning(f"Timeout expired for command: {command}")
            process.kill()
            output, error = process.communicate()
    return output, error


def list():
    """return tuple of (name, version) for each installed package
    e.g. [('requests', '2.25.1'), ('numpy', '1.20.0')]"""

    from importlib.metadata import distributions

    packages = []
    for dist in distributions():
        name = dist.metadata["Name"]
        version = dist.version
        packages.append((name, version))
    
    # output, error = run_command([python_interpreter, "-m", "pip", "list"])

    # # Parse the output of the pip list command
    # packages = []
    # raw = output.decode()

    # for line in raw.split("\n")[2:-1]:  # 2-1 skips the first lines
    #     split_text = line.split()  # assumes version and package name dont contain spaces
    #     if split_text:
    #         name, version = split_text[:2]  # TODO edit packages contain a 3rd value: path
    #         packages.append((name, version))

    global __cached_installed_packages
    __cached_installed_packages = packages
    return packages


def get_version(package_name, cached=False) -> str:
    """
    Return installed package version or empty string
    use_cached: requires running list before use. speed up get_version since pip list is slow
    """
    if cached:
        global __cached_installed_packages
        packages = __cached_installed_packages
    else:
        packages = list()
    for name, version in packages:
        if name == package_name:
            return version
    return ""


def get_location(package_name: str) -> "str|None":
    # todo cleanup
    def find_package_location(name: str) -> "str|None":
        try:
            dist = distribution(name)
            return dist.locate_file('')
        except PackageNotFoundError:
            logging.warning(f"Package '{name}' not found.")
            return None

    try:
        loader = pkgutil.get_loader(package_name)
        if loader is not None:
            package_location = os.path.dirname(loader.get_filename())
            return package_location
        else:
            return find_package_location(package_name)
    except ImportError as e:
        logging.error(f"Error while trying to locate package '{package_name}'. Error: {e}")
        return None


def install_process(package_name: "str|List[str]" = None,
                    target_path: "str|pathlib.Path" = None,
                    force=False,
                    upgrade=False,
                    requirements=None,
                    options=None,
                    ):
    """
    target_path: path where to install module too, if default_target_path is set, use that
    to fix possible import issues, invalidate caches after installation with 'importlib.invalidate_caches()'
    """
    command = [python_interpreter, "-m", "pip", "install"]
    if package_name:
        command.append(package_name)
    if requirements:
        command.extend(["-r", str(requirements)])
    if force:
        command.append("--force-reinstall")
    if upgrade:
        command.append("--upgrade")
    target_path = target_path or default_target_path
    if target_path:
        command.extend(["--target", str(target_path), "--no-user"])
    if options:
        command.extend(options)
    return run_command_process(command)


def _print_error(error, package_name=None):
    if not error:
        return

    try:
        txt = error.decode()
        raw_lines = txt.splitlines()
        # remove empty lines
        lines = [line for line in raw_lines if line.strip()]
        first_line = lines[0].strip()

        # check if we don't just have a pip upgrade error, like this:
        # LogPython: Error: ERROR:root:There was an install error for package 'py_pip'
        # LogPython: Error: ERROR:root:
        # LogPython: Error: ERROR:root:[notice] A new release of pip is available: 24.0 -> 25.1.1
        # LogPython: Error: ERROR:root:[notice] To update, run: C:\Program Files\Epic Games\UE_5.6\Engine\Binaries\ThirdParty\Python3\Win64\python.exe -m pip install --upgrade pip
        if len(lines) == 2 and "A new release of pip is available" in lines[0] and "To update, run:" in lines[1]:
            return

        # subprocess writes the command run as an error, let's avoid this false error
        if len(lines) <= 1 and first_line.startswith("Running command"):
            # print(first_line)
            return

        logging.error(f"There was an install error for package '{package_name}'")

        for line in lines:
            logging.error(line)
    except Exception as e:
        logging.error("failed to decode subprocess error", e)
        logging.error(error)


def install(package_name: "str|List[str]" = None,
            invalidate_caches: bool = True,
            target_path: "str|pathlib.Path" = None,
            force=False,
            upgrade=False,
            requirements: "str|pathlib.Path" = None,
            options=None,  # list[str] extra options to pass to pip install, e.g. ["--editable"]
            add_to_path=True,  # if True, add target_path to sys.path after installation
            skip_installed=True,  # if True, skip installation of already installed packages 
            ):
    """
    pip install a python package
    package_name: name of package to install (extra args can be passed in the package_name kwarg)
    invalidate_caches: if True, invalidate importlib caches after installation
    target_path: path where to install module too, if default_target_path is set, use that
    skip_if_installed: if True, check if packages are already installed and skip subprocess if they are
    """
    
    missing_packages = []
    if skip_installed and not force and not upgrade :

        # Check if we can skip installation for requirements file
        if requirements and not package_name:
            missing_packages = get_missing_packages_from_requirements(requirements)
            if not missing_packages:
                print(f"All packages from requirements file '{requirements}' are already installed.")
                # logging.info(f"All packages from requirements file are already installed, skipping pip install")
                return b"All package already installed", b""
        
        # Check if single package is already installed
        elif package_name and not requirements:
            parsed_name = parse_package_name(package_name)
            if is_package_installed(parsed_name):
                print(f"Package '{parsed_name}' is already installed.")
                # logging.info(f"Package '{package_name}' is already installed, skipping pip install")
                return b"Package already installed", b""
    
    if package_name:
        missing_packages.append(package_name)
    for package_name in missing_packages:
        # install packages 1 by 1
        process = install_process(package_name=package_name, target_path=target_path, force=force, upgrade=upgrade, requirements=requirements, options=options)
        output, error = process.communicate()
        _print_error(error, package_name=package_name)

        # exception on fail, TODO test if this doesn't trigger warnings, e.g. a pip version is outdated warning
        return_code = process.returncode
        if return_code != 0:
            # Treat non-zero return code as a package installation failure
            raise RuntimeError(f"Package installation failed with return code {return_code}: {error}")

    # TODO if editable install, we add a pth file to target path.
    # but target path might not be in site_packages, and pth might not be processed.
    # if target_path:
    #     import site
    #     site.addsitedir(pth_path)
    #     site.removeduppaths()

    if invalidate_caches:
        importlib.invalidate_caches()

    # check if target_path and default path are in sys.path
    # many apps don't add the path if the folder doesn't exist, e.g. on a fresh install
    # adding it to the sys.path allows importing without restarting the app
    if add_to_path:
        if target_path and str(target_path) not in sys.path:
            sys.path.append(str(target_path))
            logging.debug(f"Added target path to sys.path: {target_path}")
        if default_target_path and str(default_target_path) not in sys.path:
            sys.path.append(str(default_target_path))
            logging.debug(f"Added default target path to sys.path: {default_target_path}")

    return output, error


def get_package_modules(package_name):
    # Get a list of modules that belong to the specified package
    package_modules = []
    package_loader = pkgutil.get_loader(package_name)
    file_name = package_loader.get_filename()  # e.g. "C:\Users\hanne\AppData\Roaming\Blender Foundation\Blender\3.2\scripts\addons\modules\plugget\__init__.py"
    if not Path(file_name).is_dir():  # todo test with a .py file instead of package
        file_name = str(Path(file_name).parent)  # # e.g. "C:\Users\hanne\AppData\Roaming\Blender Foundation\Blender\3.2\scripts\addons\modules\plugget"

    if package_loader is not None:
        for _, module_name, _ in pkgutil.walk_packages([file_name]):
            full_module_name = f"{package_name}.{module_name}"
            package_modules.append(full_module_name)

    return package_modules


def unimport_modules(package_name):
    """unload any package's imported modules from memory"""
    for module_name in get_package_modules(package_name):
        if module_name in sys.modules:
            logging.debug(f"deleting module {module_name}")
            del sys.modules[module_name]


def uninstall(package_name=None, unimport=True, yes=True, requirements=None):  # dependencies=False
    """
    custom kwargs
    delete_module: if True, delete the module from sys.modules, it's the opposite of importing the module

    pip kwargs
    yes: if True, Don’t ask for confirmation of uninstall deletions
    """
    # todo uninstall dependencies

    command = [python_interpreter, "-m", "pip", "uninstall"]
    if package_name:
        command.append(package_name)
    if yes:
        command.append("-y")
    if requirements:
        command.extend(["-r", str(requirements)])
    output, error = run_command(command)

    # todo add unimport support if we uninstall from requirements
    try:
        unimport_modules = []
        if package_name:
            unimport_modules.append(package_name)
        if requirements:
            for module in iter_packages_in_requirements(requirements):
                unimport_modules.append(module)
        if unimport:
            for package in unimport_modules:
                unimport_modules(package)
    except Exception as e:
        logging.warning(f"unimport failed: {e}")

    return output, error


def iter_packages_in_requirements(path: "str|Path"):
    data = Path(path).read_text().splitlines()
    for line in data:
        line = line.strip()
        if line.startswith("#"):  # skip comments
            continue
        if not line:  # skip empty lines
            continue
        yield line


def parse_package_name(package_spec: str) -> str:
    """
    Extract package name from a pip package specification. 
    (a line of string in a requirements file)

    Handles version specifiers, git URLs, etc.
    Examples:
    - "requests==2.25.1" -> "requests"
    - "git+https://github.com/user/repo.git" -> "repo"
    - "package>=1.0" -> "package"
    """
    package_spec = package_spec.strip()

    # Handle git URLs
    if package_spec.startswith("git+"):
        # Extract repo name from git URL
        repo_name = package_spec.split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]
        return repo_name

    # Handle local paths
    if package_spec.startswith((".", "/")):
        return os.path.basename(package_spec.rstrip("/"))

    # Handle package with version specifiers
    for separator in ["==", ">=", "<=", "!=", ">", "<", "~="]:
        if separator in package_spec:
            return package_spec.split(separator)[0].strip()

    # Handle extras like "package[extra]"
    if "[" in package_spec:
        return package_spec.split("[")[0].strip()

    return package_spec


def is_package_installed(package_name: str) -> bool:
    """
    Check if a package is installed by trying to get its version.
    Returns True if package is installed, False otherwise.
    """
    try:
        version = get_version(package_name, cached=False)
        return bool(version)
    except Exception:
        return False
    
# plugget code - TODO decide on best method and cleanup / combine with above
# def is_package_installed(package_name):
#     try:
#         importlib.metadata.version(package_name)
#         return True
#     except importlib.metadata.PackageNotFoundError:
#         return False


def get_missing_packages_from_requirements(requirements_path: "str|Path") -> "tuple[bool, list[str]]":
    """
    Check if all packages in requirements file are already installed.
    Returns (all_installed, missing_packages)
    """
    try:
        missing_packages = []

        for package_spec in iter_packages_in_requirements(requirements_path):
            if not package_spec.strip():  # skip empty lines
                continue

            package_name = parse_package_name(package_spec)
            if not is_package_installed(package_name):
                missing_packages.append(package_spec)

        return missing_packages

    except Exception as e:
        logging.warning(f"Failed to check requirements: {e}")
        # If we can't check, assume we need to install
        return False, []
