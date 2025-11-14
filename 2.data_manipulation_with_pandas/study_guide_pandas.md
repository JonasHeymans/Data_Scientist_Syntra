# Python for Data Science – Pandas

Pandas is één van de belangrijkste tools binnen data science.  
Het laat je toe om data te verkennen, op te schonen en te transformeren — allemaal binnen Python.

Deze gids helpt je stap voor stap begrijpen hoe je met Pandas werkt.  
Ze dient als naslagwerk tijdens de oefeningen en projecten in deze module.

---

## 📦 1. Installeren en gebruiken van Pandas

Voordat je met Pandas aan de slag kunt, moet je het installeren.

### Installatie
```bash
pip install pandas
```

Importeer Pandas in je Python-omgeving:
```python
import pandas as pd
```

Vaak gebruik je ook **NumPy** en **Matplotlib** samen met Pandas:
```python
import numpy as np
import matplotlib.pyplot as plt
```

Werk je in **Jupyter Notebook**? Start dan eerst je omgeving:
```bash
jupyter notebook
```

---

## 🧱 2. Pandas-objecten

Pandas bestaat uit drie kernobjecten:

| Object | Beschrijving | Voorbeeld |
|--------|--------------|-----------|
| **Series** | Een eendimensionale gelabelde array | `pd.Series([10, 20, 30])` |
| **DataFrame** | Een tweedimensionale tabel met rijen en kolommen | `pd.DataFrame({'a': [1,2], 'b': [3,4]})` |
| **Index** | Labels voor rijen en kolommen | `df.index` of `df.columns` |

### Het Series-object
```python
import pandas as pd
s = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
print(s)
```
Een Series lijkt op een NumPy-array, maar heeft **labels**. Je kunt ze zien als een kolom uit een Excel-bestand.

### Het DataFrame-object
```python
data = {
    'Naam': ['Bert', 'Sammy', 'Lisa'],
    'Leeftijd': [28, 23, 31],
    'Stad': ['Antwerpen', 'Brussel', 'Gent']
}
df = pd.DataFrame(data)
print(df)
```
Een DataFrame lijkt op een Excel-tabel of SQL-tabel: elke kolom heeft een naam en elke rij een index.

### Het Index-object
De index geeft elke rij en kolom een identiteit.
```python
print(df.index)
print(df.columns)
```
Je kunt ook zelf een index instellen:
```python
df.set_index('Naam', inplace=True)
```

---

## 🎯 3. Data selecteren en indexeren

Met Pandas kun je eenvoudig rijen en kolommen selecteren, filteren en manipuleren.  
Het is belangrijk om het verschil te begrijpen tussen **.loc[]** en **.iloc[]**:

- `.loc[]` selecteert op **label** (naam van rijen of kolommen).
- `.iloc[]` selecteert op **positie** (0-gebaseerde index).

### Kolommen selecteren
```python
df['Leeftijd']           # één kolom
```

### Meerdere kolommen selecteren
```python
df[['Naam', 'Stad']]     # meerdere kolommen
```

### Rijen selecteren
```python
df.loc['Bert']          # via label
```
```python
df.iloc[0]               # via positie
```

### Filteren van rijen
```python
df[df['Leeftijd'] > 25]  # filter op voorwaarde
```

Je kunt meerdere voorwaarden combineren:
```python
df[(df['Leeftijd'] > 25) & (df['Stad'] == 'Antwerpen')]
```

### Slicing van rijen
```python
df.iloc[1:3]  # rijen 1 en 2
```

Bij het filteren is het belangrijk om haakjes rond elke voorwaarde te zetten. Zonder haakjes krijg je fouten.

---

## ⚙️ 4. Operaties uitvoeren op data

Zodra je data hebt geselecteerd, kun je er berekeningen op uitvoeren.  
Pandas is geoptimaliseerd om berekeningen kolomgewijs en efficiënt uit te voeren.

### Rekenkundige operaties
Je kunt eenvoudig berekeningen maken over kolommen:
```python
df['Leeftijd'] + 5
```
Dit verhoogt elke waarde in de kolom ‘Leeftijd’ met 5.

