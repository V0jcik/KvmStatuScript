import mariadb
import os
import dotenv

import requests
import logging
import datetime

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

logging.basicConfig(filename=os.getenv('LOG_PATH') + "script.log", format= '%(message)s') 

logger=logging.getLogger()
logger.setLevel(logging.INFO)

#testy URL utworzonych na podstawie zawartości tabeli w bazie danych.

def url_check(url):
    try:
        get = requests.get(url)
        if get.status_code == 200:
            return(1) # adres url odpowiada prawidłowo
        else:
            return(0) # adres url stał się niedostępny
            
    except requests.exceptions.RequestException as e:
        return(0)

def actual_time():
    try:
        currentDate = datetime.datetime.now()
        today = currentDate.strftime("%Y-%m-%d %H:%M:%S")
        return(today)
    except ValueError as e:
        return(0)
    
    # Logowanie aktualnej daty do pliku script.log
def log_time():
    time = datetime.datetime.now().strftime("%Y.%m.%d %H:%M")
    logging.info(f'---------[ {time} ]---------')

DBstates = []

try:
    # Połączenie z bazą danych używające danych pobranych z pliku .env
    conn = mariadb.connect(
        user= os.getenv('USER'), 
        password= os.getenv('PASSWORD'),
        host= os.getenv('HOST'), 
        port= int(os.getenv('PORT')),
        database= os.getenv('DATABASE')) 

    # Utworzenie cursora, by móc poruszać się po bazie danych
    cur = conn.cursor()   

    cur.execute(os.getenv('DBSTATES'))
    
    # Pobranie rekordów z bazy danych i dopisanie ich do listy
    records = cur.fetchall()
    for row in records:
        DBstates.append(str(row)[1:-2])
    
    i = 0
    # Lista na wszystkie zmiany, które zaszły podczas wywołania skryptu np:
        # ---------[ 2023.09.19 04:18 ]---------
        #   Console 4  has been DISCONNECTED
        #   Console 7  has been DISCONNECTED
    log_changes = []
    
    for state in DBstates:
        getState = str(url_check(os.getenv('URL') % str(i+1)))
        
        if DBstates[i] != getState: 
            cur.execute(os.getenv('STATE') % (getState, str(i+1)))
            
            #fragment kodu, opisany w linijce 102
            # if int(os.getenv('TIMELOOP')) == (n):

            # wyrównanie odstępu w pliku script.log
            # ---------[ 2023.09.20 12:09 ]---------
            #     Console 9  has been CONNECTED
            #              ^
            # ---------[ 2023.09.20 12:19 ]---------
            #     Console 11 has been CONNECTED
            space = ''
            if len(str(i+1)) == 1 : space = ' '

            if getState == '1':
                startValue = str(actual_time())
                # Zapis informacji kiedy konsola została podłączona
                cur.execute(os.getenv('STARTED') % (startValue, str(i+1)))
                log_changes.append(f'    Console {i+1}{space} has been CONNECTED')
            
            if getState == '0':
                # Reset czasu (do wartości NULL) podłączenia jeśli konsola została odłączona
                cur.execute(os.getenv('NULL') % str(i+1))
                log_changes.append(f'    Console {i+1}{space} has been DISCONNECTED')
  
        i = i+1
    
    # Zapis stanu do bazy co drugie wykonanie skryptu {testowy kawałek kodu, posiada minusy}

    # dotenv.set_key(dotenv_file, 'TIMELOOP', str(int(os.environ['TIMELOOP'])+1))
    # if int(os.getenv('TIMELOOP')) > (n-1):
    #     dotenv.set_key(dotenv_file, 'TIMELOOP', '0')

    # Jeśli zaszły jakieś zmiany podczas wykonania skryptu -> zapisz zmiany w formie loga
    if len(log_changes) != 0: 
        log_time()
        for e in log_changes:
            logging.info(e)

    conn.commit()

    # Logowanie błędów bazy danych [nie widoczne w pliku z racji ustawienia poziomu logowania na INFO]
except mariadb.Error as e:
    log_time()
    logging.info("Error with MariaDB", e)
    
finally:
    conn.close()
    cur.close()
    print("MariaDB connection is closed")