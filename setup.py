#!/usr/bin/env python3
"""
CoIDE Environment Setup Script
"""

import os
import sys
import argparse
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path

# Поддержка цветов в Windows
try:
    import colorama
    from colorama import Fore, Style
    colorama.init()
    INFO_COLOR = Fore.GREEN
    ERROR_COLOR = Fore.RED
    STEP_COLOR = Fore.CYAN
    RESET = Style.RESET_ALL
except ImportError:
    INFO_COLOR = ERROR_COLOR = STEP_COLOR = ""
    RESET = ""

# ============================================================================
# Конфигурация
# ============================================================================
DEFAULT_INSTALL_DIR = "C:\\CooCox\\CoIDE"

# Каталоги относительно скрипта
SCRIPT_DIR = Path(__file__).parent.absolute()
DOWNLOADS_DIR = SCRIPT_DIR / "downloads"
PORTABLE_DIR = SCRIPT_DIR / "portable"

# Список для скачивания
DOWNLOAD_ITEMS = [
    {
        "name": "CoIDE Installer 1.7.8",
        "url": "https://github.com/unsi9ned/coide-1.7.8-patch/releases/download/CoIDE-1.7.8/CoIDE-1.7.8.exe",
        "filename": "CoIDE-1.7.8.exe"
    },
    {
        "name": "CoFlash Adapter v0.1.0",
        "url": "https://github.com/unsi9ned/coflash-adapter/releases/download/v0.1.0/coflash.exe",
        "filename": "coflash.exe"
    },
    {
        "name": "CoIDE Pack Installer v0.2.0",
        "url": "https://github.com/unsi9ned/coide-pack-installer/releases/download/v0.2.0-test/CoIDE_PackInstaller-v0.2.0-test-Win64-portable.zip",
        "filename": "CoIDE_PackInstaller.zip"
    },
    {
        "name": "Nordic DFP Pack 8.28.0",
        "url": "https://files.nordicsemi.com/artifactory/nRF5-SDK/external/pieces/nRF_DeviceFamilyPack/NordicSemiconductor.nRF_DeviceFamilyPack.8.28.0.pack",
        "filename": "NordicSemiconductor.nRF_DeviceFamilyPack.8.28.0.pack"
    },
    {
        "name": "Microchip SAMD21 DFP Pack 3.7.262",
        "url": "https://github.com/unsi9ned/Microchip.SAMD21_DFP/releases/download/v3.7.262-unsi9ned.1/Microchip.SAMD21_DFP.3.7.262-unsi9ned.1.pack",
        "filename": "Microchip.SAMD21_DFP.3.7.262-unsi9ned.1.pack"
    },
    {
        "name": "Milandr DFP Pack 1.3.2",
        "url": "https://github.com/unsi9ned/Milandr.MDR32FxQI_DFP/releases/download/v1.3.2-unsi9ned.2-test/Milandr.MDR32FxQI_DFP.1.3.2-unsi9ned.2-test.pack",
        "filename": "Milandr.MDR32FxQI_DFP.1.3.2-unsi9ned.2-test.pack"
    },
    {
        "name": "Milandr Examples Pack 1.3.2",
        "url": "https://github.com/unsi9ned/Milandr.MDR32FxQI_DFP/releases/download/v1.3.2-unsi9ned.2-test/Milandr.MDR32FxQI_Examples.1.3.2-unsi9ned.2-test.pack",
        "filename": "Milandr.MDR32FxQI_Examples.1.3.2-unsi9ned.2-test.pack"
    },
    {
        "name": "pyOCD 0.44.0",
        "url": "https://github.com/pyocd/pyOCD/releases/download/v0.44.0/pyocd-windows-0.44.0.zip",
        "filename": "pyocd-windows-0.44.0.zip"
    }
]

# ============================================================================
# Утилиты
# ============================================================================
def print_info(msg):
    print(f"{INFO_COLOR}[INFO]{RESET} {msg}")

