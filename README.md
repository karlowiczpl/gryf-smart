# Integracja GRYF_SMART z Home assistant

## 1. Ważne informacje dotyczące integracji

### 1.1 Komunikacja

#### Konwerter RS-232/USB lub fizyczny RS-232

- Dodanie do konfiguracji - w parametrze "port" podajemy ścieżkę do fizycznego portu dla Konwertera będzie to standardowo "/dev/ttyUSB0", a dla fizycznego RS-232 "/dev/ttyS0"
  ```yaml
  gryf_smart:
      port: "/dev/ttyS0"    #lokalizacja portu RS-232
  ```

#### Sterownik DUINO MEGA 2560

- Dodanie do konfiguracji - w parametrze "ip" podajemy adres ip sterownika
  ```yaml
  gryf_smart:
      ip: 192.168.0.95    #ip sterownika
  ```

### 1.2 Aktualizacja stanów

#### Aktualizacja po uruchomieniu

- Serwer Po każdym uruchomieniu odpyta sterowniki o stany
- Wymaga do pracy parametru "id" w którym jest zawarta ilość sterowników

```yaml
gryf_smart:
    id: 9    #ilość sterowników
```

#### Asynchroniczna aktualizacja stanów

- Domyślnie włączona
- Cyklicznie odpytuje sterowniki o stany wejść i wyjść
- wymaga parametru "id"

```yaml
gryf_smart:
    states_update: False    #wyłaczenie asynchronicznej aktualizacji stanów
```

### 1.3 Encja Resetująca

- Domyślna nazwa to switch.gryf_rst
- Zalecane resety raz dziennie
- Po resecie automatycznie przywróci stany sterowników

### 1.4 Encje wychodzących i wchodzących komend

#### Encja: sensor.gryf_in

- Pokazuje aktualnie przychodzące komendy oraz zapisuje historię

#### Encja: sensor.gryf_out

- Pokazuje aktualnie wychodzące komendy oraz zapisuje historię

## 2. Wszystkie typy i ich parametry

### 2.1 Encje sterujące - wspierają akcje
|  Typ  | Rodzaj złącza sterownika | Schemat konfiguracji |        Wspierane akcje        | rodzaj domyślnych ikonek |               zastosowanie                |       Typ encji        |
| :----: | :------------------------: | :------------------: |:-----------------------------:|:------------------------:|:-----------------------------------------:|:----------------------:|
| Lights |  wyjście przekaźnikowe  |      Klasyczny      | turn_on<br>turn_off<br>toggle |         Żarówka          |            lampy i oświetlenie            |         switch         |
| lock| wyjście przekaźnikowe| klasyczny| turn_on<br> turn_off<br>toggle|          Kłudka|                zamek drzwi                |    switch    |
 | pwm | wyjścia tranzystorowe (pwm) | klasyczny| set_value | Żarówka|                listwy LED                 |    number    |
|gate | wyjścia przekaźnikowe| klasyczny| turn_on| Brama|              otwieanie bram               | switch|
|covers| wyjścia roletowe| roletowy| turn_on<br>turn_off<br>toggle| Rolety|sterowanie <br>roletami nie <br>na procent | cover|
|p_covers| wyjścia roletowy| roletowy| turn_on<br>turn_off<br>toggle<br>set_cover_position| Rolety|               sterowanie roletami <br>na konkretny<br>procent|cover|
|climate|wyjście przekaźnikowe,<br>wejście temperaturowe| regulator|turn_on<br>turn_off<br>toggle<br>set_temperatur| Regularoe| prosty regularoe<br>dwustawny| climate

### 2.2 Encje typu sensor 
- nie wspierają żadnych akcji tylko zbierają dane
- wszystkie posiadają klasyczny schemat konfiguracji

|  Typ  | Rodzaj złącza sterownika  |rodzaj domyślnych ikonek |      zastosowanie      |       Typ encji        |
| :----: | :------------------------: |:-----------------------:|:----------------------:|:----------------------:|
 | butttons | wejścia |       Przycisk         |   klasyczne wejścia    |  sensor |
| doors | wejścia|         drzwi          | kontraktron w drzwiach | binary sensor|
| windows | wejścia|           okna          |  kontraktron w oknach  | binary sensor|
| temperature | wejścia temperaturowe | temperatura | pomiar temperatury | sensor |

## 3. Schematy konfiguracji - schamaty dla każdego typu są określone w tabelce

### 3.1 Klasyczny

```yaml
gryf_smart:   
    lights: 
        -   name: Przykładowa lampa   //Przykładowa nazwa lampy, dopuszcza liczby spacje i duże litery, bez znaków specjalnych
            pin: 1    //Numer wyjścia/wejścia sterownika
            id: 1   //Numer ID sterownika
```
### 3.2 Roletowy

```yaml
gryf_smart:   
    p_cover: 
        -   name: Przykładowa lampa   //Przykładowa nazwa lampy, dopuszcza liczby spacje i duże litery, bez znaków specjalnych
            pin: 1    //Numer wyjścia/wejścia sterownika
            id: 1   //Numer ID sterownika
            time: 100   //Czas pełnego otwarcia *10ms
```
### 3.3 Regulator

```yaml
gryf_smart:   
    p_cover: 
        -   name: Przykładowa lampa   //Przykładowa nazwa lampy, dopuszcza liczby spacje i duże litery, bez znaków specjalnych
            t_pin: 1    //Numer wejścia temperaturowgo
            t_id: 1   //Numer ID sterownika wejścia temperaturowego
            p_pin: 1    //Numer wyjścia przekaźnikowego
            p_id: 1   //Numer ID sterownika wyjścia przekażnikowego
```




