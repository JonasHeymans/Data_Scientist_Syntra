class Battery():
    def __init__(self, capaciteit,STE=1, tank_init=1):
        '''
        : param capaciteit : Max laad-capaciteit van de thuisbatterij, : int,float >0 in kWh
        : param STE : Single Trip Efficiency, welke percentage aan energie gaat er verloren
        tijdens een tranactie (laden/ontladen): float [0.01 , 1 ]
        : param tank_init : Hoeveel kWh zit al in de batterij bij simulatie-start: int [0, capaciteit ]
        
        Ik ben een perfecte batterij, ik laad tot de maximale capaciteit en draineer tot 0.00 %.
        Ik kan op de milliseconde afname en injectie balanceren.
        Mijn round-trip-efficiency is 100% (1kWh laden = 1 kWh ontladen, geen warmte-verliezen).
        Mijn electronica (componenten en on-board SOC, display,.. et al.) verbruiken niets.
        Ook heb ik geen last van spontane ontlading over de tijd.
        Mijn capaciteit is ongevoelig aan de omgevingstemperatuur.
        Er is geen limiet op het vermogen waarmee ik laad en ontlaad.
        Ik verlies geen capaciteit overheen de jaren en heb ongelimiteerde laadcycli.
        Ik ben een stukje code.        
        '''
        self.capacity = capaciteit
        self.tank = tank_init
        self.STE = STE                     # Single trip efficiency
        self.SDFR = 0                      # Self-discharge factor, discharge of the battery over time (You snooze, you lose)
        self.selfconsuption = 0            # Energy needed to run the battery mamagment system
        self.age_factor = 0                # Degradation over time (nothing lasts forever)
        self.cycles = 0                    # Keep track of cycles (metric of of battery fatigue)
        self.Temp_coef = 0                          # Temperature-coëficient (colder = less capacity)
        
        # a wee bit of input validation
        
        if not isinstance(capaciteit,(int, float)):
            raise TypeError(f'expected int or float, not {type(capaciteit(kWh))}')
        elif capaciteit <= 0 :
            raise ValueError('Negative or zéro capacity, are you trying to break my simulator?')
        elif self.STE <=0.01:
            raise ValueError(f'0 or negative efficiency is not allowed ')
        elif self.tank > self.capacity:
            raise ValueError("Can't start with an overcharged battery!")

    def simulate(self, pd_series):
        
        import pandas
        if not isinstance(pd_series, pandas.core.series.Series):
            raise TypeError(f'input expects pandasSeries, I got {type(pd_series)}')
            
        injectie = -pd_series['Injectie (Kwh)']    # injectie is negtief, maar we willen de batterij vullen, maakt dit positive
        afname = -pd_series['Afname (Kwh)']         # afname is positief maar we willen de batterij leeghalen, maak het negatief
        
        delta = injectie + afname  # delta: netto beweging per kwartier, moest hij laden (+) of ontladen/leveren (-)?
        STE = self.STE
        
        if afname > injectie:      #kleine inputvalidatie
            raise ValueError('not the input I was expecting')
        elif delta >0 :   #Laden!
            afname_n = 0    # er is overschot dus de batterij kan alle verbruik vermijden
            injectie_n  = max(0, (self.tank-self.capacity)/STE+delta)    # 0 of het overschot op het net zetten
            self.tank = min(self.capacity, self.tank + delta*self.STE)   # vol=vol, kan niet meer dan 
        elif delta < 0 :  #ontladen
            afname_n = min(0, delta + self.tank/STE)     # als er genoeg in de batterij zit, kan verbruik vermeden, of verminderd tot hij leeg is
            injectie_n  = 0                              # 0 want we hebben tekort, de batterij vermijdt injectie
            self.tank = max(0, delta/STE + self.tank)    #leeg = leeg! kan niet meer geven dan erinzat 
        else:
            injectie_n = injectie
            afname_n = afname                             # als delta = 0 of als er een NaN is?
            
        self.pct = self.tank/self.capacity
        return -injectie_n, -afname_n, self.tank           # tekens opnieuw omkeren

    def simulate_plot(self, df, prijs_afname, vergoeding_injectie):
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import seaborn as sns
        '''
        instance methode om een batterij van een bepaalde langs een Fluvius kwartier-waarde dataframe te laten lopen
        en de invloed van de batterij te simuleren, plotten en een berekening te maken van gesimuleerde besparing.
        de metode verwacht de aanwezigheid van kolommon ['Injectie (Kwh)', 'Afname (Kwh)'].
        kwargs: prijs_afname, vergoeding_injectie zijn in EUR/kWh afname of injectie.
        '''
        
        results_apply = df.apply(self.simulate, axis=1, result_type='expand')
        df[['Injectie_sim', 'Afname_sim', 'Tank']] = results_apply
        print("Resultaten van de simulatie:\n")
        display(df)
        print("˅" * 70)
        print(f'>>>>>>  Huidige batterij status (na simulatie):", {self.tank:0.1f} kWh ({self.pct:.0%}) <<<<<<\n')
        print("˄" * 70)

        #Het kosten/baten plaatje:
        
        kost = prijs_afname * df['Afname (Kwh)'].sum()
        vergoeding = vergoeding_injectie * df['Injectie (Kwh)'].sum()
        netto_factuur = kost + vergoeding           # injectie is negatief gefiniëerd
        
        kost_sim = prijs_afname * df['Afname_sim'].sum()
        vergoeding_sim = vergoeding_injectie * df['Injectie_sim'].sum()
        netto_factuur_sim = kost_sim + vergoeding_sim           # injectie is negatief gefiniëerd
        
        print(
        f'\n----> Het factuurbedrag bedraagt zonder batterij: {netto_factuur:.2f} EUR, mét {self.capacity} kWh batterij: {netto_factuur_sim:.2f}EUR, een besparing van {netto_factuur - netto_factuur_sim:.2f}  EUR <----\n')


        # " ToDo: proper scaling of linewidt, makersizer by periode selected in the df
        # index_range = df.index.max() - df.index.min()
        # index_weeks = index_range.days//7
        # index_months = index_range.days//28    
        # index_years = index_range.days//365

        
        fig, (ax1,ax2, ax3) = plt.subplots(nrows = 3, figsize = (16,14))
        columns = ['Injectie (Kwh)', 'Afname (Kwh)'][::-1]
        colors=['olivedrab', 'firebrick'][::-1]
        linestyles=['-','-']
        linewidth = 0.5
        
        for idx in range(len(columns)):
            sns.lineplot(df[columns[idx]], ax=ax1,color=colors[idx], linestyle=linestyles[idx], label=columns[idx], linewidth=linewidth, legend = False)
        
        # beetje netjes maken:
        ax1.legend() 
        ax1.set_title('Originele data-  kwartierwaarden)')
        ax1.set_xlabel('Voorgaand kwartiertje')
        ax1.set_ylabel('kWh')
        ax1.set_xlim(min(df.index), max(df.index))
        
        
        # Simulated
        columns = ['Injectie_sim', 'Afname_sim'][::-1]
        colors=['olivedrab', 'firebrick'][::-1]
        linestyles=['-','-',':'] 
        
        for idx in range(len(columns)):
            sns.lineplot(df[columns[idx]], ax=ax2,color=colors[idx], linestyle=linestyles[idx], label=columns[idx], linewidth=linewidth ,legend = False)
        
        # beetje netjes maken: 
        ax2.legend() 
        ax2.set_title(f'Met batterijsimulatie, {self.capacity} kWh capacity')
        ax2.set_xlabel('Voorgaand kwartiertje')
        ax2.set_ylabel('kWh')
        ax2.set_xlim(min(df.index), max(df.index))
        
        # de batterij:
        
        columns = ['Tank']
        colors=['black']
        linestyles=['-'] 
        
        for idx in range(len(columns)):
            sns.scatterplot(df[columns[idx]], ax=ax3, color=colors[idx], label=columns[idx], marker='*', s=5, lw=0.011, legend = False)
        
        # beetje netjes maken: 
        ax3.set_title('kWh in de batterij ("in the tank")')
        ax3.set_xlabel('Voorgaand kwartiertje')
        ax3.set_ylabel('kWh')
        ax3.hlines(self.capacity, min(df.index), max(df.index), linestyles='dotted',color='magenta', alpha=0.4)
        
        
        for ax in fig.axes:
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'),) # Formatteer minor ticks als maandnummer
            ax.set_xlim(min(df.index), max(df.index))
            ax.tick_params(axis='x', rotation=-60)
        
        plt.tight_layout()
        plt.show();
