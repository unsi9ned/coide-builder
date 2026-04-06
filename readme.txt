Скачать в папку downloads:
--------
1) CoIDE (https://github.com/unsi9ned/coide-1.7.8-patch/releases/download/CoIDE-1.7.8/CoIDE-1.7.8.exe)
2) CoFlash Adapter (https://github.com/unsi9ned/coflash-adapter/releases/download/v0.1.0/coflash.exe)
3) CoIDE Pack Installer (https://github.com/unsi9ned/coide-pack-installer/releases/download/v0.1.0-test/CoIDE_PackInstaller-v0.1.0-test-Win64-portable.zip)
4) NordicSemiconductor.nRF_DeviceFamilyPack.8.28.0.pack (https://files.nordicsemi.com/artifactory/nRF5-SDK/external/pieces/nRF_DeviceFamilyPack/NordicSemiconductor.nRF_DeviceFamilyPack.8.28.0.pack)
5) pyocd-windows-0.44.0.zip (https://github.com/pyocd/pyOCD/releases/download/v0.44.0/pyocd-windows-0.44.0.zip)

Установить:
-----------
1) CoIDE: start /wait "" "CoIDE-1.7.8.exe" /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP- /DIR="%INSTALL_DIR%" /NOICONS (%INSTALL_DIR% указывает пользователь, но предложить по умолчанию C:\CooCox\CoIDE)
2) В папке установки переименовать C:\CooCox\CoIDE\bin\coflash.exe в C:\CooCox\CoIDE\bin\coflash_origin.exe
3) Распаковать pyocd-windows-0.44.0.zip в каталог C:\CooCox\CoIDE\bin\
4) Скопировать coflash.exe в C:\CooCox\CoIDE\bin\coflash.exe
5) Распаковать CoIDE Pack Installer в текущий каталог ./CoIDE_PackInstaller

Установка CMSIS PACK
----------
1) Перейти cd ./CoIDE_PackInstaller
2) Указать путь к директории CoIDE: CoIDE_PackInstaller.exe -d "C:\CooCox\CoIDE"
3) Указать путь к архиву CoIDE: CoIDE_PackInstaller.exe -p "..\downloads\NordicSemiconductor.nRF_DeviceFamilyPack.8.28.0.pack"
4) Вывести список устройств и компонентов: CoIDE_PackInstaller.exe -l -c
5) Оптимизировать базу данных: CoIDE_PackInstaller.exe --optimize-db
6) Проивести установку пакета: CoIDE_PackInstaller.exe -i

Удаление артефактов:
-------------------
1) Удалить каталог C:\CooCox\CoIDE\temp
2) Удалить каталог C:\CooCox\CoIDE\kindeditor-3.5.4-en
3) Удалить каталог C:\CooCox\CoIDE\repo\.rn

Создать portable-версию CoIDE в каталоге portable (понадобится в GitHub Workflow):
1) Упаковать C:\CooCox\CoIDE в zip-архив и поместить в portable

-------------------
 Справка по командам
-------------------
# Интерактивный режим (с запросом пути)
python setup.py

# Полностью автоматическая установка в указанную папку
python setup.py --install-path "C:\CooCox\CoIDE_1.7.9" --silent

# Перезагрузить все файлы и установить
python setup.py --force --install-path "C:\CooCox\CoIDE" --silent

# Только скачать файлы (без установки)
python setup.py --skip-install --skip-config --skip-packs --skip-portable

# Только создать portable версию из существующей установки
python setup.py --skip-download --skip-install --skip-config --skip-packs