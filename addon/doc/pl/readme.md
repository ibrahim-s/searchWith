# Search With #

* Autor: Ibrahim Hamadeh
* Pobierz [wersja stabilna][1]
* Zgodność z wersjami NVDA: 2019.3 i nowszymi

Ten dodatek pomaga wyszukiwać tekst za pośrednictwem różnych
wyszukiwarek. Nie zaznaczaj tekstu i naciśnij gest dodatku, zostanie
wyświetlone okno dialogowe z polem edycji, aby wprowadzić wyszukiwane
zapytanie, wyszukać za pomocą Google nacisnąć enter lub tab, aby wyszukać za
pomocą innych engins.

A jeśli chcesz wyszukać zaznaczony tekst, wybierz tekst i naciśnij raz,
zostanie wyświetlone menu z różnymi wyszukiwarkami do wyboru. i możesz,
jeśli chcesz, naciśnij gest dwa razy, aby wyszukać wybrany tekst
bezpośrednio w Google.

Domyślnym gestem dla dodatku jest: NVDA+ Windows+ S. Jeśli naciśnięcie nie działa dla Ciebie lub powoduje konflikt z innym naciśnięciem, możesz jak zawsze dodać gest lub zmienić istniejący, przechodząc do: MENU NVDA>oferty>InputGestury>Wyszukiwanie z kategorią.

## Użycie

* Jeśli chcesz wprowadzić zapytanie wyszukiwania, po prostu naciśnij gest
  dodatku. Zostanie wyświetlone okno dialogowe z polem edycji, w którym
  można wprowadzić wyszukiwane hasło.
* Chcesz wyszukiwać w Google? wystarczy nacisnąć Enter.
* W przeciwnym razie przejdź do przycisku Inne silniki i daj mu miejsce,
  pojawi się wyskakujące menu z różnymi wyszukiwarkami do wyboru. Yahoo,
  Bing, DuckDuckGo i Youtube. Jest to menu domyślne i można je modyfikować z
  panelu ustawień dodatku.
* Innym sposobem użycia dodatku jest zaznaczenie tekstu. A po naciśnięciu
  gestu dodatku lub dowolnego innego przypisanego do niego wirtualnego menu
  zostanie wyświetlone z różnymi wyszukiwarkami, albo domyślnym menu, albo
  dowolnym innym, które dostosowałeś do swoich potrzeb.
* Wybierz jeden i naciśnij enter, domyślna przeglądarka otworzy się
  wyświetlając wyniki wyszukiwania. lub, jeśli chcesz wyszukiwać
  bezpośrednio w Google, naciśnij gest dwa razy i gotowe.
* Chcesz uruchomić menu wyszukiwania specjalnie dla schowka lub ostatniego
  tekstu mówionego? OK, wtedy możesz z okna dialogowego gestów wejściowych,
  przypisany gest dla:
    * Uruchom menu wyszukiwania dla tekstu ze schowka i naciśnij dwukrotnie,
      wyszukuje ten tekst bezpośrednio przez Google.
    * Uruchom menu wyszukiwania dla ostatniego tekstu mówionego i naciśnij
      dwukrotnie wyszukuje ten tekst bezpośrednio przez Google.
* Chcesz zmodyfikować wyszukiwanie za pomocą menu? Tak, możesz to zrobić z
  panelu ustawień i dostosować menu do swojego nastroju i potrzeb.
* Możesz stamtąd dodać do wyszukiwarki z menu, inne dostępne
  wyszukiwarki. Możesz też, jeśli chcesz, usunąć z niego element, przenieść
  element w górę, przenieść element w dół lub powrócić i ustawić menu na
  stan domyślny.
* Jeśli chcesz, aby te modyfikacje były trwałe, musisz zapisać konfigurację
  po oddziałach.
