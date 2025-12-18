def validation_agg(validations_):    
    ''' 
    My little helper # 2
    Writing my own aggregation function... very exciting!
    '''
    unique_values = validations_.unique()   #list of unique values in the rows per 'dag'
    return unique_values[0] if len(unique_values) == 1 else 'Mixed'

def validate_total_generated(SEMS_df):
    '''
    Removes rows with non-increasing 'Total_Generated(kWh)' aka cumsum of production
    and returns the 'cleaned dataframe'
    '''
    import pandas as pd
    if not 'Total_Generated(kWh)' in SEMS_df.columns:
        raise KeyError("f{SEMS_df} is not for me, I am looking for column 'Total_Generated(kWh)'" )
    invalid_count = 1
    
    while invalid_count > 0:                                           # Fragiel: Als er ergens een grote foute waarde in 'Total_Generated(kWh)' staat kan die alle downstream data droppen
        SEMS_df = SEMS_df.sort_index()
        total_generated = SEMS_df['Total_Generated(kWh)']              # Isoleer de kolom in kwestie, is nu een Series
        is_increasing = total_generated >= total_generated.shift(1)    # Dé check: Boolean mask: "Ben ik groter dan mijn voorganger?"
        is_valid = pd.Series(True, index=SEMS_df.index)                # nieuwe kolomm voor later, default = True
        is_valid[1:] = is_increasing[1:]                               # , skip index 0 en de laatste, die heeft geen voorganger
        
        SEMS_df['Total_is_valid'] = is_valid                           #Series invoegen met de validatie-resultaat
        invalid_count = (SEMS_df['Total_is_valid'] == False).sum()  
        print(f"Er zijn {invalid_count} 'invaliden' gevonden - waarbij de cumsum daalde t.o.v. de vorige rij!")
        SEMS_df = SEMS_df.drop(SEMS_df[SEMS_df['Total_is_valid'] == False].index)
        SEMS_df.drop(columns=['Total_is_valid'], inplace=True)

    return SEMS_df
    

def verify_daterange(df):
    '''
    author's little helper # 2
    Dat alle dagen in dataset zitten is niet vanzelfsprekend
    '''
    from datetime import timedelta
    import warnings
    n_days = (df.index.max() - df.index.min()+ timedelta(days=1)).days    #rekenen met dagen, zorg dat je geen dag verliest!
    if n_days == len(df):
        print(f'Dataset bevat {n_days} dagen, geen ontbrekend! \nDate range: {df.index.min().date()} -> {df.index.max().date()}\n')
    elif n_days < len(df):
        print(f' {n_days} days n range, {len(df)} lines of data, do we have {len(df) - n_days} duplicates?')
    else: 
        warnings.warn(f'Dataset is missing {n_days-len(df)} dates')
    return f'Verification complete'


def export_dagtotalen(df, export_path, filename):
    '''
    author's little helper, schrijft dataframs naar een *.csv
    Een *.csv wegschrijven, ça va de seul!
    'params df, export_path, filename: 'geef het pandas dataframe, een pad en een bestandsnaam.csv in 
    '''
    import os
    if os.path.exists(export_path.joinpath(filename)) == True:
        os.remove(export_path.joinpath(filename))
        print(f'this file:" {filename}  already existed -> deleted existing file')
    else:
        os.makedirs(export_path, exist_ok=True)
        print(f'Attempting to write {filename}\n')
            
        # Write the DataFrame to the csv file
        
    df.to_csv(export_path.joinpath(filename))
    print(f"File has been written to: {export_path.joinpath(filename)}")

def get_daylight_duration(date_str, latitude=51.1667, longitude=5.0333):
    from astral import LocationInfo
    from astral.sun import sun
    """
    Berekent de daglichtlengte voor een gegeven datum en locatie.

    Args:
        date_str (str): De datum in de vorm 'YYYY-MM-DD'.
        latitude (float): De breedtegraad van de locatie.
        longitude (float): De lengtegraad van de locatie.

    Returns:
        timedelta: De duur van het daglicht.
        None: Als er een fout optreedt.
    """
    try:
        city_name = "Laakdal"  # Een naam voor de locatie
        region_name = "Antwerp"  # Een regio
        timezone = "Europe/Brussels"  # Belangrijk voor de juiste tijden
        city = LocationInfo(city_name, region_name, timezone, latitude, longitude)
        s = sun(city.observer, date=date_str)
        sunrise = s["sunrise"]
        sunset = s["sunset"]
        daylight_duration = sunset - sunrise
        return daylight_duration.seconds
    except Exception as e:
        print(f"Er is een fout opgetreden: {e}")
        return None


