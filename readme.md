## CoIDE Builder

Автоматическая установка и настройка среды CoIDE с поддержкой CMSIS-пакетов.

### Что устанавливает

- **CoIDE 1.7.8** (патченная версия с поддержкой новых МК)
- **CoFlash Adapter** (транслятор команд для pyOCD)
- **pyOCD** (современный программатор)
- **CoIDE Pack Installer** (установщик CMSIS-пакетов)

### Устанавливаемые CMSIS-пакеты

| Производитель | Пакет | Версия | Описание |
|---------------|-------|--------|----------|
| Nordic Semiconductor | `NordicSemiconductor.nRF_DeviceFamilyPack` | 8.28.0 | Поддержка nRF51, nRF52, nRF91 серий |
| Microchip | `Microchip.SAMD21_DFP` | 3.7.262-unsi9ned.1 | Поддержка Microchip SAM D21 |
| Milandr | `Milandr.MDR32FxQI_DFP` | 1.3.2-unsi9ned.1 | Поддержка Milandr MDR32FxQI |

### Использование

```batch
Usage: setup.py [options]

Options:
  -i, --install-path PATH Путь установки CoIDE (по умолчанию: C:\CooCox\CoIDE)
  -f, --force             Принудительная перезагрузка всех файлов
  -s, --silent            Тихий режим (без запросов подтверждения)

  --skip-download         Пропустить скачивание файлов
  --skip-install          Пропустить установку CoIDE
  --skip-config           Пропустить настройку CoIDE
  --skip-packs            Пропустить установку CMSIS-пакетов
  --skip-cleanup          Пропустить очистку временных файлов
  --skip-portable         Пропустить создание portable-версии
  --clean                 Удаление файлов сборки
```
  
### Примеры

```batch
# Интерактивная установка (с запросом пути)
setup.py

# Полная автоматическая установка в указанную папку
setup.py --install-path "C:\CooCox\CoIDE" --silent

# Только скачать файлы (без установки)
setup.py --skip-install --skip-config --skip-packs

# Принудительная перезагрузка всех файлов
setup.py --force

# Только создать portable версию из существующей установки
setup.py --skip-download --skip-install --skip-config --skip-packs  
```

### Portable-версия
В разделе [Releases](https://github.com/unsi9ned/coide-builder/releases) доступны архивы сборок CoIDE, которые содержат:

- Полностью настроенную среду CoIDE
- CoFlash Adapter (поддержка pyOCD)
- Установленные CMSIS-пакеты (Nordic, SAM D21)

### Запуск portable-версии
1. Скачать CoIDE-\{version\}.zip из раздела Releases
2. Распаковать архив в любую папку
3. Запустить CoIDE.exe из распакованной папки

## Поддерживаемые микроконтроллеры

### Nordic Semiconductor (nRF серия)

#### nRF51 Series
- nRF51422_xxAA, nRF51422_xxAB, nRF51422_xxAC
- nRF51801_xxAB, nRF51802_xxAA, 
- nRF51822_xxAA, nRF51822_xxAB, nRF51822_xxAC
- nRF51824_xxAA

#### nRF52 Series
- nRF52805_xxAA, nRF52810_xxAA, nRF52811_xxAA
- nRF52832_xxAA, nRF52832_xxAB
- nRF52833_xxAA, nRF52840_xxAA

#### nRF91 Series
- nRF9160_xxAA

### Microchip (SAMD21 серия)

#### SAM D21 Series

- ATSAMD21E15A, ATSAMD21E15B, ATSAMD21E15BU, ATSAMD21E15L, ATSAMD21E15CU
- ATSAMD21E16A, ATSAMD21E16B, ATSAMD21E16BU, ATSAMD21E16L, ATSAMD21E16CU
- ATSAMD21E17A, ATSAMD21E17D, ATSAMD21E17DU, ATSAMD21E17L, 
- ATSAMD21E18A


- ATSAMD21G15A, ATSAMD21G15B, ATSAMD21G15L
- ATSAMD21G16A, ATSAMD21G16B, ATSAMD21G16L
- ATSAMD21G17A, ATSAMD21G17AU, ATSAMD21G17D, ATSAMD21G17L
- ATSAMD21G18A, ATSAMD21G18AU

- ATSAMD21J15A, ATSAMD21J15B
- ATSAMD21J16A, ATSAMD21J16B
- ATSAMD21J17A, ATSAMD21J17D
- ATSAMD21J18A

> **Примечание:** Для успешной сборки проекта под МК серии SAMD21 в CoIDE необходимо в Configuration:
> - Снять галочку Use Memory Layout from Memory Window
> - Снять галочку Don't use the standard system startup files
> - Указать путь к скрипту линкера {project}\samd21{letter}\gcc\gcc\\\{mcu}_flash.ls

### Milandr (MDR32FxQI серия)

- K1986VE1xI, MDR32F1QI, K1986VE92xI, K1986VE94GI, MDR32F9Q2I, MDR32FG16S1QI