def print_error(msg):
    print(f"{ERROR_COLOR}[ERROR]{RESET} {msg}")

def print_step(msg):
    print(f"\n{STEP_COLOR}=== {msg} ==={RESET}")

def download_file(url, dest_path, force_download=False):
    """Скачивание файла, если он не существует или force_download=True"""
    if not force_download and dest_path.exists():
        print_info(f"File already exists: {dest_path.name} (skipping)")
        return True
    
    try:
        print_info(f"Downloading: {url}")
        urllib.request.urlretrieve(url, dest_path)
        return True
    except Exception as e:
        print_error(f"Failed to download: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Распаковка ZIP архива"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        print_error(f"Failed to extract: {e}")
        return False

# ============================================================================
# Основные функции
# ============================================================================
def download_all(force_download=False):
    """Скачивание всех файлов в папку downloads (пропускает существующие)"""
    print_step("Downloading all files")
    
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    
    for item in DOWNLOAD_ITEMS:
        dest = DOWNLOADS_DIR / item["filename"]
        if not force_download and dest.exists():
            print_info(f"Already exists: {item['name']} (skipping)")
            continue
        
        if not download_file(item["url"], dest, force_download):
            print_error(f"Failed to download {item['name']}")
            return False
    
    print_info(f"All files downloaded to {DOWNLOADS_DIR}")
    return True

def install_coide(install_dir, silent=True):
    """Установка CoIDE"""
    print_step("Installing CoIDE")
    
    installer = DOWNLOADS_DIR / "CoIDE-1.7.8.exe"
    
    if not installer.exists():
        print_error("CoIDE installer not found")
        return False
    
    # Запуск установки
    if silent:
        cmd = f'start /wait "" "{installer}" /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP- /DIR="{install_dir}" /NOICONS'
    else:
        cmd = f'start /wait "" "{installer}" /DIR="{install_dir}"'
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode == 0:
        print_info(f"CoIDE installed to {install_dir}")
        return True
    else:
        print_error(f"CoIDE installation failed with code {result.returncode}")
        return False

def configure_coide(install_dir):
    """Настройка CoIDE (замена coflash.exe, распаковка pyOCD, копирование адаптера)"""
    print_step("Configuring CoIDE")
    
    bin_dir = Path(install_dir) / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Переименование оригинального CoFlash
    coflash_original = bin_dir / "coflash_origin.exe"
    coflash_exe = bin_dir / "coflash.exe"
    
    if coflash_exe.exists():
        shutil.move(str(coflash_exe), str(coflash_original))
        print_info("Renamed original coflash.exe -> coflash_origin.exe")
    
    # 2. Распаковка pyOCD
    pyocd_zip = DOWNLOADS_DIR / "pyocd-windows-0.44.0.zip"
    if pyocd_zip.exists():
        temp_extract = SCRIPT_DIR / "temp_pyocd"
        temp_extract.mkdir(exist_ok=True)
        
        extract_zip(pyocd_zip, temp_extract)
        
        for item in temp_extract.iterdir():
            dest = bin_dir / item.name
            if item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
        
        shutil.rmtree(temp_extract)
        print_info("Extracted pyOCD to bin directory")
    
    # 3. Копирование CoFlash Adapter
    adapter_src = DOWNLOADS_DIR / "coflash.exe"
    adapter_dst = bin_dir / "coflash.exe"
    if adapter_src.exists():
        shutil.copy(str(adapter_src), str(adapter_dst))
        print_info("Copied CoFlash Adapter to bin directory")
    
    return True

def setup_pack_installer():
    """Распаковка CoIDE Pack Installer в текущий каталог"""
    print_step("Setting up CoIDE Pack Installer")
    
    pack_installer_zip = DOWNLOADS_DIR / "CoIDE_PackInstaller.zip"
    pack_installer_dir = SCRIPT_DIR / "CoIDE_PackInstaller"
    
    if pack_installer_zip.exists():
        if pack_installer_dir.exists():
            shutil.rmtree(pack_installer_dir)
        extract_zip(pack_installer_zip, pack_installer_dir)
        print_info(f"Extracted CoIDE Pack Installer to {pack_installer_dir}")
    
    return True

def install_cmsis_pack(install_dir):
    """Установка CMSIS Pack через Pack Installer"""
    print_step("Installing CMSIS Packs")
    
    pack_installer_dir = SCRIPT_DIR / "CoIDE_PackInstaller"
    pack_installer_exe = pack_installer_dir / "CoIDE_PackInstaller.exe"
    
    if not pack_installer_exe.exists():
        print_error("CoIDE Pack Installer not found")
        return False
    
    # Список пакетов для установки
    pack_files = [
        "NordicSemiconductor.nRF_DeviceFamilyPack.8.28.0.pack",
        "Microchip.SAMD21_DFP.3.7.262-unsi9ned.1.pack",
        "Milandr.MDR32FxQI_DFP.1.3.2-unsi9ned.2-test.pack",
        "Milandr.MDR32FxQI_Examples.1.3.2-unsi9ned.2-test.pack"
    ]

    for pack_filename in pack_files:
        pack_path = DOWNLOADS_DIR / pack_filename
        
        if not pack_path.exists():
            print_error(f"Pack not found: {pack_filename}")
            continue
        
        print_info(f"Installing {pack_filename}...")
        
        # 1. Указать путь к CoIDE
        subprocess.run([str(pack_installer_exe), "-d", install_dir], cwd=str(pack_installer_dir))
        
        # Оптимизация БД до всех установок
        print_info("Optimizing database...")
        subprocess.run([str(pack_installer_exe), "--optimize-db"], cwd=str(pack_installer_dir))
        
        # 2. Указать путь к пакету
        subprocess.run([str(pack_installer_exe), "-p", str(pack_path)], cwd=str(pack_installer_dir))
        
        # 3. Вывести список устройств
        subprocess.run([str(pack_installer_exe), "-l"], cwd=str(pack_installer_dir))
        
        # 4. Установить пакет
        subprocess.run([str(pack_installer_exe), "-i"], cwd=str(pack_installer_dir))
    
    return True

def cleanup(install_dir):
    """Удаление временных файлов и артефактов"""
    print_step("Cleaning up")
    
    coide_path = Path(install_dir)
    
    # Удаление временных папок
    temp_dirs = ["temp", "kindeditor-3.5.4-en", "repo\\.rn"]
    for dir_name in temp_dirs:
        dir_path = coide_path / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print_info(f"Removed {dir_path}")
    
    return True

def create_portable(install_dir):
    """Создание portable-версии CoIDE в папке portable"""
    print_step("Creating portable version")
    
    PORTABLE_DIR.mkdir(parents=True, exist_ok=True)
    
    coide_path = Path(install_dir)
    zip_path = PORTABLE_DIR / "CoIDE-portable.zip"
    
    print_info(f"Archiving {coide_path} to {zip_path}...")
    shutil.make_archive(str(zip_path).replace('.zip', ''), 'zip', str(coide_path))
    
    print_info(f"Portable version created at {zip_path}")
    return True
    
def clean_all():
    """Удаление всех скачанных файлов и временных папок"""
    print_step("Cleaning all downloaded files")
    
    # Удаление папки downloads
    if DOWNLOADS_DIR.exists():
        shutil.rmtree(DOWNLOADS_DIR)
        print_info(f"Removed {DOWNLOADS_DIR}")
    
    # Удаление папки portable
    if PORTABLE_DIR.exists():
        shutil.rmtree(PORTABLE_DIR)
        print_info(f"Removed {PORTABLE_DIR}")
    
    # Удаление распакованного Pack Installer
    pack_installer_dir = SCRIPT_DIR / "CoIDE_PackInstaller"
    if pack_installer_dir.exists():
        shutil.rmtree(pack_installer_dir)
        print_info(f"Removed {pack_installer_dir}")
    
    # Удаление временной папки pyOCD (если осталась)
    temp_pyocd = SCRIPT_DIR / "temp_pyocd"
    if temp_pyocd.exists():
        shutil.rmtree(temp_pyocd)
        print_info(f"Removed {temp_pyocd}")
    
    print_info("Clean completed")
    return True    

# ============================================================================
# Главная функция
# ============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="CoIDE Environment Setup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup.py                           # Interactive mode
  python setup.py --install-path "C:\\CoIDE"  # Silent install
  python setup.py --force                   # Force re-download all files
  python setup.py --skip-download           # Skip download step
  python setup.py --skip-install            # Skip CoIDE installation
  python setup.py --skip-config             # Skip configuration
  python setup.py --skip-packs              # Skip CMSIS packs installation
  python setup.py --skip-portable           # Skip portable creation
  python setup.py --silent                  # Silent mode (no prompts)
        """
    )
    
    parser.add_argument(
        "--install-path", "-i",
        type=str,
        default=None,
        help=f"CoIDE installation directory (default: {DEFAULT_INSTALL_DIR})"
    )
    
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force re-download all files even if they exist"
    )
    
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip downloading files"
    )
    
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip CoIDE installation"
    )
    
    parser.add_argument(
        "--skip-config",
        action="store_true",
        help="Skip CoIDE configuration"
    )
    
    parser.add_argument(
        "--skip-packs",
        action="store_true",
        help="Skip CMSIS packs installation"
    )
    
    parser.add_argument(
        "--skip-portable",
        action="store_true",
        help="Skip portable version creation"
    )
    
    parser.add_argument(
        "--silent", "-s",
        action="store_true",
        help="Silent mode (no prompts, use defaults)"
    )
    
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean all downloaded files and temporary directories"
    )
    
    args = parser.parse_args()
    
    # Если запрошена очистка — выполняем и выходим
    if args.clean:
        clean_all()
        return
    
    print("=" * 50)
    print("    CoIDE Environment Setup Script")
    print("=" * 50)
    print(f"Script directory: {SCRIPT_DIR}")
    print(f"Downloads will be saved to: {DOWNLOADS_DIR}")
    print(f"Portable package will be saved to: {PORTABLE_DIR}")
    print()
    
    # Определяем путь установки
    if args.install_path:
        install_dir = args.install_path
    elif args.silent:
        install_dir = DEFAULT_INSTALL_DIR
    else:
        install_dir = input(f"Enter CoIDE install directory [{DEFAULT_INSTALL_DIR}]: ").strip()
        if not install_dir:
            install_dir = DEFAULT_INSTALL_DIR
    
    print_info(f"Installation directory: {install_dir}")
    
    # Последовательное выполнение с проверкой пропусков
    steps = []
    
    if not args.skip_download:
        steps.append(("Downloading files", lambda: download_all(args.force)))
    
    if not args.skip_install:
        steps.append(("Installing CoIDE", lambda: install_coide(install_dir, silent=args.silent)))
    
    if not args.skip_config:
        steps.append(("Configuring CoIDE", lambda: configure_coide(install_dir)))
    
    if not args.skip_packs:
        steps.append(("Setting up Pack Installer", lambda: setup_pack_installer()))
        steps.append(("Installing CMSIS Pack", lambda: install_cmsis_pack(install_dir)))
    
    if not args.skip_config:
        steps.append(("Cleanup", lambda: cleanup(install_dir)))
    
    if not args.skip_portable:
        steps.append(("Creating portable version", lambda: create_portable(install_dir)))
    
    for step_name, step_func in steps:
        print_step(step_name)
        if not step_func():
            print_error(f"Failed at step: {step_name}")
            sys.exit(1)
    
    print_step("Setup completed successfully!")

if __name__ == "__main__":
    main()