import sys
import os
import argparse
from datetime import date


# ---------- Работа с датами ----------

def is_leap_year(year: int) -> bool:
    """Проверка года на високосность (по григорианскому календарю)."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def days_in_month(year: int, month: int) -> int:
    """Количество дней в месяце с учётом високосного года."""
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    if month in (4, 6, 9, 11):
        return 30
    if month == 2:
        return 29 if is_leap_year(year) else 28
    raise ValueError(f"Некорректный месяц: {month}")


def parse_date(s: str) -> date:
    """
    Разбор строки даты в формате ДД.ММ.ГГГГ.
    Возвращает объект date или возбуждает ValueError.
    """
    s = s.strip()
    parts = s.split('.')
    if len(parts) != 3:
        raise ValueError(f"Ожидается формат ДД.ММ.ГГГГ, получено: '{s}'")
    try:
        d, m, y = (int(p) for p in parts)
    except ValueError:
        raise ValueError(f"Дата содержит нецифровые символы: '{s}'")

    if not (1 <= m <= 12):
        raise ValueError(f"Месяц вне диапазона 1..12: {m}")
    if not (1 <= d <= days_in_month(y, m)):
        raise ValueError(
            f"День {d} вне диапазона для {m:02d}.{y} "
            f"(в месяце {days_in_month(y, m)} дней)"
        )
    return date(y, m, d)


def days_between(d1: date, d2: date) -> int:
    """Количество дней между датами (по модулю)."""
    return abs((d2 - d1).days)


def calculate(text: str) -> str:
    """
    Принимает многострочный текст: первая дата, вторая дата.
    Возвращает строку-результат.
    """
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    if len(lines) < 2:
        raise ValueError("Нужно ввести две даты (каждая на отдельной строке).")

    d1 = parse_date(lines[0])
    d2 = parse_date(lines[1])

    diff = days_between(d1, d2)
    leap_flag_1 = "високосный" if is_leap_year(d1.year) else "невисокосный"
    leap_flag_2 = "високосный" if is_leap_year(d2.year) else "невисокосный"

    result = (
        f"Дата 1: {d1.strftime('%d.%m.%Y')} ({leap_flag_1} год)\n"
        f"Дата 2: {d2.strftime('%d.%m.%Y')} ({leap_flag_2} год)\n"
        f"Количество дней между датами: {diff}\n"
    )
    return result


# ---------- Ввод/вывод ----------

def read_console() -> str:
    print("Введите первую дату (ДД.ММ.ГГГГ): ", end="", flush=True)
    d1 = sys.stdin.readline()
    print("Введите вторую дату (ДД.ММ.ГГГГ): ", end="", flush=True)
    d2 = sys.stdin.readline()
    return d1 + d2


def write_console(result: str) -> None:
    print("\n--- Результат ---")
    print(result)


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, result: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(result)


# ---------- CLI ----------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Вычисление количества дней между двумя датами (ДД.ММ.ГГГГ) "
                    "с учётом високосных лет."
    )
    p.add_argument("--in", dest="in_path", metavar="FILE",
                   help="файл с исходными датами (2 строки)")
    p.add_argument("--out", dest="out_path", metavar="FILE",
                   help="файл для сохранения результата")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.in_path:
            if not os.path.isfile(args.in_path):
                print(f"Ошибка: файл не найден: {args.in_path}", file=sys.stderr)
                return 2
            source = read_file(args.in_path)
        else:
            source = read_console()

        result = calculate(source)

        if args.out_path:
            write_file(args.out_path, result)
            print(f"Результат записан в файл: {args.out_path}")
        else:
            write_console(result)

        return 0
    except (ValueError, OSError) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())