def min_days_to_solstice(date):   # deze heb ik volledig zelf bedacht en gemaakt. 
    '''
    berekent hoeveel dagen verwijderd de date is tot de volgende of vorige 20-juni,
    welkeender kleiner is
    bv 
    '''
    from datetime import datetime, timedelta
    year, next_year = date.year, date.year +1
    days_to_current = abs((date - datetime(year, 6, 20)).days) 
    days_to_next = abs((date - datetime(next_year, 6, 20)).days)
    min_dist = min(days_to_current, days_to_next)
    return min_dist


def preprocess_fluvius_daily(raw_dir_set = False, export_dir_set=False, filewriter= True, return_df = True):
    '''
    helper function to read csv files exported from the Fluvius 'netbeheerder' website
    containing data regarding electricity consumption from- and injection to - the grid
    param : raw_dir_set, export_dir_set : set both an input and export Path-like object, entering only one will raise an error
        setting both to false defaults to author's excellent choise in Path() objects
    param : filewriter : when True, will write to disk
    param : return_df : returns a dataframe
    '''
    #imports
    import pandas as pd
    from pathlib import Path
    from helpers import validation_agg, export_dagtotalen, verify_daterange

    #variables:

    csv_suffix = 'dagtotalen.csv'
    export_file_name = "Fluvius_dagtotalen.csv"
    
    locs=dict()
    
    if filewriter == return_df == False:
        raise NotImplementedError(f"I don't know what you want me to return")
        
    if not(raw_dir_set == export_dir_set == False):
        locs['fluvius_path']  = raw_dir_set
        locs['export_folder'] = export_dir_set  
        if raw_dir_set and filewriter and Path(export_dir_set).exists():
            raise FileExistsError('You must enter truthy Pathlike objects for both raw and export Paths')
    
    locs = dict({ 'fluvius_path' : Path('./data/raw/Fluvius'),
                'export_folder' : Path('./data/preprocessed/Fluvius')})   
    if raw_dir_set:
        locs['fluvius_path']  = Path(raw_dir_set)
    if export_dir_set:
        locs['export_folder'] = Path(export_dir_set)
    
    # using the data files with daily totals for plotting later, list the csv files:
    
    fluvius_file_list = [x for x in Path.iterdir(locs['fluvius_path']) if (str(x).endswith(csv_suffix) and x.is_file())]    # the *.csv that meet my filename-criterium
    
    merging_df = pd.DataFrame()
    for file in fluvius_file_list:
        read_csv = pd.read_csv(file, delimiter=";", decimal=",")    #Belgian data source
        merging_df = pd.concat((merging_df,read_csv))
    
    fluvius_data = merging_df.copy()
    
    # lets cleanup the table 
    # Omschrijving: all N/A; EAN/meter/metertype: only 1 (digtal) meter; Eenheid can be added to Volume)
    
    droplist = ['Omschrijving','Eenheid','EAN-code','Meter','Metertype','Van (tijdstip)','Tot (datum)','Tot (tijdstip)']
    fluvius_data = fluvius_data.rename(columns={"Volume":"Volume (kWh)","Van (datum)":"Dag"})
    fluvius_data = fluvius_data.drop(columns=droplist)
    print(f'\nDeze kolommen zijn gedropt: {droplist}\n')
    # dtype update:
    fluvius_data['Dag'] = pd.to_datetime(fluvius_data['Dag'], format="%d-%m-%Y")
    
    print(f'{int(fluvius_data.duplicated().sum())} duplicate rijen gedetecteerd.\n')
    print(f"Ik heb maar een enkel tarief voor 'gebruik' and 'injectie' dus someren we Dag & Nacht kolommen\n")
    pivot_temp = fluvius_data.pivot(index='Dag',columns=('Register'),values=('Volume (kWh)'))
    
    print(f'Pivot table complete - output: \n')
    display(pivot_temp )
    
    validation_data = fluvius_data.loc[:,('Dag','Validatiestatus')].pivot_table(index='Dag', aggfunc=validation_agg) 
    print(f'\nPre-join check: zijn de Dataframes van gelijke lengte? dus hetzelfde aantal dagen? -->' 
          f'{len(pivot_temp) == len(validation_data)}\n')
    
    fluvius_data = pd.merge(left = pivot_temp, right = validation_data, how='inner', on='Dag')
    
    #Are there any 'Mixed' validation? - > No
    

    
    fluvius_data['Afname (Kwh)'] = fluvius_data['Afname Dag'] + fluvius_data['Afname Nacht']
    fluvius_data['Injectie (Kwh)'] = fluvius_data['Injectie Dag'] + fluvius_data['Injectie Nacht']
    fluvius_data = fluvius_data.drop(columns=['Afname Dag','Afname Nacht','Injectie Dag','Injectie Nacht'])
    fluvius_data.sort_values(by='Dag')
    
    # sanity check

    verify_daterange(fluvius_data)

    if filewriter:
        export_dagtotalen(fluvius_data, locs['export_folder'],export_file_name)

    if return_df:
        print('')
        return fluvius_data

