# LubuskieDomy.pl – Elementor šablonas (PL)

Failas importui: **`lubuskiedomy-elementor-kit-pl.zip`** (Envato „Template Kit“ formatas, kaip ir originalas).

## 1. Kas pakeista

* Visi tekstai išversti į lenkų kalbą ir pritaikyti LubuskieDomy.pl (namų statyba ir pardavimas Liubušo vaivadijoje).
* Struktūra pagal dokumentą „Podstawy“ (11 puslapių):

| # | Puslapis (PL) | Šablono failas | Pagrindas iš originalo | Rekomenduojamas URL |
|---|---|---|---|---|
| 1 | Strona Główna | `strona-glowna.json` | Home | `/` |
| 2 | Oferta | `oferta.json` | Services | `/oferta/` |
| 3 | Projekty | `projekty.json` | Listing | `/projekty/` |
| 4 | Działki pod budowę (po „Oferta“) | `dzialki-pod-budowe.json` | Listing | `/oferta/dzialki-pod-budowe/` |
| 5 | Gotowe domy z działką (po „Oferta“) | `gotowe-domy-z-dzialka.json` | Listing | `/oferta/gotowe-domy-z-dzialka/` |
| 6 | Technologia Budowy | `technologia-budowy.json` | Careers | `/technologia-budowy/` |
| 7 | Realizacje | `realizacje.json` | Agent | `/realizacje/` |
| 8 | O nas | `o-nas.json` | About Us | `/o-nas/` |
| 9 | Kontakt | `kontakt.json` | Contact Us | `/kontakt/` |
| 10 | Drewniana (po „Technologia Budowy“) | `technologia-drewniana.json` | Single Property | `/technologia-budowy/drewniana/` |
| 11 | Ytong (po „Technologia Budowy“) | `technologia-ytong.json` | Single Property | `/technologia-budowy/ytong/` |

Be to: antraštė (header), poraštė (footer), blogas, įrašas ir 404 – išversti. FAQ šablonas pašalintas (reikalavimuose jo nėra).

* **Mygtukas „Darmowa wycena“** (kaip superdom.pl) yra ant **kiekvienos projekto / namo / sklypo kortelės**, antraštėje ir CTA blokuose.
  Paspaudus nuvedama į sekciją `#darmowa-wycena` tame pačiame puslapyje. Ten klientas pasirenka projektą ir įveda el. paštą.
  Formos veiksmai: **Email** (pranešimas įmonei į gospodarstwo.lemanska@gmail.com) + **Email 2** (pasiūlymas
  **automatiškai išsiunčiamas klientui** į jo nurodytą el. paštą). Pridėtas RODO sutikimo laukelis.
* Spalvos (klientas paliko pasirinkti mums): tamsiai žalia (miškai, Liubušo regionas) + medžio / vario akcentas
  mygtukams. Pagrindinis mygtukas `#B5651D`, tamsus fonas `#1F3A2E`, šviesus fonas `#ECE5D8`.
  Šriftai (Mulish / Inter) palaiko lenkiškas raides.
* Logotipas „Realia“ pakeistas tekstiniu logotipu „Lubuskie**Domy**.pl“ (galima vėliau pakeisti paveikslėliu).
* Kontaktai: tel. 690 295 170, gospodarstwo.lemanska@gmail.com.

## 2. Importas į WordPress

Reikalingi įskiepiai (kaip originale): **Elementor**, **Elementor Pro**, **ElementsKit Lite**,
**Skyboot Custom Icons for Elementor**.

1. Įdiekite įskiepį **„Template Kit – Import“** (Envato) → *Template Kits* → *Upload Template Kit ZIP* → pasirinkite `lubuskiedomy-elementor-kit-pl.zip`.
2. Pirmiausia importuokite **„Style globalne“**, tada visus kitus šablonus.
3. Sukurkite puslapius (Pages): *Oferta* ir *Technologia Budowy* kaip tėvinius, o *Działki pod budowę*, *Gotowe domy z działką*
   bei *Drewniana*, *Ytong* – kaip jų vaikinius puslapius (Page Attributes → Parent). Slug'ai turi atitikti lentelėje nurodytus URL
   (vidinės nuorodos šablonuose naudoja būtent juos).
4. Kiekviename puslapyje: *Edit with Elementor* → aplankas → *My Templates* → įterpkite atitinkamą šabloną.
   Page Layout: **Elementor Full Width**.
5. *Settings → Reading*: „Strona Główna“ kaip pradinis puslapis.
6. *Templates → Theme Builder*: patikrinkite, kad antraštė ir poraštė rodomos „Entire Site“.
7. **Meniu** (*Appearance → Menus*, pavadinimas pvz. „Menu główne“, priskirti antraštės Nav Menu valdikliui):
   * Strona Główna
   * Oferta → Działki pod budowę, Gotowe domy z działką
   * Projekty
   * Technologia Budowy → Drewniana, Ytong
   * Realizacje
   * O nas
   * Kontakt

## 3. Automatinis pasiūlymo siuntimas – būtina sukonfigūruoti

1. Įkelkite pasiūlymo PDF į *Media* ir nukopijuokite jo adresą. Formose (*Email 2 → Message*) pakeiskite nuorodą
   `https://lubuskiedomy.pl/wp-content/uploads/oferta-lubuskiedomy.pdf` į tikrąją. (Elementor forma negali prisegti failo – todėl siunčiama nuoroda.)
2. Įdiekite **WP Mail SMTP** ir prijunkite Gmail paskyrą gospodarstwo.lemanska@gmail.com – kitaip laiškai
   „nuo Gmail adreso“ iš hostingo serverio dažnai patenka į SPAM arba nepristatomi.
3. Išbandykite formą su savo el. paštu.

Formos su „Darmowa wycena“ yra: Strona Główna (hero), Projekty, Działki, Gotowe domy, Drewniana, Ytong ir poraštėje.

## 4. Ką būtina pakeisti tikrais duomenimis

Šie duomenys yra **pavyzdiniai** (užpildymui), jų nepalikite gyvoje svetainėje be patikrinimo:

* projektų pavadinimai, plotai ir **kainos** (projektai, sklypai, paruošti namai) – tame tarpe ir formų pasirinkimų sąrašuose;
* **atsiliepimai** (Anna i Marek, Katarzyna, Tomasz) – pakeiskite tikrais klientų atsiliepimais arba pašalinkite;
* skaitikliai (150+ namų, 40+ projektų, 15+ metų) ir realizacijų sąrašas;
* **nuotraukos** – visos yra iš demo (Envato), pakeiskite tikromis įmonės nuotraukomis; vaizdo įrašas (YouTube nuoroda) – taip pat;
* įmonės adresas (dabar „województwo lubuskie“), darbo valandos, socialinių tinklų nuorodos;
* puslapiai `/regulamin/`, `/polityka-prywatnosci/`, `/polityka-cookies/` (nuorodos poraštėje).

## 5. Pastaba

Šablonas sugeneruotas automatiškai iš originalių JSON failų; peržiūrą darykite Elementor redaktoriuje
(ypač mobilų vaizdą), nes ilgesni lenkiški tekstai kai kur gali užimti daugiau vietos nei angliški.
