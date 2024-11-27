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

| Typ| Rodzaj złącza sterownika| Schemat konfiguracji|Wspierane akcje|rodzaj domyślnych ikonek|zastosowanie|Charakterystyka
|:-----:|:------:|:----------:|:-------:|:------:|:--------:|:-----:|
|


