import pandas as pd

from etl import ITransformer

class JsonTransformer(ITransformer):
    def transform(self, data: dict[str, pd.DataFrame]) -> dict:

        df = data.get("json_uni_data")

        # Przygotowanie danych do wstawienia
        rows_grupy = set()
        rows_podgrupy = set()
        rows_nazwy_kierunkow = set()
        rows_stopnie = set()
        rows_kierunki = []
        
        # Dla każdej linii w DataFrame
        for _, row in df.iterrows():
            stopien = row.get('stopien', None)
            kierunek = row.get('kierunek', None)
            nazwa_kierunkow = row.get('nazwa kierunkow', None)
            podgrupa = row.get('podgrupa', None)
            grupa = row.get('grupa', None)

            # Pomijanie wierszy, które nie mają wymaganych danych
            if not stopien or not kierunek or not nazwa_kierunkow or not podgrupa or not grupa:
                print(f"Brak wymaganych danych w wierszu: {row}")
                continue

            if stopien.strip().lower() == "brak_danych":
                continue
            
            # Zbieranie unikalnych grup, podgrup, stopni
            rows_grupy.add(grupa)
            rows_stopnie.add(stopien)

            # Zbieranie unikalnych podgrup jako pary (nazwa_podgrupy, grupa)
            rows_podgrupy.add((podgrupa, grupa))

            # Zbieranie unikalnych nazw kierunków jako pary (nazwa_kierunku, nazwa_podgrupy)
            rows_nazwy_kierunkow.add((nazwa_kierunkow, podgrupa))

            # Zbieranie danych o kierunkach
            rows_kierunki.append({
                "stopien": stopien,
                "nazwaKierunku": kierunek,
                "nazwaKierunkow": nazwa_kierunkow
            })
        
        print(rows_grupy)

        
        rows_grupy = {grupa.strip().lower() for grupa in rows_grupy}
        rows_stopnie = {stopien.strip().lower() for stopien in rows_stopnie}

        rows_podgrupy = {
            (podgrupa.strip().lower(), grupa.strip().lower())
            for (podgrupa, grupa) in rows_podgrupy
        }

        rows_nazwy_kierunkow = {
            (nazwa_kierunku.strip().lower(), podgrupa.strip().lower())
            for (nazwa_kierunku, podgrupa) in rows_nazwy_kierunkow
        }

        rows_kierunki = [
            {
                "stopien": kierunek["stopien"].strip().lower(),
                "nazwaKierunku": kierunek["nazwaKierunku"].strip().lower(),
                "nazwaKierunkow": kierunek["nazwaKierunkow"].strip().lower(),
            }
            for kierunek in rows_kierunki
        ]

        return {
            "grupa": pd.DataFrame(sorted(rows_grupy), columns=["nazwa"]),
            "stopien": pd.DataFrame(sorted(rows_stopnie), columns=["nazwa"]),
            "podgrupa": pd.DataFrame(sorted(rows_podgrupy), columns=["nazwa", "grupa"]),
            "nazwa_kierunkow": pd.DataFrame(sorted(rows_nazwy_kierunkow), columns=["nazwa", "podgrupa"]),
            "kierunek": pd.DataFrame(rows_kierunki)
        }