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
  Pliki logo są w folderze `logo/` oraz w archiwum ZIP:
  * `lubuskiedomy-logo.png` – logo z przezroczystym tłem (do strony),
  * `lubuskiedomy-ikona.png` – sam domek (ikona witryny / favicon),
  * `lubuskiedomy-logo-oryginal.jpg` – oryginał.
* Kontakt: tel. 690 295 170, gospodarstwo.lemanska@gmail.com.

## 2. Import do WordPressa

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
