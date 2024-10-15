#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import logging
import os
import pathlib
import time

class IllegalCount(Exception):
    def __init__(self, count, message="Illegall count"):
        self.count = count
        self.message = message
        super(IllegalCount, self).__init__(message)

    def __str__(self):
        logging.info(f"{self.count} -> {self.message}")
        return f"{self.count} -> {self.message}"

class UnknownCommandError(Exception):
   def __init__(self, command, message="Unknown command"):
       self.command = command
       self.message = message
       super(UnknownCommandError, self).__init__(message)
   def __str__(self):
       return f"{self.command} -> {self.message}"

def add_product(staff, name, market, count):
    """
    Добавить данные о магазине.
    """
    if count < 0:
        raise IllegalCount(count)

    staff.append({"name": name, "market": market, "count": count})
    return staff


def display_products(workers):
    """
    Отобразить список работников.
    """
    if workers:
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 20, "-" * 10
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^10} |".format(
                "№", "Название продукта", "Имя магазина", "Стоимость"
            )
        )
        print(line)
        for idx, worker in enumerate(workers, 1):
            print(
                "| {:>4} | {:<30} | {:<20} | {:>10} |".format(
                    idx,
                    worker.get("name", ""),
                    worker.get("market", ""),
                    worker.get("count", 0),
                )
            )
        print(line)

    else:
        print("Список продуктов пуст.")


def select_products(products, find_name):
    """
    Выбрать продукт с заданным именем.
    """
    result = []
    for product in products:
        if product.get("name_of_product") == find_name:
            result.append(product)

    return result


def save_products(file_name, staff):
    """
    Сохранить всех работников в JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fount:
        json.dump(staff, fount, ensure_ascii=False, indent=4)


def load_products(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main():
    """
    Главная функция программы.
    """
    logging.basicConfig(
        filename='product.log',
        encoding='utf-8',
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename", action="store", help="The data file name"
    )
    parser = argparse.ArgumentParser("products")
    parser.add_argument(
        "--version", action="version", version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add", parents=[file_parser], help="Add a new product"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The product's name",
    )
    add.add_argument(
        "-m", "--market", action="store", help="The market's name"
    )
    add.add_argument(
        "-c",
        "--count",
        action="store",
        type=int,
        required=True,
        help="The count",
    )

    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Display all products"
    )

    info = subparsers.add_parser(
        "info", parents=[file_parser], help="Select the products"
    )

    info.add_argument(
        "-p",
        "--name_product",
        action="store",
        type=str,
        required=True,
        help="The required name of product",
    )

    args = parser.parse_args()
    is_dirty = False
    home_dir = pathlib.Path.home()

    if os.path.exists(args.filename):
        products = load_products(args.filename)
        logging.info("Загружен список продуктов.")
    elif pathlib.Path(f'{home_dir / args.filename}').exists():
        products = load_products(home_dir / args.filename)
        logging.info("Загружен список продуктов.")
    else:
        products = []
        logging.info("Новый список продуктов.")
    
    try:
        if args.command == "add":
            products = add_product(products, args.name, args.market, args.count)
            is_dirty = True
            logging.info(
                f"Добавлен продукт: {args.name}, {args.market}, "
                f"стоимостью {args.count} руб."
            )

        elif args.command == "display":
            display_products(products)
            logging.info("Отображен список продуктов.")

        elif args.command == "info":
            selected = select_products(products, args.name_product)
            display_products(selected)
            logging.info(
                f"Отображен список продуктов по именю {args.name_product}."
            )

        else:
            raise UnknownCommandError(args.command)


        if is_dirty:
            save_products(args.filename, products)
            logging.info("Сохранен список продуктов.")
        
    except UnknownCommandError as exc:
        logging.error(f"Ошибка: {exc}")
        raise UnknownCommandError(args.command)

if __name__ == "__main__":
    main()
