# De CRISP-DM Methode: een 6-stappenraamwerk voor data science-projecten  

Machine learning en data science lijken vaak complex. De media doen het soms lijken als magie. In werkelijkheid is het gewoon een gestructureerde aanpak om problemen met data op te lossen.  
De **CRISP-DM**-methode – voluit *Cross Industry Standard Process for Data Mining* – biedt daarvoor een bewezen kader. Het helpt je om van een vaag idee naar een werkend dataproject te gaan, stap voor stap.  

In deze tekst leer je hoe je CRISP-DM toepast op machine learning- en data-analyseprojecten. Het sluit perfect aan bij de thema’s die we behandelen in deze opleiding, zoals **pandas**, **data exploratie & cleaning**, en **matplotlib**.  

---

## Overzicht van de CRISP-DM cyclus

CRISP-DM bestaat uit zes stappen:  

1. **Business Understanding** – Wat wil je oplossen?  
2. **Data Understanding** – Wat weet je al uit de data?  
3. **Data Preparation** – Hoe maak je de data klaar voor analyse?  
4. **Modeling** – Welke algoritmes gebruik je?  
5. **Evaluation** – Hoe goed werkt je model?  
6. **Deployment** – Hoe zet je het resultaat in de praktijk?  

Deze stappen vormen geen rechte lijn. Het is een iteratief proces: je springt vaak terug naar eerdere fases als je iets nieuws ontdekt.  

---

## 1. Business Understanding – Begrijp het probleem

Elk goed data science-project begint met een duidelijke **probleemdefinitie**.  
Niet: *“Ik wil AI gebruiken.”*  
Wel: *“Ik wil het aantal klanten dat hun abonnement opzegt beter voorspellen.”*

Denk hierbij in termen van:
- **Doelstelling**: Wat wil je precies bereiken?
- **Succescriteria**: Wanneer is het project geslaagd?
- **Projectbeperkingen**: Tijd, budget, beschikbare data.

Voorbeeld:  
> “We willen een model bouwen dat voorspelt of een klant zijn contract zal verlengen, zodat we tijdig gepersonaliseerde kortingen kunnen aanbieden.”

Het doel is dus niet *machine learning toepassen om de hype mee te doen*, maar *waarde creëren met data*.

---

## 2. Data Understanding – Verken de data

De **Data Understanding**-fase draait om nieuwsgierigheid. Je wil ontdekken wat er in je data zit, wat er ontbreekt en of de data betrouwbaar zijn. In deze fase zet je jouw analytische bril op: je leert de dataset kennen, stelt vragen en zoekt verbanden.  

### Typische activiteiten
- **Data verzamelen** uit verschillende bronnen (Excel, CSV, API’s, databases).  
- **Data inladen en inspecteren** met `pandas`: hoeveel rijen en kolommen zijn er, welke datatypes komen voor, zijn er null-waarden?  
- **Beschrijvende statistiek** berekenen met `df.describe()` om een eerste idee te krijgen van gemiddelden, spreiding en uitschieters.  
- **Verkenning via visualisaties** met `matplotlib` of `seaborn`: histogrammen, boxplots en scatterplots helpen je patronen of vreemde waarden te ontdekken.  

### Praktische tips
- Controleer of kolomnamen logisch zijn. Onduidelijke namen zoals *var1* of *col2* maak je beter leesbaar.  
- Kijk naar **distributies** (hoe vaak komt iets voor) om te zien of data scheef verdeeld zijn.  
- Maak **correlatiematrices** om te begrijpen welke variabelen samenhangen.  
- Documenteer bevindingen in een notebook — noteer opvallende trends, problemen en hypotheses die je later kunt testen.  

### Voorbeeld:

```python
import pandas as pd
import data_exploration_and_cleaning.pyplot as plt
import seaborn as sns

df = pd.read_csv("klantdata.csv")
print(df.info())
print(df.describe())

sns.boxplot(x=df['inkomen'])
plt.title("Verdeling van inkomens")
plt.show()
```

De uitkomst van deze fase is inzicht: je weet wat je data vertellen, waar de gaten zitten en welke variabelen nuttig kunnen zijn voor modellering.  

---

## 3. Data Preparation – Maak de data klaar

De **Data Preparation**-fase is waar je ruwe data omzet in een bruikbare dataset. Deze stap bepaalt voor 80% het succes van je model. Slechte data leiden onvermijdelijk tot slechte voorspellingen, dus zorg hier voor grondigheid.  