def preprocess_SEMS_daily(raw_dir_set = False, export_dir_set = False, filewriter= True, return_df = True):
    '''
    helper function to read csv files exported from the SEMS (solar inverter company) website
    containing data regarding electricity production from the solar inverter to the local in-home grid
    param : raw_dir_set, export_dir_set : set both an input and export Path-lke object, entering only one will raise an error
    setting both to false defaults to author's excellent choise in Path() objects
    param : filewriter : when True, will write to disk
    param : return_df : returns a dataframe
    '''
    # Imports
    import pandas as pd
    from pathlib import Path
    from helpers import verify_daterange, export_dagtotalen
    
    export_file_name = "SEMS_dagtotalen.csv"

    locs=dict()
    
    if filewriter == return_df == False:
        raise NotImplementedError(f"I don't know what you want me to return")
        
    if not(raw_dir_set == export_dir_set == False):
        locs['fluvius_path']  = raw_dir_set
        locs['export_folder'] = export_dir_set  
        if not (Path(raw_dir_set).exists() and Path(export_dir_set).exists()):
            raise FileExistsError('You must enter truthy Pathlike objects for both raw and export Paths')
    
    locs=dict({ 'SEMS_daily' : Path('./data/raw/SEMS/daily'),
                'export_folder' : Path('./data/preprocessed/SEMS')})
    
    daily_list = Path.iterdir(locs['SEMS_daily'])
    df = pd.DataFrame()    #initialize an empty dataframe
    
    for file in daily_list:
        read_file = pd.read_excel(file, header=0, skiprows=20,skipfooter=1)    #each file starts with two superfluous rows + an image, skip these
        df = pd.concat((df, read_file))
    else: 
        df['Date'] = pd.to_datetime(df['Date'] , format="%d.%m.%Y")
        df = df.set_index(['Date'], drop=True)    # reset the index to the date

    # Let's cleanup a little, all we really need is the date + daily production number
    droplist = ['Plant','Classification','Capacity(kW)','Income(EUR)']
    df = df.drop(columns=droplist).sort_index()
    
    print(f'\nDeze kolommen zijn gedropt: {droplist}\n')
    display(df.sample(5))

    if filewriter:
        export_dagtotalen(df, locs['export_folder'],export_file_name)

    if return_df:
        print('')
        return df

