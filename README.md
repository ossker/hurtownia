Klonowanie repo:

```bash
  $ git clone https://github.com/ossker/hurtownia.git
```
Wejdż do głownego folderu, jeżeli nie jesteś:
```bash
  $ cd hurtownia 
```

Zainstaluj virtualenv, jeśli nie masz:

```bash
  $ pip install virtualenv
```

Stwórz wirtualne środowisko (unikamy sytuacji typu: „U mnie działa, a u ciebie nie”):
```bash
  $ python3 -m venv env
```

Za każdym wejściem do projektu aktywuj środowisko:
```bash
  $ env/Scripts/activate
```

Za kazdym razem, gdy coś zanistalujesz w środowisku, dorzuć to do requirements.txt za pomocą tej komendy:
```bash
  $ pip freeze > requirements.txt
```

Jeśli zapiszesz zależności w pliku requirements.txt, inni mogą łatwo odtworzyć dokładnie to samo środowisko u siebe tą komendą:
```bash
  $ pip install -r requirements.txt
```