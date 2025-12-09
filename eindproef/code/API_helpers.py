def enter_the_code():
    # Imports
    from hashlib import sha256
    from IPython.display import clear_output
    import ipywidgets as widgets
    from IPython.display import display
    from datetime import date, timedelta
    import requests
    import json
    from pathlib import Path
    from pygoodwe import SingleInverter
    from time import sleep
    import pandas as pd
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import datetime
    from IPython.display import display, HTML

    k=3
    for i in range(k):
        print(f'Poging {i} van {k}\n:')
        secret_code = input(f'Geef de code in om het wachtwoord en omvormer-ID te genereren, Q of af te sluiten')
        secret_hex = sha256(secret_code.encode('utf-8')).hexdigest()     # input als bytestring meegeven aan de hasher, en hex-waarde outputten
        
        if secret_code.lower() == 'q':
            print('---- ABORT ----')
            return None
            
        elif secret_hex == '0d99a53dac94c516caaac356e6c2c7a996a8f46f483571075a7605c1d02b31ab':
            clear_output()    # ik wil niet dat de secret na het testen in de output blijft staan, zou deze hashing-ramtamtam overbodig maken.
            print('\n🟩🟩🟩✔️😀 Die code is correct, klaar om API calls te doen! 😀✔️🟩🟩🟩\n')

            args = {'gw_station_id' : secret_code+'-cd93-4ff9-b6e7-6c24e26511a4' , 
                    'gw_account' : 'wim.pierson@gmail.com',
                    'gw_password' : '*'+secret_code+'*',
                    'base_url' : "https://eu.semsportal.com/api/",
                    'city' : 'Laakdal',
                    'User_Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
                    'token' : '{"version":"v2.0.4","client":"ios","language":"en"}'
                   }
            return args
            
        else:
            print('\n❌❌❌ Code foutief! probeer nog eens! ❌❌❌\n')
    else:
        print(f'\n😐😑😣😩 Helaas, na {k} pogingen is het niet gelukt om de code in te geven, hier stopt het. 😩😣😑😐\n')
        return None

def kies_datum(API_details, animeer_deze_dag, toon_historie):

    """
    Creëert een widget met een datumkiezer en knoppen om een API call te starten.

    Args:
        animeer_deze_dag (callable): De functie die wordt aangeroepen voor 'Enkel deze dag'.
                                            Moet een datumobject als argument accepteren.
                                            schrijft een excel weg in ./data/temp en animeert deze data
        toon_history (callable): De functie die wordt aangeroepen voor 'Historie van 2 weken vanaf deze dag'.
                                                Moet een start- en einddatumobject als argumenten accepteren.
                                                schrijft een excel weg in ./data/temp

    Returns:
        Een VBox widget die de datumkiezer, periodeknoppen en verwerkingsknop bevat.
    """
    
    datum_label = widgets.Label(value="Selecteer een datum:")
    datum_selectie = widgets.DatePicker(
        disabled=False,
        value=date.today()
    )

    periode_keuze = widgets.RadioButtons(
        options=['Enkel deze dag', 'Historie van 2 weken vanaf deze dag'],
        description='Kies een periode:',
        disabled=False,
        layout=widgets.Layout(width='700px')
    )

    verwerk_knop = widgets.Button(description="Verwerken")
    resultaat_output = widgets.Output()

    def verwerk_klik(b):
        with resultaat_output:
            resultaat_output.clear_output()
            gekozen_datum = datum_selectie.value
    
            if periode_keuze.value == 'Enkel deze dag':
                if gekozen_datum > date.today():
                    raise ValueError(f"De datum: '{gekozen_datum}' : De historiek ligt niet zeker niet in de toekomst 😵‍💫")
                animeer_deze_dag(API_details, gekozen_datum)
            elif periode_keuze.value == 'Historie van 2 weken vanaf deze dag':
                print()
                start_datum = gekozen_datum
                eind_datum = gekozen_datum + timedelta(days=14)    #check of het incluis of niet-incluise date is, pas day-delta aan naar 13 of 14 resp.
                if eind_datum > date.today():
                    raise ValueError(f"De einddatum: '{eind_datum}' : ligt in de toekomst. Het is enkel toegelaten historiek te consulteren t.e.m {start_datum - timedelta(days=1)}")
                toon_history(API_details, start_datum, eind_datum)

    verwerk_knop.on_click(verwerk_klik)

    return widgets.VBox([datum_label, datum_selectie, periode_keuze, verwerk_knop, resultaat_output])