### Functies toepassen op kolommen
Gebruik `.apply()` om functies toe te passen:
```python
df['Leeftijd'].apply(lambda x: x * 2)
```
Of gebruik ingebouwde functies:
```python
df['Leeftijd'].mean()
df['Leeftijd'].max()
df['Leeftijd'].sum()
```

### Nieuwe kolommen maken
Je kunt eenvoudig een nieuwe kolom toevoegen op basis van een berekening:
```python
df['Leeftijd_in_2026'] = df['Leeftijd'] + 1
```

### Operaties tussen kolommen
```python
df['Totaal'] = df['Prijs'] * df['Aantal']
```

### Toepassing met `apply()` op meerdere kolommen
```python
df['Omschrijving'] = df.apply(lambda x: f"{x['Naam']} uit {x['Stad']}", axis=1)
```

Gebruik `axis=1` om per rij te werken, `axis=0` om per kolom te werken.

---

## 🧩 5. Omgaan met ontbrekende data

Ontbrekende waarden komen vaak voor in echte datasets. Je moet kiezen of je ze **verwijdert** of **vervangt**.

### Ontbrekende waarden detecteren
```python
df.isnull()      # toont True voor ontbrekende waarden
df.notnull()     # toont True voor bestaande waarden
```

### Aantal ontbrekende waarden per kolom tellen
```python
df.isnull().sum()
```

### Ontbrekende waarden verwijderen
```python
df.dropna(inplace=True)
```
Je kunt ook alleen rijen verwijderen waar alle waarden ontbreken:
```python
df.dropna(how='all', inplace=True)
```

### Ontbrekende waarden invullen
```python
df.fillna(0, inplace=True)
```
Of met de mediaan of het gemiddelde:
```python
df['Leeftijd'].fillna(df['Leeftijd'].median(), inplace=True)
```

### Forward/Backward fill
Gebruik waarden van vorige of volgende rijen:
```python
df.fillna(method='ffill')   # vorige waarde gebruiken
df.fillna(method='bfill')   # volgende waarde gebruiken
```

Inspecteer altijd voor en na de aanpassing:
```python
df.info()
```

---

## 🔗 6. Datasets combineren

Het combineren van datasets is essentieel als je data uit meerdere bronnen samenbrengt.

### Concateneren en toevoegen
Datasets samenvoegen, verticaal of horizontaal:
```python
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
resultaat = pd.concat([df1, df2])
```

Met `axis=1` kun je kolommen naast elkaar plakken:
```python
pd.concat([df1, df2], axis=1)
```

### Mergen en joinen
Datasets samenvoegen op gemeenschappelijke kolommen (zoals in SQL):
```python
verkopen = pd.DataFrame({'Product': ['A', 'B'], 'Prijs': [100, 200]})
voorraad = pd.DataFrame({'Product': ['A', 'B'], 'Aantal': [30, 12]})

pd.merge(verkopen, voorraad, on='Product', how='inner')
```

Andere join-types:
```python
pd.merge(df1, df2, how='outer')  # alles behouden
pd.merge(df1, df2, how='left')   # alles uit linkse tabel behouden
```

Je kunt ook mergen op indexen met `left_index=True` en `right_index=True`.

---

## 📊 7. Aggregatie en groepering

Met `groupby()` kun je data samenvatten en analyseren. Dit is één van de krachtigste functies van Pandas.

### Voorbeeld
```python
df = pd.DataFrame({
    'Afdeling': ['IT', 'HR', 'IT', 'Financiën', 'HR'],
    'Loon': [3000, 2500, 4000, 5000, 2700]
})

# Gemiddeld loon per afdeling
df.groupby('Afdeling')['Loon'].mean()
```

### Meerdere aggregaties tegelijk
```python
df.groupby('Afdeling').agg(['mean', 'max', 'min', 'count'])
```

### Groeperen op meerdere kolommen
```python
df.groupby(['Afdeling', 'Functie']).mean()
```

### Toepassingen
- Gemiddelde verkoop per maand
- Totaal aantal klachten per productcategorie
- Gemiddelde wachttijd per afdeling

Gebruik `reset_index()` om het resultaat weer als een gewone DataFrame te krijgen:
```python
resultaat = df.groupby('Afdeling')['Loon'].mean().reset_index()
```

