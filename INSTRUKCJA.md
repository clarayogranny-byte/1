# LubuskieDomy.pl – szablon strony dla WordPress + Elementor (PL)

Plik do importu: **`lubuskiedomy-elementor-kit-pl.zip`** (format Envato „Template Kit”, taki sam jak oryginalny szablon Realia).
Wszystkie strony są w pełni edytowalne w Elementorze – teksty, zdjęcia, kolory, przyciski i formularze.

## 1. Co zawiera szablon

* Wszystkie teksty po polsku, dopasowane do LubuskieDomy.pl (budowa i sprzedaż domów w województwie lubuskim).
* Struktura zgodna z dokumentem „Podstawy” (11 zakładek):

| # | Zakładka | Plik szablonu | Układ z oryginału | Zalecany adres URL |
|---|---|---|---|---|
| 1 | Strona Główna | `strona-glowna.json` | Home | `/` |
| 2 | Oferta | `oferta.json` | Services | `/oferta/` |
| 3 | Projekty | `projekty.json` | Listing | `/projekty/` |
| 4 | Działki pod budowę (w „Oferta”) | `dzialki-pod-budowe.json` | Listing | `/oferta/dzialki-pod-budowe/` |
| 5 | Gotowe domy z działką (w „Oferta”) | `gotowe-domy-z-dzialka.json` | Listing | `/oferta/gotowe-domy-z-dzialka/` |
| 6 | Technologia Budowy | `technologia-budowy.json` | Careers | `/technologia-budowy/` |
| 7 | Realizacje | `realizacje.json` | Agent | `/realizacje/` |
| 8 | O nas | `o-nas.json` | About Us | `/o-nas/` |
| 9 | Kontakt | `kontakt.json` | Contact Us | `/kontakt/` |
| 10 | Drewniana (w „Technologia Budowy”) | `technologia-drewniana.json` | Single Property | `/technologia-budowy/drewniana/` |
| 11 | Ytong (w „Technologia Budowy”) | `technologia-ytong.json` | Single Property | `/technologia-budowy/ytong/` |

Dodatkowo: nagłówek, stopka, blog, pojedynczy wpis i strona błędu 404.

* **Przycisk „Darmowa wycena”** (jak na superdom.pl) jest na **każdej karcie projektu / domu / działki**, w nagłówku i w blokach CTA.
  Kliknięcie przenosi do sekcji `#darmowa-wycena` na tej samej stronie – klient wybiera projekt i podaje swój e-mail.
  Formularz wykonuje dwie akcje: **Email** (powiadomienie dla firmy na gospodarstwo.lemanska@gmail.com) oraz **Email 2**
  (oferta **wysyłana automatycznie do klienta** na podany przez niego adres). Dodane jest pole zgody RODO.
* **Kolorystyka z logo**: niebieski `#17539B` (linie, ikony, akcenty), zielony `#8CAD2A` (przyciski), granatowe nagłówki `#0F2440`,
  ciemne tła `#0F3A6E`, jasne tła `#E3EBF5` / `#F2F6FA`. Kolory są zapisane jako **kolory globalne** – można je zmienić w jednym miejscu
  (Elementor → Ustawienia witryny → Kolory globalne). Czcionki Mulish / Inter obsługują polskie znaki.
* **Logo**: w nagłówku i stopce jest widżet **„Logo witryny”** (Elementor Pro). Pobiera on logo ustawione w WordPressie, więc wystarczy je raz wgrać (krok 2.2).
  Pliki logo są w folderze `logo/` w repozytorium:
  * `lubuskiedomy-logo.png` – logo z przezroczystym tłem (do strony),
  * `lubuskiedomy-ikona.png` – sam domek (ikona witryny / favicon),
  * `lubuskiedomy-logo-oryginal.jpg` – oryginał.
* Kontakt: tel. 690 295 170, gospodarstwo.lemanska@gmail.com.

## 2. Import do WordPressa

> **Jak pobrać plik z GitHuba:** otwórz plik `lubuskiedomy-elementor-kit-pl.zip` w repozytorium i kliknij **„Download raw file”** (ikona pobierania).
> **Nie** używaj przycisku „Code → Download ZIP” – wtedy pobierasz całe repozytorium, a plik szablonu jest schowany w środku i importer go nie rozpozna.
> Na Macu Safari potrafi automatycznie rozpakować pobrany ZIP – wgrywaj **oryginalny plik .zip** (w środku, bezpośrednio, muszą być `manifest.json`
> oraz foldery `templates` i `screenshots`, bez dodatkowego folderu nadrzędnego).
> Jeśli WordPress pokazuje błąd o rozmiarze pliku – plik ma ok. 2,5 MB, a limit wysyłania na hostingu bywa ustawiony na 2 MB; poproś hosting o zwiększenie
> `upload_max_filesize` lub użyj metody B poniżej.

### Metoda A – wtyczka „Template Kit – Import”

Wymagane wtyczki (jak w oryginale): **Elementor**, **Elementor Pro**, **ElementsKit Lite**,
**Skyboot Custom Icons for Elementor**. Zalecany motyw: **Hello Elementor**.