def preprocess_SEMS_granular(filewriter= True, return_df = True):

    '''
    helper function to read csv files exported from the SEMS (solar inverter company) website
    containing granular data regarding electricity production from the solar inverter to the local in-home grid
    param : raw_dir_set, export_dir_set : set both an input and export Path-lke object, entering only one will raise an error
    setting both to false defaults to author's excellent choise in Path() objects
    param : filewriter : when True, will write to disk
    param : return_df : returns a dataframe
    '''
    from pathlib import Path
    import pandas as pd
    from tqdm import tqdm
    import os
    
    if filewriter == return_df == False:
            raise NotImplementedError(f"I don't know what you want me to return")
    
    location = {'SEMS_data_path' : Path('./data/raw/SEMS/'),
                'export_folder' : Path("./data/preprocessed/SEMS/"),
               }
    export_file_name = "SEMS_granulair.csv" 
    
    SEMS_file_list = [x for x in location['SEMS_data_path'].iterdir() if x.name.startswith('Historical')]
    
    size_list = dict()     #dict with ({filenames : filesizes})
    for file in SEMS_file_list:
        size_list[file] = file.stat().st_size
    
    # Some data may be missing, resulting in 'abnormally small' files (files of exactly 4096 bytes are invalid excel files [yes, I checked])
    size_list_copy = size_list.copy() # make a copy, as I'm itterating over my dict, and don't want to change the iterable during itteration
    print()  
    for file,size in size_list_copy.items():
        if size <= 4096:
            size_list.pop(file)
            print(file, 'is verwijderd uit de lijst van in te lezen bestanden')
    print()        
    SEMS_table_raw = pd.DataFrame()
    for file in tqdm(size_list.keys(), desc="Extracting File contents"):
        try:
            read_file = pd.read_excel(file, skiprows=2)
            SEMS_table_raw = pd.concat((SEMS_table_raw, read_file))
        except Exception as e:
            print(f"Error reading {file}: {e}")
    else:
        SEMS_table =  SEMS_table_raw.reset_index(drop=True)       
    print('\n')
    # let's do some checks on this final table:
    SEMS_table = SEMS_table_raw.copy()
    print(f'There are {SEMS_table.isna().sum().sum()} missing values')
    print(f'There are {int(SEMS_table[SEMS_table.duplicated()].sum().sum())} duplicates\n')
    
    # Working mode and working mode.1 are redundant
    print(f'PF max: {SEMS_table["PF"].max()} PF min: {SEMS_table["PF"].min()}\n')
    # PF column contains 655.35 -> 65 535 => 0xFFFF looks like missing or 16-bit overflow, PowerFactor == cos(x) expected [-1,1]
    # This PF-deviation is a disabled setting in my invertor installation, so drop this column.
    print(f'RSSI max: {SEMS_table["RSSI"].min()} RSSI min: {SEMS_table["RSSI"].max()}\n')
    # RSSI(Received Signal Strength Indicator) is the strength of received wifi-signal, seems to go 0 -> 101. Interesting.
    # in BE: if voltage (AC) goes over 253V for more than 10 min, inverter should stop injecting current. At 264V, should stop injecting immediatly!
    print(f'Maximal AC-voltage in the dataset: {SEMS_table["Ua(V)"].max()} Volts')
    # Max Vac = 255.1 so not alarming
    #  MPPT parameters are interesting, but not in the scope of this analysis so we will drop them
    #  H Total(h) is cumumulative total hours online, not interesting so drop column
    
    # let's do the cleanup:
    
    SEMS_table = SEMS_table.drop(columns=['H Total(h)','PF','V MPPT 1(V)','I MPPT 1(A)', 'Working Mode.1','I AC 1(A)'])
    SEMS_table= SEMS_table.rename(columns={'Time':'Timestamp','Ua(V)':'AC_Voltage','Working Mode':'Status','RSSI':'Wifi_power',
                                           'F AC 1(Hz)':'Grid_frequency','Total Generation(kWh)':'Total_Generated(kWh)'})
    SEMS_table['Timestamp'] = pd.to_datetime(SEMS_table['Timestamp'], format="%d.%m.%Y %H:%M:%S")
    SEMS_table['Total_Generated(kWh)'] = SEMS_table['Total_Generated(kWh)'].where(SEMS_table['Total_Generated(kWh)'] >2)
    # SEMS_table = SEMS_table.drop_duplicates('Timestamp')    # zeldzaam maar soms zijn er 2 dezelfde timestamps (N=12)
    SEMS_table = SEMS_table.set_index('Timestamp')
    
    SEMS_table = validate_total_generated(SEMS_table)   #remove erroneous rows that how non ascending cumsum 'Total_Generated(kWh)'
    
    SEMS_table_resampled15m = ((SEMS_table[['Power(W)','AC_Voltage','Temperature(℃)','Grid_frequency','Total_Generated(kWh)']])
                            .resample('15min')
                            .agg({'Power(W)':'mean','AC_Voltage':'max','Temperature(℃)':'max','Grid_frequency':'max', 'Total_Generated(kWh)': lambda x: x.max()- x.min() })
                           )
        
    SEMS_table_resampled60m = ((SEMS_table[['Power(W)','AC_Voltage','Temperature(℃)','Grid_frequency','Total_Generated(kWh)']])
                            .resample('60min')
                            .agg({'Power(W)':'mean','AC_Voltage':'max','Temperature(℃)':'max','Grid_frequency':'max', 'Total_Generated(kWh)': lambda x: x.max()- x.min() })
                           )
    SEMS_table_resampled15m.rename({'Total_Generated(kWh)': '15min_Generated(kWh)'}, axis=1, inplace=True)
    SEMS_table_resampled60m.rename({'Total_Generated(kWh)': '1h_Generated(kWh)'}, axis=1, inplace=True)
                                   
    print(f'\n-----This is the SEMS granular data resampled to 15min: ')
    display(SEMS_table_resampled15m)
    
    # The facts tabel dim_status are now pre-processed: let's write some a csv files
    
    tables= [SEMS_table, SEMS_table_resampled15m, SEMS_table_resampled60m]
    file_names = ([fr"{location['export_folder']}/SEMS_table_granular.csv",
                   fr"{location['export_folder']}/SEMS_table_15min.csv",
                   fr"{location['export_folder']}/SEMS_table_60min.csv"])
    
    if filewriter:
            Path.mkdir(Path('./data/preprocessed/SEMS'),exist_ok=True)
            for table,file in zip(tables,file_names):
                if os.path.exists(file) == True:
                    os.remove(file)
                    print("this file:", file,", already existed -> deleted existing file")
                else:
                    print(file,"does not exist, attempting to write file")
                
                # Write the DataFrames to the csv files
            
                table.to_csv(file)   
                print(f"-> Table has been written to: {file}")
    
    
    if return_df:
        print('')
        return SEMS_table, SEMS_table_resampled15m, SEMS_table_resampled60m


