# Temtris.py

![Temtris](https://user-images.githubusercontent.com/57668948/202525057-6eb53a06-a879-4e1e-97bc-5c44f1d58734.png)

## Wprowadzenie

`Temtris.py` to port Temtrisa z konsoli NES napisanego w asemblerze 6502 na język Python.

Repozytorium projektu `Temtris (NES)`:

[https://github.com/Kimel-PK/Temtris](https://github.com/Kimel-PK/Temtris)

Projekt został stworzony jako projekt zaliczeniowy z przedmiotu Język Python na studia. Aktualna wersja oparta jest na Temtrisie (NES) w wersji 1.5.4

## Sterowanie

Przyciski kontrolera NES zostały przeniesionę na klawiaturę w następujący sposób:

### Gracz 1

- ←↓→ - ruch klocka
- K - obrót klocka przeciwnie do ruchu wskazówek zegara
- L - obrót klocka zgodnie z ruchem wskazówek zegara
- Enter - Start gry / pauza
- Prawy shift - zmień tryb gry / następna melodia

![kontroler 1](https://user-images.githubusercontent.com/57668948/204330494-e2bbfb67-a95b-4865-9c9a-90178ade0fb5.png)

### Gracz 2

- VBN - ruch klocka
- Z - obrót klocka przeciwnie do ruchu wskazówek zegara
- X - obrót klocka zgodnie z ruchem wskazówek zegara
- Enter - Start gry / pauza
- Prawy shift - zmień tryb gry / następna melodia

![kontroler 2](https://user-images.githubusercontent.com/57668948/204330534-1aab3375-fa96-4bcc-a4e8-425dbcb337e5.png)

## Wymagania

`Temtris.py` został napisany z wykorzystaniem poniższych wersji bibliotek:

```text
Python 3.11.0
pygame 2.1.3.dev8
SDL 2.0.22
```

Zainstaluj wymagane biblioteki ręcznie lub pobierz plik `requirements.txt`. Następnie uruchom wiersz poleceń / terminal i wpisz:

```console
pip install -r requirements.txt
```

## Uruchamianie

### Plik wykonywalny

> Na razie tylko dla systemu Windows

1. Pobierz najnowsze wydanie Temtrisa pod twój system operacyjny.
2. Uruchom pobrany plik

### Kopia repozytorium

1. Pobierz repozytorium i wypakuj je
2. Uruchom wiersz poleceń / terminal w miejscu, w którym znajduje się plik `Temtris.py`
3. Wpisz polecenie
    - W systemie Windows:

    ```console
    python .\Temtris.py
    ```

    - W systemach Linux / MacOS

    ```console
    python Temtris.py
    ```
