# Days Between Dates Calculator
[English](README.en.md) | [Русский](README.md)
A Python command-line utility that calculates the number of days between two dates, taking leap years into account.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Input Format](#input-format)
- [Output Format](#output-format)
- [Error Handling](#error-handling)
- [Program Example](#program-example)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)

## Features

- Calculates the number of days between two dates (the result is always non-negative, so the order of dates does not matter).
- Determines leap years according to the Gregorian calendar.
- Validates dates: format, month range, and the number of days in the specific month.
- Two input/output modes: interactive console or files.
- Clear error messages and exit codes suitable for use in scripts.
- No third-party dependencies.

## Requirements

- Python 3.6 or newer (f-strings and type annotations are used).
- No third-party packages needed: only the standard library is used (`sys`, `os`, `argparse`, `datetime`).

> **Note:** the program's messages and output are in Russian.

## Installation

1. Download or clone the repository.
2. Make sure Python is installed:

   ```bash
   python --version
   ```

No additional installation is required — the `date.py` file is all you need.

## Usage

### Interactive mode

Run the program without arguments and enter two dates:

```bash
python date.py
```

```text
Введите первую дату (ДД.ММ.ГГГГ): 01.01.2024
Введите вторую дату (ДД.ММ.ГГГГ): 01.01.2025
```

(The prompts read "Enter the first date" and "Enter the second date", in `DD.MM.YYYY` format.)

### File mode

Read dates from a file and print the result to the console:

```bash
python date.py --in input.txt
```

Read from a file and save the result to a file:

```bash
python date.py --in input.txt --out result.txt
```

Enter dates from the keyboard and save the result to a file:

```bash
python date.py --out result.txt
```

### Command-line options

| Option | Description |
|---|---|
| `--in FILE` | File with the input dates (two lines). If omitted, dates are entered from the keyboard |
| `--out FILE` | File to save the result to. If omitted, the result is printed to the console |
| `-h`, `--help` | Show help |

## Input Format

Two dates in `DD.MM.YYYY` format, each on its own line:

```text
01.01.2024
01.01.2025
```

Rules:

- the separator is a dot;
- empty lines and leading/trailing spaces are ignored;
- the file must be UTF-8 encoded (preferably without BOM);
- the date must exist in the calendar (for example, `29.02.2023` is an error).

## Output Format

```text
Дата 1: 01.01.2024 (високосный год)
Дата 2: 01.01.2025 (невисокосный год)
Количество дней между датами: 366
```

Translation: *Date 1 … (leap year); Date 2 … (non-leap year); Number of days between the dates: 366.*

In console mode the output is preceded by the heading `--- Результат ---` ("Result").

## Error Handling

Error messages are written to the standard error stream (`stderr`).

### Exit codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Data error (invalid format, non-existent date, fewer than two dates) or I/O error |
| `2` | Input file not found |

### Error message examples

| Cause | Message | Meaning |
|---|---|---|
| Invalid format | `Ошибка: Ожидается формат ДД.ММ.ГГГГ, получено: '1-1-2024'` | Expected format DD.MM.YYYY |
| Non-numeric characters | `Ошибка: Дата содержит нецифровые символы: 'аа.бб.вввв'` | The date contains non-digit characters |
| Month out of range | `Ошибка: Месяц вне диапазона 1..12: 13` | Month is outside 1..12 |
| Non-existent day | `Ошибка: День 29 вне диапазона для 02.2023 (в месяце 28 дней)` | Day 29 is out of range for 02.2023 (the month has 28 days) |
| Only one date entered | `Ошибка: Нужно ввести две даты (каждая на отдельной строке).` | Two dates are required, one per line |
| File not found | `Ошибка: файл не найден: input.txt` | File not found |

## Program Example

<!-- Insert program screenshots here -->

## How It Works

A year is a leap year if it is divisible by 4 but not by 100, or if it is divisible by 400:

```python
(year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
```

For example, 2000 and 2024 are leap years; 1900 and 2100 are not.

Main functions:

| Function | Purpose |
|---|---|
| `is_leap_year(year)` | Checks whether a year is a leap year |
| `days_in_month(year, month)` | Returns the number of days in a month, accounting for leap years |
| `parse_date(s)` | Parses and validates a `DD.MM.YYYY` date string |
| `days_between(d1, d2)` | Returns the number of days between two dates (absolute value) |
| `calculate(text)` | Processes two date lines and builds the result |
| `main(argv)` | Entry point: argument parsing, input, output, exit codes |

## Project Structure

```text
.
├── date.py          # program source code
├── README.md        # project description (Russian)
└── README.en.md     # project description (English)
```
author: Serdeshniy K.M
