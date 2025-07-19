import argparse
import json
import os
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(
        description="Создать пустую карточку персонажа с таймстемпом в имени"
    )
    parser.add_argument("slug", help="slug персонажа (например, anna_petrova)")
    parser.add_argument(
        "--output-dir",
        default="assets/characters",
        help="Папка для сохранения карточки (по умолчанию assets/characters/)"
    )

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{args.slug}.json"
    filepath = os.path.join(args.output_dir, filename)

    # Заготовка: минимально пустая карточка с slug
    character = {"slug": args.slug}

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(character, f, ensure_ascii=False, indent=2)

    print(f"Карточка создана: {filepath}")


if __name__ == "__main__":
    main()