def preprocess_fluvius_kwartier(raw_dir_set = False, export_dir_set=False, filewriter= True, return_df = True):
    '''
    helper function to read csv files exported from the Fluvius 'netbeheerder' website
    containing data regarding electricity consumption from- and injection to - the grid
    param : raw_dir_set, export_dir_set : set both an input and export Path-lke object, entering only one will raise an error
        setting both to false defaults to author's excellent choise in Path() objects
    param : filewriter : when True, will write to disk
    param : return_df : returns a dataframe
    '''
    #imports
    import pandas as pd
    from pathlib import Path
    from helpers import validation_agg, export_dagtotalen, verify_daterange

    #variables:

    csv_suffix = 'kwartiertotalen.csv'
    export_file_name = "Fluvius_15min.csv"
    locs=dict()
   
    if filewriter == return_df == False:
        raise NotImplementedError(f"I don't know what you want me to return")
        
    if not(raw_dir_set == export_dir_set == False):
        locs['fluvius_path']  = Path(raw_dir_set)
        locs['export_folder'] = Path(export_dir_set)
        if not (Path(raw_dir_set).exists() and Path(export_dir_set).exists()):
            raise FileExistsError('You must enter truthy Pathlike objects for both raw and export Paths')
    
    locs=dict({ 'fluvius_path' : Path('./data/raw/Fluvius'),
                'export_folder' : Path('./data/preprocessed/Fluvius')})
   
    if raw_dir_set:
        locs['fluvius_path']  = Path(raw_dir_set)
    if export_dir_set:
        locs['export_folder'] = Path(export_dir_set)
    
    # Listing the csv files:
    
    fluvius_file_list = [x for x in Path.iterdir(locs['fluvius_path']) if (str(x).endswith(csv_suffix) and x.is_file())]    # the *.csv that meet my filename-criterium
    
    df = pd.DataFrame()
    for file in fluvius_file_list:
        read_csv = pd.read_csv(file, delimiter=";", decimal=",")    #Belgian data source
        df = pd.concat((df,read_csv))

    # dtype update:
    df['Timestamp'] = pd.to_datetime(df['Van (datum)'] + ' ' + df['Van (tijdstip)'], format="%d-%m-%Y %H:%M:%S")   
    print(f'{int(df.duplicated().sum())} duplicate rijen gedetecteerd.\n')
    print(f"Ik heb maar een enkel tarief voor 'gebruik', dus someren we Dag & Nacht kolommen\n")
    
    # lets cleanup the table 
    # Omschrijving: all N/A; EAN/meter/metertype: only 1 (digtal) meter; Eenheid can be added to Volume)
    df = df.drop_duplicates()    # Bug bij fluvius geeft soms duplicate rijen, is gemeld bij Fluvius
    droplist = ['Omschrijving','Eenheid','EAN-code','Meter','Metertype','Van (tijdstip)','Tot (datum)','Tot (tijdstip)',"Van (datum)"]
    df = df.rename(columns={"Volume":"Volume (kWh)"})
    df = df.drop(columns=droplist)
    print(f'\nDeze kolommen zijn gedropt: {droplist}\n')
    pivot_temp = df.pivot_table(index='Timestamp', values=['Volume (kWh)'], columns='Register', aggfunc='max' )
    print(f'Pivot table complete - output: \n')
    display(pivot_temp)
    validation_data = df.loc[:,('Timestamp','Validatiestatus')].pivot_table(index='Timestamp', aggfunc=validation_agg) 
    print(f'\nPre-join check: zijn de Dataframes van gelijke lengte? dus hetzelfde aantal dagen? --> ' 
          f'{len(pivot_temp) == len(validation_data)}\n')
    
    pivot_temp.columns = pivot_temp.columns.droplevel(0)    #drop the multi-index
    df = pd.merge(left = pivot_temp, right = validation_data, how='inner', on='Timestamp')
    
    print(f"Er zijn {int((df['Validatiestatus'] == 'Mixed').sum())} met een 'Mixed' Validatiestatus, dit kan wijzen op geschatte waarden (interpolatie vanuit Fluvius)\n of ontbrekende waarden (de meter stond uit). \n")

    df['Afname (Kwh)'] = df['Afname Dag'].fillna(0) + df['Afname Nacht'].fillna(0)
    df['Injectie (Kwh)'] = df['Injectie Dag'].fillna(0) + df['Injectie Nacht'].fillna(0)
    df = df.drop(columns=['Afname Dag','Afname Nacht','Injectie Dag','Injectie Nacht'])
    df['Injectie (Kwh)'] = -df['Injectie (Kwh)']     #voor gemaak in berekeningen zijn dit negatieve floats
    df.sort_values(by='Timestamp')

    # Sanity check
    
    def verify_daterange(df):
        '''
        author's little helper # 2
        Dat alle dagen in dataset zitten is niet vanzelfsprekend
        '''
        from datetime import timedelta
        import warnings
        n_days = (df.index.date.max() - df.index.date.min()+ timedelta(days=1)).days    #rekenen met dagen, zorg dat je geen dag verliest!
        if n_days == len(set(df.index.date)):
            print(f'Dataset bevat {n_days} dagen, geen ontbrekend! \nDate range: {df.index.min().date()} -> {df.index.max().date()}\n')
        elif n_days < len(set(df.index.date)):
            print(f' {n_days} days n range, {len(set(df.index.date))} unique dates, do we have {len(set(df.index.date)) - n_days} duplicates?')
        else: 
            warnings.warn(f'Dataset is missing {n_days-len(set(df.index.date))} dates')
        return f'Verification complete'
    
    verify_daterange(df)
    
    if filewriter:
        export_dagtotalen(df, locs['export_folder'],export_file_name)

    if return_df:
        print('')
        df_60m = df.resample('60min').agg({'Validatiestatus': validation_agg, 'Afname (Kwh)':'sum','Injectie (Kwh)':'sum'})
        
        return df, df_60m





    