### Typische activiteiten
1. **Data cleaning** – verwijder duplicaten, corrigeer datatypes, vul missende waarden in of verwijder rijen waar nodig.  
2. **Feature selectie** – kies enkel de variabelen die relevant zijn voor je probleem. Overbodige kolommen verhogen enkel de complexiteit.  
3. **Feature engineering** – maak nieuwe kolommen uit bestaande informatie, bv. *leeftijdscategorie*, *dagen sinds laatste aankoop*, of *weekdag van transactie*.  
4. **Normalisatie en standaardisatie** – schaal numerieke waarden zodat alle features op gelijkaardige schalen liggen.  
5. **Encodering van categorische variabelen** – zet tekstcategorieën om naar numerieke waarden met `pd.get_dummies()` of `LabelEncoder`.  

### Praktische tips
- Werk stap voor stap en controleer na elke transformatie met `df.head()`.  
- Visualiseer opnieuw na cleaning: vaak zie je meteen of iets fout gelopen is.  
- Houd een logboek bij van je aanpassingen zodat je proces reproduceerbaar blijft.  

### Voorbeeld:
```python
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Missende waarden opvullen en categorische variabelen coderen
df['leeftijd'] = df['leeftijd'].fillna(df['leeftijd'].median())
df = pd.get_dummies(df, columns=['geslacht'], drop_first=True)

# Schalen van numerieke waarden
scaler = StandardScaler()
df[['inkomen', 'leeftijd']] = scaler.fit_transform(df[['inkomen', 'leeftijd']])

# Train-test-split voor modelbouw
X = df.drop('verlengt_contract', axis=1)
y = df['verlengt_contract']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

Het resultaat van deze fase is een *cleane*, goed gestructureerde dataset die klaar is voor modellering.  

---

## 4. Modeling – Bouw en test je model

Nu pas begint het echte **machine learning**-werk.  
Je kiest een algoritme (bijv. decision tree, logistic regression, random forest) en traint het met je data.

Voorbeeld met scikit-learn:
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X = df[['leeftijd', 'inkomen', 'klachten']]
y = df['verlengt_contract']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)
```

Doel: patronen leren die voorspellen wat er zal gebeuren, of inzicht geven in wat er nu gebeurt.  

---

## 5. Evaluation – Evalueer de prestaties

Je model moet niet enkel werken, maar **betrouwbaar** zijn.  
Daarom vergelijk je de voorspellingen met de echte waarden.

Voor classificatieproblemen gebruik je vaak:
- **Accuracy** (percentage juiste voorspellingen)
- **Precision / Recall**
- **F1-score**
- **Confusion matrix**

Voorbeeld:
```python
from sklearn.metrics import classification_report, confusion_matrix

y_pred = model.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
```

Visualiseer resultaten met `matplotlib` om te zien waar het fout gaat.  
Als het model onvoldoende presteert, keer je terug naar **Data Preparation** of **Modeling**.  

---

## 6. Deployment – Breng het resultaat tot leven

De laatste stap is **actie**.  
Een goed model is pas waardevol als het gebruikt wordt:  
- Een dashboard in Power BI of Streamlit.  
- Een rapport in Excel of PDF.  
- Een API die automatisch voorspellingen doet.  

Soms blijft het bij een proof of concept. Soms groeit het uit tot een volwaardig systeem.

Belangrijk:
- Documenteer wat je hebt gedaan.
- Automatiseer wat herhaalbaar is.
- Plan onderhoud: data verandert, dus je model ook.

---

## Samenvattend

| Stap | Doel | Typische tools |
|------|------|----------------|
| 1. Business Understanding | Probleem begrijpen | Brainstorm, interviews |
| 2. Data Understanding | Data verkennen | pandas, matplotlib, seaborn |
| 3. Data Preparation | Data opschonen | pandas, numpy, sklearn.preprocessing |
| 4. Modeling | Model bouwen | scikit-learn |
| 5. Evaluation | Model testen | sklearn.metrics, matplotlib |
| 6. Deployment | Resultaten toepassen | Streamlit, Power BI, Excel |

---

## Waarom CRISP-DM?

CRISP-DM is geen theorie, het is **praktisch**.  
Het helpt studenten en bedrijven om gestructureerd te denken:  
- Niet meteen code schrijven, maar eerst het probleem begrijpen.  
- Niet meteen een model trainen, maar eerst de data leren kennen.  
- Leren dat mislukkingen deel uitmaken van het proces.

En vooral: **je leert denken als een data scientist**.  

---