def toon_history(API_details, start_datum, eind_datum):    

        
    start_ = start_datum.strftime(format="%Y-%m-%d %H:%M")
    end_ = eind_datum.strftime(format="%Y-%m-%d %H:%M")
    print(f'\n--> Logging in...\n')
    login_token = SEMS_login(API_details)
    
    print(f'\n--> Generating payload for {start_} --> {end_}\n')
    
    API_details["start_datum"], API_details["eind_datum"], API_details["login_token"] = start_datum, eind_datum, login_token    # API_details aanvullen
    
    payload={
        "tm_content": {"qry_time_end": end_, "qry_time_start": start_,
        "times": 5, "qry_status": 0, 
        "pws_historys": [
            {    "id": "0905ac27-cd93-4ff9-b6e7-6c24e26511a4",
                "pw_name": "22_1_garage",
                "status": -1,
                "inverters": [
                     {  "sn": "52000SSX207W0532",
                        "name": "Inverter_22_1",
                        "change_num": 0,
                        "change_type": 0,
                        "relation_sn": None,
                        "relation_name": None,
                        "status": -1     
                     }]}],
        "targets": [{
                "target_key": "Vac1",
                "target_index": 9},
            {   "target_key": "Fac1",
                "target_index": 15},
            {    "target_key": "Pac",
                "target_index": 18},
            {   "target_key": "WorkMode",
                "target_index": 19},
            {   "target_key": "Tempperature",
                "target_index": 20},
            {  "target_key": "ETotal",
                "target_index": 22 },   
            {   "target_key": "Reserved5",
                "target_index": 36}]}
        }
    print(f'----> Payload Generated')
    
    print(f'------> Requesting data')
    
    API_request = requests.Session()
    response = API_request.post(
        url = API_details['base_url'] + "api/HistoryData/ExportExcelStationHistoryData",
        headers = {"User-Agent": API_details['User_Agent'], "Token": login_token},
        json = payload, 
        timeout = 60)     # Het kan even duren voordat er een response komt uit China ...

    response_json = response.json()
    file_id = response_json.get('data').get('qry_key')
    print(f'--------> Data ID has been returned')
    payload_download = {"file_id": file_id}
    print(f'----------> Payload (file-ID) : {payload_download}')
    print(f'------------> Initiating download\n')
    file_download_path = get_data_file(API_details, payload_download)
    print(f'--------------> Download complete to {file_download_path}')
    
    return(file_download_path)

