class ExamException(Exception):
    pass



class CSVTimeSeriesFile:

    def __init__(self, name):
        self.name = name
    
    def get_data(self):
        #Controllo che il file sia leggibile, o anche solo presente
        try:
            lista = open(self.name,'r')
        except:
            raise ExamException('Errore: Non possibile leggere il file richiesto.')

        lista = lista.readlines()
        if(len(lista) == 0):
            raise ExamException ('Errore: Lista dei valori vuota.')
        
        valori = []
        for linea in range(len(lista)):

            #Nel caso in cui siano presenti degli errori all'interno del try si passa automanticamente alla prossima riga senza eseguire nessun altro comando
            try:
                #Divisione del blocco in 2 elementi divisi dalla virgola
                elemento = lista[linea].split(',')
                if (elemento[0]!="epoch" or elemento[1]!="temperature"):
                    if(len(elemento)==2):   #Controllo che non vengano inserite delle virgole di troppo
                        data = float(elemento[0])   #Nel caso in cui il valore contenga decimali non e' possibile convertire da str a int direttamente 
                        temperatura = elemento[1]
                        valori.append([int(data),float(temperatura)])
            except: 
                pass

        return valori



def daily_stats(time_series):
    valori = []
    min = time_series[0][1]
    max = min
    media = 0
    n_stats = 0    #Utilizzato per tenere il conto di quanti dati si possiedono per ogni singolo giorno (serve per ottenere la media)
    curr_day = time_series[0][0]-(time_series[0][0]%86400)    #Per controllare se i valori appartengono ad un giorno differente o meno
    
    for i in range(len(time_series)):
        if(i>0):   #Per i=0 non ci sarebbe un valore precedente
            if(time_series[i][0] <= time_series[i-1][0]):   #Controllo che le data sia maggiore alla precedente
                raise ExamException('Errore: Ordine di data dei valori non accettabile.')
        
        stat_day = time_series[i][0]-(time_series[i][0]%86400)
        
        if(stat_day == curr_day):   #Azioni nel caso in caso di stessa data
            n_stats += 1
            media += time_series[i][1]
            if(time_series[i][1]<min):
                min = time_series[i][1]
            
            if(time_series[i][1]>max):
                max = time_series[i][1]
        
        else:   #In caso di data diversa dalla precedente
            media = media/n_stats
            valori.append([float(min),float(max),float(media)])
            n_stats = 1
            min = time_series[i][1]
            max = time_series[i][1]
            media = time_series[i][1]
            curr_day = stat_day    #Cambio di data
        
    media = media/n_stats
    valori.append([float(min),float(max),float(media)])   #Finito il ciclo for bisogna effettuare l'inserimento degli ultimi valori
    return valori


        
        
time_series_file = CSVTimeSeriesFile('data.csv')
time_series = time_series_file.get_data()
print(time_series)



daily_stats_series = daily_stats(time_series)

for i in range(len(daily_stats_series)):
    print(daily_stats_series[i])
    