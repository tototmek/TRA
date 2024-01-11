# Delay
Niniejszy projekt powstał w ramach realizacji przedmiotu TRA - Techniki Realizacji Algorytmów Cyfrowego Przetwarzania Sygnałów.

### Wymagania
Wymagane zależności zainstalować można z wykorzystując podane polecenia:
```bash
sudo apt-get update
sudo apt-get -y install jackd python3 python3-pip
pip install setuptools numpy JACK-Client
```
Stworzone oprogramowanie wykorzystuje [JACK Audio Connection Toolkit](https://jackaudio.org/) do interfejsowania się ze sterownikami audio działającymi w systemie. Konieczne jest odpowiednie skonfigurowanie tego narzędzia, do czego wykorzystać można na przykład program QjackCtl.
```bash
sudo apt-get -y install qjackctl
qjackctl
```
Należy wybrać odpowiedni sterownik sprzętowy, by system działał poprawnie. QjackCtl pozwala również uruchomić serwer JACK, co pozwala potwierdzić poprawność konfiguracji.

### Użytkowanie
Uruchomienie stworzonego programu odbywa się poprzez wykonanie skryptu `delay.py`. Jeżeli nie jest włączony serwer JACK, skrypt automatycznie go uruchomi.
```bash
python3 delay.py
```
Przedstawione wywołanie uruchamia efekt delay z domyślnymi parametrami. Listę dostępnych parametrów oraz ich domyślne wartości można zobaczyć wpisując poniższe polecenie.
```bash
python3 delay.py --help
```
