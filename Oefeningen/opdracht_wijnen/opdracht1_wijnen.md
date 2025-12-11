### Dataset
Gebruik de **Wine dataset** van `sklearn`, die verschillende chemische eigenschappen van wijnmonsters bevat.

### Stappen

1. **Importeer Nodige Bibliotheken**
   Importeer de benodigde bibliotheken

2. **Laad de Wine Dataset**
   Gebruik `pd.read_csv` om de dataset te laden en om te zetten naar een pandas DataFrame.

3. **Data Verkenning**
   Toon de eerste paar rijen van de DataFrame en krijg een samenvatting van de data.

4. **Data Manipulatie**
   Voer de volgende manipulaties uit op de DataFrame:
   - Maak een nieuwe kolom genaamd `total_acidity` door de kolommen `fixed acidity` en `volatile acidity` bij elkaar op te tellen.
   - Maak een andere kolom genaamd `alcohol_sugar_ratio` door de kolom `alcohol` te delen door de kolom `residual sugar`.
   - Maak een kolom genaamd `doubleQuality` de kolom `quality` te vermenigvuldigen met `2`.

5. **Extra Vragen**
   - Hoeveel unieke wijnsoorten zijn er in de dataset?
   - Wat is de gemiddelde waarde van `total_acidity` voor elke wijnsoort?
   - Hoe verhoudt de `alcohol` zich tot de `residual sugar` voor de verschillende wijnsoorten?

### Analyse
Analyseer de resultaten en beschrijf je observaties.