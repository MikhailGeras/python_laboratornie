import random
from math import*
def plohaya_ugadaika(a, b, c):
    """найти медленным перебором загаданное число c на интервале от a до b, вернуть a и количество сравнений"""
    if not(isinstance(a, int) and isinstance(b, int) and isinstance(c, int)): #проверяем тип данных
        return "Формат не подходит"
    elif b > c: #правильность границ 
        raise ValueError("Неверный интервал")
    elif not (b <= a <= c): #загадываемое число в диапазоне
        raise ValueError("Число вне интервала") 
    elif a == b == c: #случай
        return a, 1
    n = b
    cnt = 1
    while n != a:
        n += 1
        cnt += 1
    return n, cnt
def horosh_ugadaika(a, b, c):
    """найти с помощью бинарного поиска загаданное число c на интервале от a до b, вернуть a и количество сравнений"""
    if not(isinstance(a, int) and isinstance(b, int) and isinstance(c, int)): #проверяем тип данных
        return "Формат не подходит"
    elif b > c: #правильность границ
        raise ValueError("Неверный интервал")
    elif not (b <= a <= c): #загадываемое число в диапазоне
        raise ValueError("Число вне интервала")
    elif a == b == c: #случай
        return a, 1
    cnt = 1
    mn = b
    mx = c+1
    s = [i for i in range(mn, mx)]
    n = s[ceil(len(s)/2)-1]
    while n != a:
        cnt += 1
        if n < a:
            mn = s[s.index(n) + 1]
        if n > a:
            mx = s[s.index(n) - 1]
        s = [i for i in range(mn, mx+1)]
        n = s[ceil(len(s)/2)-1]
    return n, cnt
