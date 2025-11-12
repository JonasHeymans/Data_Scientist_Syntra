# Notebook: Van NumPy naar Pandas

## 🎯 Doel van deze notebook
In deze notebook leer je hoe **Pandas** voortbouwt op **NumPy** — en waarom het belangrijk is om NumPy goed te begrijpen als je met Pandas werkt.

Je zult ontdekken:
- Hoe Pandas intern gebruik maakt van NumPy
- Wat de verschillen en voordelen zijn tussen NumPy-arrays en Pandas DataFrames
- Wanneer je beter NumPy gebruikt, en wanneer Pandas

---

## 🔢 1. Herhaling: NumPy in één oogopslag

NumPy is een library voor numerieke berekeningen. Het biedt efficiënte **n-dimensionale arrays** en vector-gebaseerde operaties.

```python
import numpy as np

# Een NumPy-array maken
arr = np.array([10, 20, 30, 40])
print(arr)
print(type(arr))

# Basisoperaties
print(arr * 2)
print(arr.mean())
```

Voordelen van NumPy:
- Zeer snel (geschreven in C)
- Ondersteunt vectorisatie (geen loops nodig)
- Compact geheugenverbruik

Beperkingen van NumPy:
- Geen kolomnamen of rijnamen
- Moeilijk te interpreteren bij complexe datasets
- Slecht bestand tegen ontbrekende waarden (`np.nan` geeft vaak fouten bij berekeningen)

---

## 🧱 2. Pandas is gebouwd bovenop NumPy

Pandas gebruikt NumPy-arrays **onder de motorkap**.  
Elke kolom van een Pandas DataFrame is eigenlijk een **NumPy-array** met extra informatie.

```python
import pandas as pd

data = np.array([[10, 20, 30], [40, 50, 60]])
df = pd.DataFrame(data, columns=['A', 'B', 'C'])
print(df)

print(type(df.values))  # NumPy array
```

Pandas combineert de snelheid van NumPy met de leesbaarheid van tabellen.

| Eigenschap | NumPy | Pandas |
|-------------|--------|---------|
| Data type | Array | DataFrame / Series |
| Structuur | Positie-gebaseerd | Label-gebaseerd |
| Ontbrekende waarden | `np.nan`, beperkt | `NaN`, met ingebouwde functies (`fillna`, `dropna`) |
| Leesbaarheid | Minder intuïtief | Kolomnamen en indexen |
| Geschikt voor | Zuiver numerieke data | Gemengde data (getallen, tekst, datums) |

---

## 🔍 3. Waarom Pandas handiger is bij data-analyse

NumPy is perfect voor wiskundige operaties, maar Pandas is gemaakt om **echte datasets** te analyseren.

### 3.1 Met NumPy
```python
data = np.array([[25, 'Antwerpen'], [30, 'Gent'], [22, 'Leuven']])
print(data[:, 0])  # leeftijd ophalen
```
Probleem: je hebt geen kolomnamen. De betekenis van kolom 0 moet je onthouden.

### 3.2 Met Pandas
```python
df = pd.DataFrame({
    'Leeftijd': [25, 30, 22],
    'Stad': ['Antwerpen', 'Gent', 'Leuven']
})
print(df['Leeftijd'])
```
Voordeel: data is **leesbaar**, **gelabeld** en **combineerbaar** met andere datasets.

---

## 🧮 4. Data selecteren en filteren

In NumPy selecteer je met indices:
```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr[0, 1])  # tweede element in eerste rij
```

In Pandas gebruik je labels:
```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
print(df.loc[0, 'B'])  # zelfde resultaat, maar leesbaarder
```

Pandas gebruikt nog steeds NumPy onderliggend, maar biedt een meer menselijke manier om met data te werken.

---

## 🧩 5. Gemengde data en ontbrekende waarden

NumPy kan slechts één datatype per array aan:
```python
arr = np.array([1, 'tekst', 3.5])
print(arr.dtype)  # alles wordt omgezet naar string
```

Pandas laat gemengde types toe per kolom:
```python
df = pd.DataFrame({
    'Naam': ['Jonas', 'Rune', 'Lisa'],
    'Leeftijd': [28, np.nan, 31]
})
print(df)
print(df['Leeftijd'].mean())  # automatisch nan negeren
```
Pandas heeft dus ingebouwde ondersteuning voor **ontbrekende waarden** en **data cleaning**.

---

## ⚡ 6. Vectorisatie en prestaties

Zowel NumPy als Pandas voeren berekeningen vectorieel uit, maar Pandas biedt meer mogelijkheden voor realistische data.

```python
# NumPy
arr = np.array([1, 2, 3])
print(arr * 10)

# Pandas
s = pd.Series([1, 2, 3])
print(s * 10)
```

In beide gevallen krijg je dezelfde snelheid, maar Pandas voegt **labels**, **indexen** en **missende waardenbeheer** toe.

---

## 📊 7. Samenvatting

| Aspect | NumPy | Pandas |
|--------|--------|--------|
| Data type | Array | DataFrame / Series |
| Labels | ❌ Nee | ✅ Ja |
| Missing values | Beperkt | Uitgebreid (`isna`, `fillna`) |
| Mixed data types | Nee | Ja |
| Geschikt voor | Wiskundige berekeningen | Data-analyse |
| Onderliggend gebruikt door | Pandas | - |

---

## 💡 8. Waarom NumPy nog steeds belangrijk is

Ook al werk je meestal in Pandas, **NumPy blijft essentieel**:
- Pandas gebruikt NumPy intern voor berekeningen
- Veel machine learning libraries (zoals Scikit-learn, TensorFlow) gebruiken NumPy arrays
- NumPy-arrays zijn efficiënter bij grote numerieke datasets

Begrijpen hoe NumPy werkt helpt je:
- Fouten beter te begrijpen (Pandas errors verwijzen vaak naar NumPy)
- Complexe berekeningen sneller te schrijven
- Over te schakelen tussen Pandas en ML-libraries

---

## 🧠 9. Oefeningen

1. Maak een NumPy-array en bereken het gemiddelde.
2. Zet datzelfde array om in een Pandas Series en herhaal de berekening.
3. Maak een DataFrame met kolommen `Naam`, `Leeftijd` en `Stad`.
4. Voeg een kolom toe `Leeftijd_volgend_jaar`.
5. Vergelijk hoe Pandas en NumPy omgaan met `NaN`-waarden.

---

## 📚 Verdere bronnen
- [NumPy Documentation](https://numpy.org/doc/stable/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Python Data Science Handbook – Jake VanderPlas](https://jakevdp.github.io/PythonDataScienceHandbook/)