* Chcesz wyszukiwać w Google przy użyciu innych opcji językowych?
* Następnie przejdź do szukaj z kategorią w panelach ustawień, z pola cumbo
  możesz wybrać wyszukiwanie w Google:

    1. Korzystanie z ustawień i języka przeglądarki.
    2. Korzystanie z języka NVDA.
    3. Korzystanie z języka systemu Windows.

* Co więcej, masz możliwość wyboru domyślnego zapytania w oknie dialogowym
  Wyszukaj za pomocą. Z pola kombi Opcje domyślnego zapytania w panelu
  ustawień można wybrać:

    * Użyj ostatnio wymówionego elementu jako zapytania wyszukiwania
    * Użyj tekstu ze schowka
    * Użyj ostatnie wymówionego tekstu

* A jeśli wybrany zostanie schowek lub ostatni tekst mówiony, tekst w polu
  wyszukiwania zostanie wyświetlony zaznaczony, dzięki czemu można go łatwo
  zastąpić.
* Now let's choose the target language for translate engines, Google
  Translate and DeepL translator.
* Still in setting panel, under Translation engines group, there are two
  combo boxes, one for Google Translate and the other for DeepL
  Translator. Choose the target language you want for each of them and you
  are done.
* Wreszcie, szczególnie dla zaawansowanych użytkowników
* You can through a check box in setting panel, choose if you want to
  preserve your data folder upon installing a new version. And this means
  that your data will be sustained, but added to it the newly entries in the
  new version.

I to wszystko, mam nadzieję szukać dobra i znaleźć je, szczęśliwe
poszukiwania!

### Changes for 2.5.3 ###

* Add DeepL translator to available engines.
* Add two combo boxes in setting panel, to choose target language for Google
  translate and DeepL translator.

### Changes for 2.3 ###

* Now choosing to preserve data from setting panel, does not means that you
  will not get the new data entries, but the new entries in the new version,
  will be merged and added to your old data file.
* Update last tested version to 2023.1 to comply with NVDA version 2023.1.

### Zmiany dla wersji 2.0 ###

* Wyłącz dodatek w trybie bezpiecznym.
* Zaktualizuj ostatnio testowaną wersję do 2022.1, aby zachować zgodność z
  najnowszą wersją interfejsu API dodatku.

### Zmiany w wersji 1.8 ###

* Dodaj pole wyboru w panelu ustawień, aby umożliwić zaawansowanym
  użytkownikom zachowanie folderu danych.
* Dodaj dwa nowe wpisy w gestach wprowadzania:
    * uruchom menu wyszukiwania tekstu ze schowka, naciśnij dwukrotnie
      wyszukuje bezpośrednio w Google.
    * Uruchom menu wyszukiwania dla ostatniego tekstu mówionego, naciśnij
      dwa razy wyszukuje bezpośrednio w Google.

### Zmiany w wersji 1.7

* Utwórz pole kombi w ustawieniach dodatku, aby wybrać opcję domyślnego
  zapytania w wyszukiwaniu z dialogiem.
* Możesz wybrać opcję Pozostaw puste, Użyj tekstu ze schowka lub Użyj
  ostatnio mówionego tekstu.

### Zmiany dla wersji 1.2

* Dodaj więcej witryn, które można dodać do menu, takich jak Stackoverflow,
  Stackexchange, GoogleBooks i inne.
* Dodaj opcje używania ostatniego tekstu mówionego jako domyślnego zapytania
  w wyszukiwaniu z oknem dialogowym.

### Zmiany w wersji 0.4

* Dodaj okno dialogowe, jeśli nie zaznaczono tekstu, aby wprowadzić
  wyszukiwane hasło.
* Umożliwia modyfikację wyszukiwania za pomocą menu z panelu ustawień, aby
  dopasować je do potrzeb użytkownika.

### Zmiany w wersji 0.3

* Dodaj panel ustawień, dając więcej opcji językowych w wyszukiwarce Google.

### Zmiany w wersji 0.1

* Pierwsza wersja.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=searchwith