---

## 🧮 8. Pivot tables

Pivot tables lijken op Excel-draaitabellen. Ze laten je data samenvatten over verschillende dimensies.

### Eenvoudige pivot table
```python
pd.pivot_table(df, values='Loon', index='Afdeling', aggfunc='mean')
```

### Pivot met meerdere dimensies
```python
pd.pivot_table(df, values='Loon', index='Afdeling', columns='Stad', aggfunc='sum')
```

### Meerdere functies toepassen
```python
pd.pivot_table(df, values='Loon', index='Afdeling', aggfunc=['mean', 'count'])
```

### Waarom pivot tables gebruiken?
- Om snel trends te ontdekken (bv. omzet per regio en maand)
- Om overzicht te creëren in grote datasets
- Om voorbereidende analyses te maken voor visualisaties

---

## 🔤 9. String Operations

Met Pandas kun je tekstkolommen gemakkelijk bewerken met string-methodes. Je hoeft niet te loopen over elke rij: de bewerkingen worden automatisch toegepast op de hele kolom.

### Tekst bewerken
```python
df['Stad'] = df['Stad'].str.upper()
df['Initiaal'] = df['Naam'].str[0]
df['Bevat_A'] = df['Naam'].str.contains('a', case=False)
```

### Veelgebruikte methodes
| Methode | Beschrijving |
|----------|---------------|
| `.str.lower()` | Zet tekst om naar kleine letters |
| `.str.upper()` | Zet tekst om naar hoofdletters |
| `.str.replace()` | Vervang tekens of woorden |
| `.str.contains()` | Controleer of tekst een substring bevat |
| `.str.len()` | Lengte van tekst |

### Combineren met filtering
```python
df[df['Naam'].str.contains('an')]
```
### Splitsen van tekst
```python
df['Voornaam'] = df['Naam'].str.split().str[0]
```

String operations zijn essentieel bij het opschonen van ongestructureerde tekstdata (zoals namen, adressen of productcodes).

---

## 🕒 10. Werken met tijdreeksen

Pandas maakt werken met datum- en tijdgegevens bijzonder eenvoudig.

```python
datums = pd.date_range('2025-01-01', periods=5, freq='D')
ts = pd.Series(np.random.randn(5), index=datums)
ts
```

### Indexeren op tijd
```python
ts['2025-01-03']
ts['2025-01']  # alle data van januari
```

### Resampling en aggregatie
```python
ts.resample('M').mean()  # groepeer per maand
```

### Shifting en rolling windows
```python
ts.shift(1)               # verschuif waarden
```


## ⚡ 12. High-performance Pandas: `eval()` en `query()`

Voor grote datasets is performance belangrijk.

### `eval()` gebruiken
```python
df.eval('Totaal = Prijs * Aantal', inplace=True)
```

### `query()` gebruiken
```python
filter = df.query('Prijs > 100 and Aantal < 50')
```

Gebruik deze functies voor:
- Complexe expressies over meerdere kolommen
- Grote datasets (miljoenen rijen)
- Leesbare en snellere code

---


## ✅ Samenvatting

| Onderwerp | Vaardigheden |
|------------|---------------|
| Installatie | Omgeving opzetten |
| Pandas-objecten | Begrijpen van Series, DataFrame, Index |
| Indexering | Data filteren en selecteren |
| Missing Data | Data opschonen |
| Datasets combineren | Merge, concat |
| Groepering | Inzichten afleiden |
| Pivot Tables | Samenvatten van data |
| String Operations | Tekstdata opschonen |
| Tijdreeksen | Data in tijd analyseren |
| Query/Eval | Efficiënt werken |


---

## 📚 Bronnen

- [Pandas Documentatie](https://pandas.pydata.org/docs/)
- [W3 Schools - Pandas](https://www.w3schools.com/python/pandas/default.asp)
- [Tutorialspoint - Pandas](https://www.tutorialspoint.com/python_pandas/index.htm)
- [Python Data Science Handbook – Jake VanderPlas](https://jakevdp.github.io/PythonDataScienceHandbook/)
- [Azure Machine Learning](https://azure.microsoft.com/en-us/services/machine-learning/)