1. Zainstaluj wtyczkę **„Template Kit – Import”** (Envato) → *Template Kits* → *Upload Template Kit ZIP* → wybierz `lubuskiedomy-elementor-kit-pl.zip`.
2. **Logo**: *Wygląd → Dostosuj → Tożsamość witryny* → *Logo* → wgraj `lubuskiedomy-logo.png`; *Ikona witryny* → `lubuskiedomy-ikona.png`.
3. Najpierw zaimportuj **„Style globalne”**, potem wszystkie pozostałe szablony.
4. Utwórz strony (*Strony → Dodaj nową*): *Oferta* i *Technologia Budowy* jako strony nadrzędne, a *Działki pod budowę*, *Gotowe domy z działką*
   oraz *Drewniana*, *Ytong* jako ich strony podrzędne (*Atrybuty strony → Strona nadrzędna*). Adresy (slug) muszą być takie jak w tabeli powyżej –
   linki wewnątrz szablonów z nich korzystają.
5. Na każdej stronie: *Edytuj w Elementorze* → ikona folderu → *Moje szablony* → wstaw odpowiedni szablon.
   Układ strony: **Elementor – pełna szerokość**.
6. *Ustawienia → Czytanie*: „Strona Główna” jako strona główna.
7. *Szablony → Kreator motywu*: sprawdź, czy nagłówek i stopka są wyświetlane na „Całej witrynie”.
8. **Menu** (*Wygląd → Menu*, np. „Menu główne”, przypisz do widżetu menu w nagłówku):
   * Strona Główna
   * Oferta → Działki pod budowę, Gotowe domy z działką
   * Projekty
   * Technologia Budowy → Drewniana, Ytong
   * Realizacje
   * O nas
   * Kontakt

### Metoda B (zapasowa) – wbudowany import Elementora

Jeśli wtyczka „Template Kit – Import” nie chce otworzyć pliku, użyj **`lubuskiedomy-elementor-szablony-json.zip`** (same szablony, ok. 160 KB):

1. *Szablony → Zapisane szablony* (Templates → Saved Templates) → **Importuj szablony** → wybierz `lubuskiedomy-elementor-szablony-json.zip` → *Importuj teraz*.
   Wszystkie strony, nagłówek, stopka, blog i 404 pojawią się na liście szablonów.
2. Nagłówek i stopkę ustaw w *Szablony → Kreator motywu* (Theme Builder) → otwórz szablon → *Opublikuj* → warunek „Cała witryna”.
3. Kolory i czcionki globalne: zaimportowany szablon „Style globalne” otwórz w Elementorze – albo ustaw ręcznie w *Ustawienia witryny → Kolory globalne*:
   Przycisk `#8CAD2A`, Przycisk – hover `#74931C`, Linie `#17539B`, Jasne tło `#E3EBF5`, Bardzo jasne tło `#F2F6FA`, Ciemne tło `#0F3A6E`,
   Bardzo ciemne tło `#0A1F3A`, Nagłówki `#0F2440`, Tekst `#3A4350`; czcionki: nagłówki **Mulish**, tekst **Inter**.
4. Dalej postępuj jak w krokach 2 i 4–8 metody A.

Jeśli nadal pojawia się błąd – skopiuj dokładny komunikat (albo zrób zrzut ekranu), żebyśmy mogli go poprawić.

## 3. Automatyczne wysyłanie oferty – konieczna konfiguracja

1. Wgraj plik PDF z ofertą do *Mediów* i skopiuj jego adres. W formularzach (*Email 2 → Wiadomość*) zamień link
   `https://lubuskiedomy.pl/wp-content/uploads/oferta-lubuskiedomy.pdf` na właściwy. (Formularz Elementora nie dołącza plików – dlatego wysyłany jest link.)
2. Zainstaluj **WP Mail SMTP** i połącz konto Gmail gospodarstwo.lemanska@gmail.com – bez tego wiadomości „z adresu Gmail” wysyłane z serwera
   hostingu często trafiają do SPAM-u lub w ogóle nie dochodzą.
3. Przetestuj formularz, wpisując własny e-mail.

Formularze „Darmowa wycena” są na stronach: Strona Główna, Projekty, Działki, Gotowe domy, Drewniana, Ytong oraz w stopce.

## 4. Co trzeba zastąpić prawdziwymi danymi

Poniższe dane są **przykładowe** – nie zostawiaj ich na działającej stronie bez sprawdzenia:

* nazwy projektów, powierzchnie i **ceny** (projekty, działki, gotowe domy) – także na listach wyboru w formularzach;
* **opinie klientów** (Anna i Marek, Katarzyna, Tomasz) – zastąp prawdziwymi lub usuń;
* liczniki (150+ domów, 40+ projektów, 15+ lat) oraz lista realizacji;
* **zdjęcia** – wszystkie pochodzą z wersji demo szablonu (Envato); zastąp je zdjęciami firmy. To samo dotyczy filmu (link YouTube);
* adres firmy (obecnie „Województwo lubuskie”), godziny pracy, linki do mediów społecznościowych;
* strony `/regulamin/`, `/polityka-prywatnosci/`, `/polityka-cookies/` (linki w stopce).

## 5. Uwagi

* Miniatury podglądu w importerze (folder `screenshots/`) pochodzą z oryginalnego szablonu – po imporcie strony mają już kolory z logo i polskie teksty.
* Szablon został wygenerowany automatycznie skryptem `tools/build.py` z oryginalnych plików JSON. Po imporcie przejrzyj strony w edytorze Elementora
  (zwłaszcza widok mobilny), bo dłuższe polskie teksty mogą miejscami zajmować więcej miejsca niż angielskie.
