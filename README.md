# Delay
Ninejsze repozytorium zawiera implementację konfigurowalnego gitarowego efektu typu *delay*.
Brzmienie instrumentu modyfikowane jest poprzez wielokrotne powtórzenie sygnału, przy odpowiednim tłumieniu każdego kolejnego wystąpienia.
Stworzone oprogramowanie pozwala na przetwarzanie sygnału pochodzącego z podłączonego do systemu instrumentu.
Wspierane są standardowe parametry konfiguracyjne pozwalające dostosowywać brzmienie efektu.
Projekt ten powstał w ramach realizacji przedmiotu TRA - Techniki Realizacji Algorytmów Cyfrowego Przetwarzania Sygnałów.

## Instrukcja użytkowania

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
Należy wybrać odpowiedni sterownik sprzętowy, by system działał poprawnie. QjackCtl pozwala również uruchomić serwer JACK, co pozwala potwierdzić poprawność konfiguracji. Prawidłowe działanie oprogramowania JACK może wymagać dodania użytkownika do grupy `audio`.
```bash
usermod -a -G audio $USER
```
Aby zmiana ta została wprowadzona, należy zrestartować komputer.

### Użytkowanie
Uruchomienie stworzonego programu odbywa się poprzez wykonanie skryptu `delay.py`. Jeżeli nie jest włączony serwer JACK, skrypt automatycznie go uruchomi.
```bash
python3 delay.py
```
Przedstawione wywołanie uruchamia efekt delay z domyślnymi parametrami. Listę dostępnych parametrów oraz ich domyślne wartości można zobaczyć wpisując poniższe polecenie.
```bash
python3 delay.py --help
```
Konfiguracja programu może zostać również wczytana z pliku yaml. Należy wówczas wywołać program z opcją `--file`, podając ścieżkę do pliku konfiguracyjnego. Przykładowa konfiguracja znajduje się w pliku `config.yaml`.

## Wykorzystanie

[Nagranie prezentujące działanie efektu — link](todo:youtubealbogithub)

Film znajdujący się pod powyższym linkiem zawiera prezentację działania stworzonego oprogramowania przy różnych konfiguracjach, pochodzących z zawartych w repozytorium plików konfiguracyjnych.

Ustawianie parametrów efektu może odbywać się poprzez argumenty wywołania skryptu, lub z pliku konfiguracyjnego (przy ustawieniu odpowiedniej flagi). Warto zwrócić uwagę, że wczytywanie konfiguracji z pliku całkowicie wyłącza działanie argumentów wywołania.

Przy zadawaniu konfiguracji z linii poleceń, parametry posiadają wartości domyślne, natomiast pliki konfiguracyjne muszą zawierać ustawienia wszsystkich parametrów – w innej sytuacji zgłoszony zostanie błąd.

Obsługiwane parametry efektu to:
- `time` – Czas opóźnienia efektu, wyrażony w sekundach. Oznacza czas, o jaki opóźnione jest każde kolejne wystąpienie zagranej frazy na wyjściu efektu;
- `dry` – Wzmocnienie w torze sygnału nieprzetworzonego – czyli jak głośno słyszalny jest instrument;
- `wet` – Wzmocnienie w torze sygnału przetworzonego – czyli jak głośno słyszalny jest wpływ efektu na brzmienie instrumentu. Aby nie wprowadzać ogólnego zgłaśniania lub ściszania sygnału, warto aby suma `dry` + `wet` wynosiła 1. Nie jest to jednak wymagane, a nie trzymanie się tej zasady może pozwolić artyście na otrzymanie ciekawych brzmień. 
- `feedback` – Wzmocnienie w torze pętli sprzężenia wyjścia efektu z jego wejściem. Oznacza ono część sygnału wychodzącego z bloku opóźniającego w efekcie, jaka trafia spowrotem na jego wejście. Zalecane są wartości 0≤x<1. Przy niskiej wartości parametru, słyszalne będzie jedno powtórzenie zagranego dźwięku, oraz możliwe minimalnie słyszalne drugie powtórzenie. Przy wartościach wysokich (na przykład 0.999), na wyjściu efektu pojawiają się prawie niegasnące powtórzenia, co również pozwala uzyskać ciekawe brzmienia. Przy wartościach większych niż 1 efekt staje się niestabilny, a poziom sygnału w pętli sprzężenia zwrotnego stale rośnie. Może to działać jako efekt artystyczny, ale w typowych wykorzystaniach jest raczej nieporządane.

todo: dopisać parametry filtru

Do projektu dołączone zostały pliki z gotowymi konfiguracjami prezentujące wpływ poszczególnych parametrów na brzmienie instrumentu:
- `todo.yaml` – todo.

Przedstawiony wyżej film zawiera pokaz brzmienia zawartych w tych plikach konfiguracji.

## Zakres stosowania

### Znane problemy

## Wkład autorów
Koncepcja projektu oraz sposób implementacji powstał w wyniku bezpośredniej współpracy obu autorów. Poniżej przedstawiono podział zadań podczas realizacji oprogramowania.

Wkład Tomasza Żebrowskiego:
- Integracja z systemem JACK Audio Connection Kit,
- Interfejs konsolowy oraz obsługa plików konfiguracyjnych,
- Przetwarzanie sygnału: ogólna struktura układu oraz blok opóźniający.

Wkład Przemysława Wyzińskiego:
- todo
