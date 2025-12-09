# Python Data Developer eindwerk
## Wim Pierson
#24-april-2025#

Dit eindwerk tracht de data van de belgische digitale elektriciteitsmeter te verwerken
en te  combineren met de data van de Goodwe inverter om een geheelplaatje te bekomen
inzake de energiebalans van een woning. Verschillende aspecten komen aan bod:

- Data verzamelen via een een API
- ✨Animatie van de via API verzamelde gegevens ✨
- Een custom API call om historische data te verzamelen (obv. ongedocumenteerde API features)
- Data cleaning
- Diverse visualisaties
- Simulatie van een thuisbatterij
- Simulatie van een elektrische boiler (sanitair warm water)

## Omgeving  
 
de ontwikkelomgeving was een [scipy image](quay.io/jupyter/scipy-notebook) in Docker
met extra dependencies die opgelijst staan in ./code/requirements.txt

## Bestanden

- ./Run all preprocessing.ipynb : Verzamelen en verwerken van alle ruwe data en wegschrijven in een .csv bestand.
- ./SEMS Historical data (API calls).ipynb : Visualiseren van de log van één dag aan PV-vermorgen data met een animatie of 
     opvragen van 2 weken aan historische date, en als *.xls bestand wegschrijven.
- ./Battery_simulation.ipynb : gebruik van de data van de digitale meter en de inverter om een 'perfecte' thuisbatterij te simuleren.
- ./KPIs.ipynb : genereren van enkele sleutel-waarden om de performatie van de PV installatie te beoordelen. bevat de eenvoudige 'boiler' simulatie.
- ./data/* : bevat alle ruwe data en output van de preprocessing. Een temp subfolder wordt gebruikt om API call data weg te schrijven.
- ./code/helpers.py = Voornamelijk helper functie om de ruwe data te 'cleanen'
- ./code/API_helpers.py: Bevat de code om de interactieve API widget te laten functioneren.
- ./code/battery.py : Bevat de Class Battery, met simulatie-method om een thusibatterij te simuleren.
- ./code/extra_visuals : Bevat enkele notebooks gebruikt om extra visualistaties te genereren voor de voorstelling van dit eindwerk, geen andere functies.

## Credits

Voor een van de API calls wordt gebruik gemaakt van het [pygoodwe](https://pypi.org/project/pygoodwe/) pakket. 
(auteur: James Hodgkinson) Op basis hiervan kon ik mijn custom API-call ontwikkelen.