#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Check:
    def is_number(self, value):
        try:
            float(value)  # Попытка преобразовать значение в число
            return True
        except ValueError:
            return False


class Meaning(Check):
    def __init__(self):
        self.mean = input("Введите значение ")

    def __add__(self, rfs):
        if self.is_number(self.mean) and self.is_number(rfs.mean):
            return float(rfs.mean) + float(self.mean)
        return self.mean + rfs.mean


def main():
    x = Meaning()
    y = Meaning()

    print(x + y)


if __name__ == "__main__":
    main()