def SEMS_login(API_details, timeout: int = 10):

    """does the login and generates token"""
    login_payload = {
        "account": API_details['gw_account'],
        "pwd": API_details['gw_password'],
    }
    login_request = requests.Session()
    try:
        response = login_request.post(
            API_details['base_url'] + "v2/Common/CrossLogin",
            headers={ "User-Agent": API_details['User_Agent'],"Token": API_details['token']},
            data= login_payload,
            timeout= timeout,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as exp:
        print(f"{exp=}")
        return False

    login_reponse = response.json()
    if login_reponse.get("code") != 0:
        print(f"{data=}")
        return f'failed to login'

    if login_reponse.get("api"):
        print(login_reponse.get("api"), '\nToken generated')
    login_token = json.dumps(login_reponse.get("data"))
    
    return login_token

def get_data_file(API_details, payload_download):

    API_request = requests.Session()
    data_file_response = API_request.post(
        url = "https://eu.semsportal.com/api/HistoryData/GetStationHistoryDataFilePath",
        headers = {"User-Agent": API_details['User_Agent'], "Token": API_details["login_token"]},
        data = payload_download,
        timeout = 14)

    data_file_response.raise_for_status()
    download_url = data_file_response.json().get('data', {}).get('file_path')

    if download_url is None:
        print("Failed to get file path from ",download_url)
    else:
        downloaded_file = API_request.get(download_url, timeout=14)
        downloaded_file.raise_for_status()
        file_download_path = Path('./data/temp/'+'Historical_'+ str(API_details["start_datum"])+ '_' + str(API_details["eind_datum"])+ '.xls')    # data excludes end_date ##
        file_download_path.write_bytes(downloaded_file.content)

    return file_download_path

def animeer_deze_dag(API_details, datum):

    
    inverter = SingleInverter(
            system_id=API_details['gw_station_id'],
            account=API_details['gw_account'],
            password=API_details['gw_password'])
    print("->Single Inverter aangemaakt!")
        
    print("---> Ophalen van de data\n")   
    filename = './data/temp/'+'Plant_Power_'+str(datum)+'.xls'
    inverter.getDayDetailedReadingsExcel(datum, filename=filename, timeout=30)
    print(f'\n-----> Het bestand is opgeslagen als {filename}\n')

    display(maak_geanimeerde_productiegrafiek(filename))
    sleep(5)

def maak_geanimeerde_productiegrafiek(excel_file):
    """
    Maakt een geanimeerde grafiek van de energieproductie over een dag.
    """


    
    try:
        df = pd.read_excel(excel_file, skiprows=2, header=0)
    except FileNotFoundError:
        print(f"Fout: Het bestand '{excel_file}' is niet gevonden.")
        return

    if df.empty or len(df.columns) < 2:
        print("Fout: Het Excel-bestand is leeg of bevat niet genoeg kolommen.")
        return
    
    
    tijd_kolom = df.columns[0]
    productie_kolom = df.columns[1]

    # Probeer de tijdskolom te parseren
    try:
        df[tijd_kolom] = pd.to_datetime(df[tijd_kolom], format="%d.%m.%Y %H:%M:%S")
        if df[tijd_kolom].isnull().any():
            print("Waarschuwing: Sommige tijdstempels konden niet naar datetime worden geconverteerd.")
    except Exception as e:
        print(f"Fout bij het converteren van tijdskolom: {e}")
        return
    df = df[(df['Time'].dt.time > datetime.time(hour=5)) & (df['Time'].dt.time < datetime.time(hour=22))]
    df = df.dropna(subset=[tijd_kolom, productie_kolom])  # Verwijder onbruikbare rijen

    print(f'\n-------> We bereiden de animatie voor.......\n ')
    
    fig, ax = plt.subplots(figsize=(8,4))
    lijn, = ax.plot([], [], label='Productie', color='indigo')
    punt, = ax.plot([], [], 'ro')
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    x_min = df[tijd_kolom].min()
    x_max = df[tijd_kolom].max().replace(hour=22, minute=0, second=0, microsecond=0, nanosecond=0)      # 22:00 van de huidige dag
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-50,2030)
    fig.autofmt_xdate()

    def animate(i):
        data_point = df.iloc[:i+1]
        x = data_point[tijd_kolom].values
        y = data_point[productie_kolom].values
        lijn.set_data(x, y)

        if len(x) > 0:
            punt.set_data([x[-1]], [y[-1]])
        else:
            punt.set_data([], [])

        return lijn, punt

    ani = animation.FuncAnimation(fig, animate, frames=len(df), interval=50)

    ax.set_xlabel("Tijd")
    ax.set_ylabel("Watt")

    try:
        datum_str = excel_file.split('_')[-1].split('.')[0]
        datum_bestand = pd.to_datetime(datum_str, format='%Y-%m-%d').strftime('%d-%m-%Y')
        ax.set_title(f"PV vermogen doorheen de dag op {datum_bestand}")
    except Exception:
        ax.set_title("Energieproductie")
    plt.tight_layout()
    
    return HTML(ani.to_jshtml(default_mode='once'))
