import json, sys, os, copy, shutil, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import load, el, st, remove, clone, children, link, icon, translate, set_card, find, new_id, walk
from texts_pl import *

SRC, OUT = sys.argv[1], sys.argv[2]
lib.SRC = SRC
os.makedirs(f"{OUT}/templates", exist_ok=True)

UP = "http://theme.creativemox.com/realia/wp-content/uploads/sites/29/2024/03/"
def img(id_, name):
    return {"id": id_, "url": UP + name}
HOUSES = [img(354, "modern-house-facade.jpg"), img(9, "modern-luxury-house-and-garden.jpg"), img(40, "house-luxury.jpg"),
          img(54, "street-with-new-modern-and-luxury-houses-near-green-plants-and-trees.jpg"),
          img(66, "modern-house-with-garden-swimming-pool-and-wooden-deck.jpg"), img(10, "panoramic-view-of-modern-houses.jpg"),
          img(43, "luxurious-house-with-balconies-on-boulevard-near-the-sea-with-green-spaces.jpg"),
          img(47, "real-estate-sale-and-happy-family-outside-of-new-house-excited-and-smiling-in-a-garden-property-.jpg")]

TECH_ICON = {"drewniana": "las la-tree", "Ytong": "las la-cubes"}
PROJECT_OPTIONS = [f"{p[0]} ({p[4]}, technologia {p[5]})" for p in PROJECTS]
WYCENA = "Darmowa wycena"


def project_card(doc, cid, p):
    name, sub, rooms, baths, area, tech = p
    set_card(doc, cid, name, sub,
             specs=[(rooms, "las la-bed"), (baths, "las la-bath"), (area, "las la-ruler-combined")],
             loc=f"Technologia: {tech}", loc_icon=TECH_ICON[tech], btn=WYCENA, href=L["wycena"])


def plot_card(doc, cid, p):
    name, sub, area, media, status, loc = p
    set_card(doc, cid, name, sub,
             specs=[(area, "las la-ruler-combined"), (media, "las la-plug"), (status, "las la-file-alt")],
             loc=loc, loc_icon="las la-map-marker", btn=WYCENA, href=L["wycena"])


def ready_card(doc, cid, p):
    name, sub, rooms, baths, area, loc = p
    set_card(doc, cid, name, sub,
             specs=[(rooms, "las la-bed"), (baths, "las la-bath"), (area, "las la-ruler-combined")],
             loc=loc, loc_icon="las la-map-marker", btn=WYCENA, href=L["wycena"])


def site_logo(lst, i, h, h_tab, h_mob):
    """Replace the demo logo image with Elementor Pro "Site Logo" (taken from Appearance > Customize > Site Identity)."""
    lst[i] = {"id": new_id(), "elType": "widget", "widgetType": "theme-site-logo", "isInner": False, "elements": [],
              "settings": {"align": "left", "link_to": "custom", "object-fit": "contain",
                           "height": {"unit": "px", "size": h, "sizes": []},
                           "height_tablet": {"unit": "px", "size": h_tab, "sizes": []},
                           "height_mobile": {"unit": "px", "size": h_mob, "sizes": []},
                           "__dynamic__": {"image": "[elementor-tag id=\"" + new_id() + "\" name=\"site-logo\" settings=\"%7B%7D\"]",
                                           "link": "[elementor-tag id=\"4f86500\" name=\"site-url\" settings=\"%7B%7D\"]"}}}


def card_ids(doc, grid_id):
    return [c["id"] for c in children(doc, grid_id)]


def set_meta(doc, title):
    doc["title"] = title


# ---------------------------------------------------------------- forms
def quote_form_settings(s, options, button="Wyślij mi darmową wycenę", with_extra=True):
    fields = [
        {"custom_id": "projekt", "field_type": "select", "required": "true", "field_label": "Wybierz projekt / ofertę",
         "field_options": "\n".join(options), "width": "100", "_id": new_id()},
        {"custom_id": "email", "field_type": "email", "required": "true", "field_label": "Twój e-mail",
         "placeholder": "Twój adres e-mail – na niego wyślemy ofertę", "width": "50" if with_extra else "100", "_id": new_id()},
    ]
    if with_extra:
        fields.append({"custom_id": "telefon", "field_type": "tel", "field_label": "Telefon (opcjonalnie)",
                       "placeholder": "Telefon (opcjonalnie)", "width": "50", "_id": new_id()})
    fields.append({"custom_id": "zgoda", "field_type": "acceptance", "required": "true", "field_label": "Zgoda",
                   "acceptance_text": "Wyrażam zgodę na przetwarzanie moich danych osobowych przez LubuskieDomy.pl w celu przygotowania i przesłania oferty.",
                   "width": "100", "_id": new_id()})
    s["form_fields"] = fields
    apply_quote_actions(s, button)


def apply_quote_actions(s, button):
    s.update({
        "form_name": "Darmowa wycena",
        "button_text": button,
        "submit_actions": ["email", "email2"],
        "email_to": CONTACT_EMAIL,
        "email_subject": "Nowe zapytanie o darmową wycenę: [field id=\"projekt\"]",
        "email_content": "[all-fields]",
        "email_from": CONTACT_EMAIL,
        "email_from_name": "LubuskieDomy.pl – formularz",
        "email_reply_to": "email",
        "email_content_type": "html",
        "email_to_2": "[field id=\"email\"]",
        "email_subject_2": "Twoja darmowa wycena – LubuskieDomy.pl",
        "email_content_2": OFFER_EMAIL,
        "email_from_2": CONTACT_EMAIL,
        "email_from_name_2": "LubuskieDomy.pl",
        "email_content_type_2": "html",
        "form_metadata_2": [],
        "success_message": "Dziękujemy! Oferta została wysłana na podany adres e-mail. Sprawdź skrzynkę (również folder SPAM).",
        "error_message": "Wystąpił błąd. Spróbuj ponownie lub zadzwoń: 690 295 170.",
        "server_message": "Błąd serwera. Spróbuj ponownie później.",
        "invalid_message": "Formularz zawiera błędy. Sprawdź wpisane dane.",
        "required_field_message": "To pole jest wymagane.",
    })


CONTACT_DOC = load("contact-us")


def quote_section(options, title="Darmowa wycena",
                  intro="Wybierz projekt i podaj adres e-mail – ofertę z cennikiem wyślemy automatycznie na Twoją skrzynkę."):
    sec = clone(el(CONTACT_DOC, "6a566fed"))
    sec["settings"]["_element_id"] = "darmowa-wycena"
    form_col, info_col = sec["elements"]
    h, txt, form = form_col["elements"]
    h["settings"]["title"] = title
    txt["settings"] = {"editor": f"<p>{intro}</p>"}
    quote_form_settings(form["settings"], options)
    ih1, ih2, itxt, grid = info_col["elements"]
    ih1["settings"]["title"] = "Jak to działa?"
    ih2["settings"]["title"] = "Trzy proste kroki do oferty na Twój dom."
    itxt["settings"] = {"editor": "<p>Bez zobowiązań i bez opłat. Oferta trafia na e-mail od razu po wysłaniu formularza.</p>"}
    steps = [("1. Wybierz projekt", "Wskaż projekt, działkę lub gotowy dom z naszej oferty.", "las la-home"),
             ("2. Podaj e-mail", "Wpisz adres, na który mamy wysłać ofertę.", "las la-envelope"),
             ("3. Odbierz ofertę", "Oferta z cennikiem przyjdzie automatycznie na Twoją skrzynkę.", "las la-file-invoice-dollar"),
             ("4. Porozmawiaj z doradcą", f"Chcesz indywidualną wycenę? Zadzwoń: {PHONE}.", "las la-phone")]
    for box, (t, d, ic) in zip(grid["elements"], steps):
        box["settings"]["title_text"] = t
        box["settings"]["description_text"] = d
        box["settings"]["selected_icon"] = icon(ic)
    return sec


def add_section(doc, sec, after=None):
    if after is None:
        doc["content"].append(sec)
    else:
        _, lst, i = find(doc, after)
        lst.insert(i + 1, sec)


def cta(doc, eid, title, button, href):
    st(doc, eid, title=title, button=button, link=link(href))


def flip(doc, eid, title, desc, href, ic=None):
    s = st(doc, eid, title_text_a=title, title_text_b=title, description_text_a=desc, description_text_b=desc,
           button_text="Zobacz", link=link(href), link_click="button")["settings"]
    if ic:
        s["selected_icon"] = icon(ic)


def btn(doc, eid, text, href):
    st(doc, eid, text=text, link=link(href))


def testimonials(doc, eid):
    data = [("Anna i Marek", "Zielona Góra", "Budowa domu przebiegła sprawnie i zgodnie z harmonogramem. Na każdym etapie mogliśmy liczyć na kontakt i rzetelne informacje."),
            ("Katarzyna", "Gorzów Wielkopolski", "Wybraliśmy dom drewniany i jesteśmy zachwyceni – ciepło, przytulnie i niskie rachunki. Polecamy!"),
            ("Tomasz", "Nowa Sól", "Kupiliśmy gotowy dom z działką. Wszystkie formalności załatwiła firma, my tylko odebraliśmy klucze.")]
    s = el(doc, eid)["settings"]
    for sl, (n, t, c) in zip(s["slides"], data):
        sl["name"], sl["title"], sl["content"] = n, t, c


def counters(doc, ids_vals):
    for eid, (title, num, suffix) in ids_vals.items():
        st(doc, eid, title=title, ending_number=num, suffix=suffix)


def save(doc, name):
    translate(doc["content"], T)
    with open(f"{OUT}/templates/{name}.json", "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=4)


# common section texts used on several pages
def why_us(doc, ids, text_id=None):
    data = [("Uczciwa cena", "Przejrzysty kosztorys i stała cena zapisana w umowie."),
            ("Działki w dobrych lokalizacjach", "Pomagamy znaleźć działkę pod budowę w województwie lubuskim."),
            ("Terminowo i z gwarancją", "Trzymamy się harmonogramu i udzielamy gwarancji na wykonane prace."),
            ("Doświadczona ekipa", "Własne ekipy budowlane i stały nadzór kierownika budowy.")]
    for eid, (t, d) in zip(ids, data):
        st(doc, eid, title_text=t, description_text=d)


# =================================================================== HOME
d = load("home")
set_meta(d, "Strona Główna")
st(d, "a8ef2fb", title="Budujemy domy w województwie lubuskim – od projektu po klucze")
st(d, "5a770c20", editor="<p>Domy drewniane i murowane z Ytonga, działki pod budowę oraz gotowe domy z działką. Wybierz, czego szukasz, i odbierz darmową wycenę na e-mail.</p>")
st(d, "666579fe", _element_id="darmowa-wycena")
hs = el(d, "7d0d5057")["settings"]
f0, f1, f2 = hs["form_fields"]
f0.update({"custom_id": "projekt", "field_label": "Czego szukasz?", "placeholder": "",
           "field_options": "Projekt domu\nGotowy dom z działką\nDziałka pod budowę\nBudowa na mojej działce"})
f0.pop("__dynamic__", None); f0.pop("dynamic", None); f0.pop("use_native_date", None)
f1.update({"custom_id": "technologia", "field_label": "Technologia", "placeholder": "",
           "field_options": "Dom drewniany\nDom murowany (Ytong)\nJeszcze nie wiem"})
f2.update({"custom_id": "email", "field_type": "email", "field_label": "Twój e-mail", "placeholder": "Twój e-mail"})
f2.pop("field_options", None)
apply_quote_actions(hs, WYCENA)
counters(d, {"7757606d": ("Zbudowanych domów", 150, "+"), "17a2093c": ("Projektów domów", 40, "+"),
             "1650d819": ("Zadowolonych rodzin", 150, "+"), "3c0a9301": ("Lat doświadczenia", 15, "+")})
st(d, "713d454f", editor=LOREM_LONG_ABOUT)
btn(d, "30b4b04b", "Więcej o nas", L["onas"])
for cid, p in zip(card_ids(d, "6b2bb88c"), PROJECTS):
    project_card(d, cid, p)
btn(d, "bde3dd9", "Zobacz wszystkie projekty", L["projekty"])
why_us(d, ["38f8dc01", "efe0f19", "34c204f8", "58d96703"])
st(d, "722d42fa", editor="<p>Kompleksowa oferta dla osób, które chcą zamieszkać we własnym domu bez zbędnych formalności i stresu.</p>")
flip(d, "f98ffd3", "Projekty domów", "Ponad 40 projektów domów parterowych i z poddaszem.", L["projekty"])
flip(d, "534b679d", "Działki pod budowę", "Sprawdzone działki budowlane w województwie lubuskim.", L["dzialki"], "las la-map-marked-alt")
flip(d, "5662fd61", "Gotowe domy z działką", "Domy gotowe do zamieszkania razem z działką.", L["gotowe"], "las la-key")
flip(d, "28c19dcf", "Technologia budowy", "Domy drewniane i murowane z bloczków Ytong.", L["tech"], "las la-hard-hat")
btn(d, "3f571b63", "Zamów darmową wycenę", L["wycena"])
cta(d, "740a406b", "Działki pod budowę", "Zobacz działki", L["dzialki"])
cta(d, "1d6ddc26", "Bezpłatna konsultacja z doradcą", "Zadzwoń teraz", PHONE_HREF)
cta(d, "6e0479f8", "Gotowe domy z działką", "Zobacz domy", L["gotowe"])
btn(d, "3303686b", "Poznaj technologie", L["tech"])
testimonials(d, "2b9f6380")
btn(d, "db5c217", "Wszystkie wpisy", L["blog"])
st(d, "4392d9c8", title="Od projektu, przez działkę, po klucze – wszystko w jednym miejscu")
save(d, "strona-glowna")

# =================================================================== OFERTA (services)
d = load("services")
set_meta(d, "Oferta")
st(d, "101e034b", title="Projekty domów, działki pod budowę i gotowe domy z działką")
st(d, "1fbe6204", ending_number=150, suffix="+")
st(d, "5bf4ae7d", title_text="Zbudowanych domów", description_text="Domy drewniane i murowane w całym województwie lubuskim")
st(d, "1fb07e50", title="Nasza oferta")
st(d, "6355f705", title="Wszystko, czego potrzebujesz, aby zamieszkać we własnym domu")
st(d, "baa98c1", editor="<p>Budujemy domy jednorodzinne pod klucz, sprzedajemy działki budowlane oraz gotowe domy z działką. Każdą inwestycję prowadzimy kompleksowo – od wyceny po odbiór.</p>")
s = el(d, "114b3489")["settings"]; s["icon_list"][0]["text"] = "Projekty domów"; s["icon_list"][1]["text"] = "Działki pod budowę"
s["icon_list"][0]["link"] = link(L["projekty"]); s["icon_list"][1]["link"] = link(L["dzialki"])
s = el(d, "5beb249")["settings"]; s["icon_list"][0]["text"] = "Gotowe domy z działką"; s["icon_list"][1]["text"] = "Budowa pod klucz"
s["icon_list"][0]["link"] = link(L["gotowe"]); s["icon_list"][1]["link"] = link(L["tech"])
st(d, "4cd5847d", editor="<p>Kompleksowa oferta dla osób, które chcą zamieszkać we własnym domu bez zbędnych formalności i stresu.</p>")
flip(d, "640623d", "Projekty domów", "Ponad 40 projektów domów parterowych i z poddaszem.", L["projekty"])
flip(d, "23976adb", "Działki pod budowę", "Sprawdzone działki budowlane w województwie lubuskim.", L["dzialki"], "las la-map-marked-alt")
flip(d, "52855b27", "Gotowe domy z działką", "Domy gotowe do zamieszkania razem z działką.", L["gotowe"], "las la-key")
flip(d, "492d4ff5", "Budowa pod klucz", "Budujemy w technologii drewnianej i z Ytonga.", L["tech"], "las la-hard-hat")
btn(d, "1d69d8e1", "Zamów darmową wycenę", L["projekty"] + L["wycena"])
cta(d, "46852dfb", "Działki pod budowę", "Zobacz działki", L["dzialki"])
cta(d, "3e139ad9", "Bezpłatna konsultacja z doradcą", "Zadzwoń teraz", PHONE_HREF)
cta(d, "64765267", "Gotowe domy z działką", "Zobacz domy", L["gotowe"])
why_us(d, ["23bf1476", "2b6650fb", "49d5992d", "1479ea15"])
save(d, "oferta")


# =================================================================== LISTING-based pages
def listing_page(title, hero, items, fill, options, cta_title, cta_text, cta_btn, cta_href, quote_title):
    d = load("listing")
    set_meta(d, title)
    st(d, "7c624299", title=hero)
    # search box -> not needed (no property search in WP); replace with a button to the quote form
    se, lst, i = find(d, "752ac5f6")
    b = clone(el(load("listing"), "43099632"))
    b["settings"].update({"text": "Darmowa wycena", "link": link(L["wycena"]), "align": "left"})
    lst[i] = b
    for cid, p in zip(card_ids(d, "6f9f9819"), items):
        fill(d, cid, p)
    st(d, "4dcf11f5", title=cta_title)
    st(d, "26d7c5ed", editor=f"<p>{cta_text}</p>")
    btn(d, "43099632", cta_btn, cta_href)
    why_us(d, ["74f2a4cf", "3706f7c", "4c32a90c", "15d7e5ca"])
    testimonials(d, "1b81396c")
    add_section(d, quote_section(options, quote_title), after="6cea0870")
    return d


d = listing_page("Projekty", "Projekty domów – wybierz dom dla swojej rodziny", PROJECTS, project_card, PROJECT_OPTIONS,
                 "Nie widzisz projektu dla siebie?", "Zbudujemy dom według Twojego projektu lub dopasujemy jeden z naszych projektów do Twojej działki.",
                 "Skontaktuj się z nami", L["kontakt"], "Darmowa wycena projektu")
save(d, "projekty")

d = listing_page("Działki pod budowę", "Działki pod budowę w województwie lubuskim", PLOTS, plot_card,
                 [f"{p[0]} – {p[2]} ({p[5]})" for p in PLOTS],
                 "Masz już działkę?", "Zbudujemy na niej dom w technologii drewnianej lub z Ytonga. Sprawdź nasze projekty.",
                 "Zobacz projekty domów", L["projekty"], "Darmowa wycena: działka + dom")
save(d, "dzialki-pod-budowe")

d = listing_page("Gotowe domy z działką", "Gotowe domy z działką – wprowadź się szybciej", READY, ready_card,
                 [f"{p[0]} – {p[4]}" for p in READY],
                 "Wolisz dom według własnego projektu?", "Wybierz jeden z naszych projektów i działkę – resztą zajmiemy się my.",
                 "Zobacz projekty domów", L["projekty"], "Darmowa wycena gotowego domu")
save(d, "gotowe-domy-z-dzialka")

# =================================================================== TECHNOLOGIA BUDOWY (careers)
d = load("careers")
set_meta(d, "Technologia Budowy")
st(d, "7761f8f3", title="Technologia budowy")
st(d, "4e6a7cbf", title="Budujemy w dwóch sprawdzonych technologiach: drewnianej i z Ytonga")
btn(d, "6a89fb8e", "Zamów darmową wycenę", L["projekty"] + L["wycena"])
st(d, "3844f843", title="Zalety")
st(d, "1295eeb9", title="Dlaczego warto budować z nami")
st(d, "3e3e4c3d", editor="<p>Niezależnie od wybranej technologii stosujemy certyfikowane materiały i sprawdzone rozwiązania.</p>")
benefits = [("Energooszczędność", "Dobrze ocieplone przegrody i szczelna konstrukcja to niższe rachunki za ogrzewanie."),
            ("Krótki czas budowy", "Precyzyjny harmonogram i własne ekipy pozwalają skrócić czas realizacji."),
            ("Trwałość", "Sprawdzone materiały i nadzór kierownika budowy na każdym etapie."),
            ("Zdrowy mikroklimat", "Materiały naturalne i paroprzepuszczalne zapewniają komfort mieszkania."),
            ("Stała cena", "Kosztorys przygotowany przed rozpoczęciem budowy i cena zapisana w umowie."),
            ("Gwarancja", "Udzielamy gwarancji na wykonane prace i pomagamy także po odbiorze domu.")]
icons_b = ["las la-leaf", "las la-clock", "las la-shield-alt", "las la-tree", "las la-file-invoice-dollar", "las la-award"]
for c, (t, desc), ic in zip(children(d, "49acd18f"), benefits, icons_b):
    box, b = c["elements"]
    box["settings"].update(title_text=t, description_text=desc, selected_icon=icon(ic))
    c["elements"] = [box]  # remove "Learn more" buttons
btn(d, "47a325e0", "Zobacz projekty domów", L["projekty"])
st(d, "444a6c2b", title="Nie wiesz, którą technologię wybrać?")
st(d, "6011dbf9", editor="<p>Zamów darmową wycenę – przygotujemy porównanie kosztów budowy w obu technologiach.</p>")
st(d, "39aed245", title="Nasze technologie")
st(d, "21ea9ede", editor="<p>Poznaj szczegóły każdej z technologii i wybierz rozwiązanie dla siebie.</p>")
jobs = children(d, "4b9b0af7")
for c, (t, sub, loc, ic, href) in zip(jobs[:2], [
        ("Dom drewniany", "Konstrukcja szkieletowa – szybko, ciepło i ekologicznie.", "Budowa od 4 miesięcy", "las la-tree", L["drewniana"]),
        ("Dom z Ytonga", "Technologia murowana z bloczków z betonu komórkowego.", "Trwałość na pokolenia", "las la-cubes", L["ytong"])]):
    ws = list(walk(c["elements"]))
    acc = [w for w in ws if w.get("widgetType") == "elementskit-accordion"][0]
    acc["settings"]["ekit_accordion_items"][0]["acc_title"] = t
    acc["settings"]["ekit_accordion_items"][0]["acc_content"] = f"<p>{sub}</p>"
    ib = [w for w in ws if w.get("widgetType") == "icon-box"][0]
    ib["settings"].update(title_text=loc, selected_icon=icon(ic))
    b = [w for w in ws if w.get("widgetType") == "button"][0]
    b["settings"].update(text="Zobacz szczegóły", link=link(href))
el(d, "4b9b0af7")["elements"] = jobs[:2]
save(d, "technologia-budowy")

# =================================================================== REALIZACJE (agent)
d = load("agent")
set_meta(d, "Realizacje")
st(d, "47cc2a10", title="Zobacz domy, które zbudowaliśmy dla naszych klientów")
st(d, "2988dbf7", title="Nasze realizacje")
st(d, "e736b6f", title="Każdy dom to osobna historia – i zadowolona rodzina, która w nim zamieszkała.")
st(d, "683f69c1", editor="<p>Budujemy w całym województwie lubuskim: w Zielonej Górze, Gorzowie Wielkopolskim, Nowej Soli, Świebodzinie, Żarach i okolicach.</p>")
btn(d, "6798c33c", "Zamów darmową wycenę", L["projekty"] + L["wycena"])
st(d, "35e8e6e5", image=HOUSES[0])
st(d, "38bced8a", title="Galeria realizacji")
st(d, "59e0daff", title="Domy drewniane i murowane z Ytonga")
st(d, "f1eab1a", editor="<p>Poniżej wybrane realizacje. Chcesz zobaczyć dom na żywo? Skontaktuj się z nami – umówimy wizytę.</p>")
reals = [("Dom w Zielonej Górze", "Technologia drewniana · 98 m²"), ("Dom w Sulechowie", "Ytong · 124 m²"),
         ("Dom w Nowej Soli", "Ytong · 136 m²"), ("Dom w Świebodzinie", "Technologia drewniana · 72 m²"),
         ("Dom w Gorzowie Wlkp.", "Ytong · 158 m²"), ("Dom w Żarach", "Technologia drewniana · 112 m²"),
         ("Dom w Ochli", "Technologia drewniana · 86 m²"), ("Dom w Deszcznie", "Ytong · 118 m²")]
for c, (t, desc), im in zip(children(d, "37d8414f"), reals, HOUSES):
    keep = []
    for w in c["elements"]:
        if w.get("widgetType") == "image":
            w["settings"]["image"] = dict(im)
        elif w.get("widgetType") == "icon-box":
            w["settings"].update(title_text=t, description_text=desc)
        elif w.get("widgetType") == "social-icons":
            continue
        keep.append(w)
    c["elements"] = keep
st(d, "e8a6448", title="Chcesz zamieszkać w takim domu?")
st(d, "2b24d36c", editor="<p>Zamów darmową wycenę – ofertę wyślemy od razu na Twój e-mail.</p>")
btn(d, "465dd4eb", "Darmowa wycena", L["projekty"] + L["wycena"])
save(d, "realizacje")

# =================================================================== O NAS (about-us)
d = load("about-us")
set_meta(d, "O nas")
st(d, "6d52c2c0", title="Budujemy domy w województwie lubuskim")
counters(d, {"6fd2ab9f": ("Zbudowanych domów", 150, "+"), "7317f55b": ("Projektów domów", 40, "+"),
             "2e0abf1": ("Zadowolonych rodzin", 150, "+"), "4b7cafd6": ("Lat doświadczenia", 15, "+")})
st(d, "4b79f76", editor=LOREM_LONG_ABOUT)
btn(d, "d954f32", "Zobacz realizacje", L["realizacje"])
why_us(d, ["6a33763b", "35730e3f", "3b6d37e0", "55c382bd"])
btn(d, "6d7b51fc", "Zamów darmową wycenę", L["projekty"] + L["wycena"])
cta(d, "3c7ebb51", "Działki pod budowę", "Zobacz działki", L["dzialki"])
cta(d, "1b11754d", "Bezpłatna konsultacja z doradcą", "Zadzwoń teraz", PHONE_HREF)
cta(d, "693b69bd", "Gotowe domy z działką", "Zobacz domy", L["gotowe"])
btn(d, "69a3c328", "Wszystkie projekty", L["projekty"])
# latest listing cards
cards = [x["id"] for x in walk(d["content"]) if x["elType"] == "container"
         and any(w.get("widgetType") == "slides" for w in x.get("elements", []))]
for cid, p in zip(cards, PROJECTS):
    project_card(d, cid, p)
save(d, "o-nas")

# =================================================================== KONTAKT
d = load("contact-us")
set_meta(d, "Kontakt")
st(d, "181e8282", title="Kontakt")
st(d, "14084f41", title="Porozmawiajmy o Twoim nowym domu.")
st(d, "3317f46d", title="Napisz do nas")
st(d, "50a0d177", editor="<p>Odpowiemy najszybciej, jak to możliwe.</p>")
fs = el(d, "21c45c3a")["settings"]
fs["form_fields"][3]["field_type"] = "text"  # template bug: subject was an e-mail field
fs["form_fields"][1]["field_type"] = "tel"
fs["form_fields"].append({"custom_id": "zgoda", "field_type": "acceptance", "required": "true", "field_label": "Zgoda",
                          "acceptance_text": "Wyrażam zgodę na przetwarzanie moich danych osobowych przez LubuskieDomy.pl w celu odpowiedzi na wiadomość.",
                          "width": "100", "_id": new_id()})
fs.update({"form_name": "Kontakt", "submit_actions": ["email"], "email_to": CONTACT_EMAIL,
           "email_subject": "Nowa wiadomość ze strony LubuskieDomy.pl", "email_reply_to": "email",
           "email_from": CONTACT_EMAIL, "email_from_name": "LubuskieDomy.pl – formularz"})
st(d, "22d4c82c", title="Dane kontaktowe")
st(d, "16214ea0", title="Zadzwoń lub napisz – chętnie odpowiemy na pytania o projekty, działki i technologie budowy.")
st(d, "111a0973", editor="")
st(d, "316a9455", title_text="Obszar działania", description_text="Województwo lubuskie<br>Zielona Góra, Gorzów Wlkp. i okolice")
st(d, "79aaed9a", title_text="E-mail", description_text=f"<a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>")
st(d, "3cb574f4", title_text="Telefon", description_text=f"<a href=\"{PHONE_HREF}\">{PHONE}</a>")
st(d, "1760b2da", title_text="Godziny pracy", description_text="Pon–Pt: 8:00–17:00<br>Sob–Nd: po wcześniejszym umówieniu")
st(d, "1e93e0d8", address="Zielona Góra, województwo lubuskie, Polska")
save(d, "kontakt")


# =================================================================== TECHNOLOGY DETAIL PAGES (single-property)
def tech_page(title, name, sub, desc1, adv, params, desc2, projects, other_title, img_list):
    d = load("single-property")
    set_meta(d, title)
    s = el(d, "48da40a")["settings"]
    s["icon_list"][0]["text"] = "Technologia budowy"; s["icon_list"][0]["link"] = link(L["tech"])
    s["icon_list"][1]["text"] = name
    st(d, "54765c2e", title=name)
    acc = el(d, "2e3e1398")["settings"]["ekit_accordion_items"][0]
    acc["acc_title"], acc["acc_content"] = name, f"<p>{sub}</p>"
    s = el(d, "58a88284")["settings"]
    vals = [f"Telefon: {PHONE}", "Bezpłatna konsultacja", CONTACT_EMAIL]
    for it, v in zip(s["icon_list"], vals):
        it["text"] = v
    s["icon_list"][0]["link"] = link(PHONE_HREF); s["icon_list"][2]["link"] = link("mailto:" + CONTACT_EMAIL)
    btn(d, "15e9be91", "Darmowa wycena", L["wycena"])
    st(d, "3d2a0234", title="Polecane projekty")
    # featured cards are flat widgets inside 50f88fd4: set accordion + icon list by id
    for (acc_id, il_id), p in zip([("1ca16461", "27cd0d1b"), ("e7b376f", "5cac66c8")], projects[:2]):
        a = el(d, acc_id)["settings"]["ekit_accordion_items"][0]
        a["acc_title"], a["acc_content"] = p[0], f"<p>{p[1]}</p>"
        il = el(d, il_id)["settings"]["icon_list"]
        il[0]["text"], il[1]["text"] = p[2], p[3]
        if len(il) > 2:
            il[2]["text"] = p[4]
    st(d, "7bf690b1", title="Opis technologii")
    st(d, "4eb11a71", editor=desc1)
    for eid, (t, dsc, ic) in zip(["7c4f2371", "58055b9", "782e6f16"], adv):
        st(d, eid, title_text=t, description_text=dsc, selected_icon=icon(ic))
    st(d, "6ff1d277", title="Parametry i standard wykonania")
    for il_id, chunk in (("62a5e4f5", params[:7]), ("3a9dad20", params[7:])):
        items = el(d, il_id)["settings"]["icon_list"]
        for it, txt in zip(items, chunk):
            it["text"] = txt
    st(d, "35767b78", editor=desc2)
    st(d, "27494233", title="Zbuduj z nami dom w tej technologii")
    st(d, "5af8c162", editor="<p>Wybierz projekt i odbierz darmową wycenę – ofertę wyślemy automatycznie na Twój e-mail.</p>")
    btn(d, "15a235f3", "Darmowa wycena", L["wycena"])
    st(d, "45a6ff37", title=other_title)
    btn(d, "42016a6d", "Wszystkie projekty", L["projekty"])
    for cid, p in zip(card_ids(d, "545f5d5d"), projects):
        project_card(d, cid, p)
    car = el(d, "172efa12")["settings"]
    for sl, im in zip(car.get("slides", []), img_list):
        sl["image"] = dict(im)
    add_section(d, quote_section([f"{p[0]} ({p[4]}, technologia {p[5]})" for p in projects] + ["Inny projekt / własny projekt"],
                                 f"Darmowa wycena – {name}"))
    return d


wood = [p for p in PROJECTS if p[5] == "drewniana"]
ytong = [p for p in PROJECTS if p[5] == "Ytong"]
d = tech_page("Drewniana", "Dom drewniany", "Konstrukcja szkieletowa",
              "<p>Domy w technologii drewnianej budujemy w konstrukcji szkieletowej z suszonego komorowo, struganego i certyfikowanego drewna konstrukcyjnego. "
              "Ściany wypełniamy wełną mineralną, a całość zamykamy szczelną przegrodą, dzięki czemu dom jest ciepły, energooszczędny i przyjazny dla zdrowia.</p>",
              [("Szybka budowa", "Stan surowy zamknięty nawet w kilka tygodni.", "las la-clock"),
               ("Ciepło i oszczędnie", "Bardzo dobra izolacyjność ścian i niskie koszty ogrzewania.", "las la-leaf"),
               ("Ekologia", "Drewno to naturalny, odnawialny materiał budowlany.", "las la-tree")],
              ["Konstrukcja szkieletowa", "Drewno C24 suszone komorowo", "Wełna mineralna", "Membrana paroizolacyjna",
               "Płyty OSB / gipsowo-kartonowe", "Elewacja: tynk lub deska", "Dach: blachodachówka",
               "Stan deweloperski lub pod klucz", "Okna trzyszybowe", "Pompa ciepła (opcja)", "Rekuperacja (opcja)",
               "Fotowoltaika (opcja)", "Gwarancja na konstrukcję", "Kierownik budowy"],
              "<p>Technologia drewniana pozwala znacząco skrócić czas budowy i ograniczyć tzw. „mokre” prace. To dobre rozwiązanie dla osób, które chcą szybko zamieszkać we własnym, energooszczędnym domu.</p>",
              wood, "Projekty w technologii drewnianej", [HOUSES[4], HOUSES[1], HOUSES[2], HOUSES[3], HOUSES[5]])
save(d, "technologia-drewniana")

d = tech_page("Ytong", "Dom z Ytonga", "Technologia murowana",
              "<p>Domy murowane budujemy z bloczków Ytong z betonu komórkowego. To materiał lekki, precyzyjny i ciepły, a jednocześnie bardzo trwały i odporny na ogień. "
              "Ściany murujemy na cienką spoinę, co ogranicza mostki termiczne i przyspiesza prace.</p>",
              [("Trwałość", "Solidna konstrukcja murowana na pokolenia.", "las la-shield-alt"),
               ("Bezpieczeństwo", "Beton komórkowy jest niepalny i odporny na wilgoć.", "las la-fire-extinguisher"),
               ("Dobra izolacyjność", "Ciepłe ściany i komfort termiczny przez cały rok.", "las la-thermometer-half")],
              ["Bloczki Ytong (beton komórkowy)", "Murowanie na cienką spoinę", "Ocieplenie styropianem grafitowym",
               "Strop żelbetowy (opcja)", "Tynki gipsowe", "Elewacja: tynk silikonowy", "Dach: dachówka ceramiczna",
               "Stan deweloperski lub pod klucz", "Okna trzyszybowe", "Pompa ciepła (opcja)", "Rekuperacja (opcja)",
               "Fotowoltaika (opcja)", "Gwarancja na konstrukcję", "Kierownik budowy"],
              "<p>Technologia murowana z Ytonga to wybór dla osób, które cenią sprawdzone rozwiązania, solidność i dużą akumulację ciepła ścian.</p>",
              ytong, "Projekty w technologii Ytong", [HOUSES[0], HOUSES[2], HOUSES[6], HOUSES[3], HOUSES[1]])
save(d, "technologia-ytong")

# =================================================================== HEADER
d = load("realia-header")
d["title"] = "LubuskieDomy – Nagłówek"
st(d, "51691bf0", title_text=CONTACT_EMAIL, link=link("mailto:" + CONTACT_EMAIL))
st(d, "77a83ec1", title_text=f"Tel. {PHONE}", link=link(PHONE_HREF), selected_icon=icon("las la-phone"))
logo, lst, i = find(d, "35d8c4e2")
site_logo(lst, i, 72, 60, 50)
btn(d, "2c64fc92", "Darmowa wycena", L["projekty"] + L["wycena"])
save(d, "lubuskiedomy-naglowek")

# =================================================================== FOOTER
d = load("realia-footer")
d["title"] = "LubuskieDomy – Stopka"
logo, lst, i = find(d, "6ad666af")
site_logo(lst, i, 110, 100, 90)
s = el(d, "f5e5f3e")["settings"]
for it, (t, h) in zip(s["icon_list"], [("Oferta", L["oferta"]), ("Projekty", L["projekty"]), ("Technologia budowy", L["tech"]),
                                         ("Realizacje", L["realizacje"]), ("O nas", L["onas"])]):
    it["text"], it["link"] = t, link(h)
s = el(d, "6ccef61e")["settings"]
for it, (t, h) in zip(s["icon_list"], [("Działki pod budowę", L["dzialki"]), ("Gotowe domy z działką", L["gotowe"]),
                                         ("Dom drewniany", L["drewniana"]), ("Dom z Ytonga", L["ytong"]), ("Kontakt", L["kontakt"])]):
    it["text"], it["link"] = t, link(h)
fs = el(d, "6f57e1e7")["settings"]
fs["form_fields"][0].update({"custom_id": "email", "field_type": "email", "required": "true",
                             "placeholder": "Twój e-mail – wyślemy Ci ofertę", "field_label": "E-mail"})
apply_quote_actions(fs, "Wyślij")
fs["form_name"] = "Oferta – stopka"
fs["email_content_2"] = OFFER_EMAIL.replace("Wybrana pozycja: <strong>[field id=\"projekt\"]</strong><br><br>", "")
fs["email_subject"] = "Prośba o ofertę (formularz w stopce)"
st(d, "61af7046", title_text="Województwo lubuskie")
st(d, "60ba502d", title_text=CONTACT_EMAIL, link=link("mailto:" + CONTACT_EMAIL))
st(d, "42ed737e", title_text=PHONE, link=link(PHONE_HREF))
s = el(d, "3d35db4d")["settings"]
for it, h in zip(s["icon_list"], ["/regulamin/", "/polityka-prywatnosci/", "/polityka-cookies/"]):
    it["link"] = link(h)
save(d, "lubuskiedomy-stopka")

# =================================================================== BLOG / POST / 404
d = load("realia-blog"); d["title"] = "LubuskieDomy – Blog"
s = el(d, "7069ca3d")["settings"]; s["icon_list"][0]["link"] = link(L["home"])
save(d, "lubuskiedomy-blog")
d = load("realia-single-post"); d["title"] = "LubuskieDomy – Wpis"
save(d, "lubuskiedomy-wpis")
d = load("realia-error-404"); d["title"] = "LubuskieDomy – Błąd 404"
btn(d, "7b98d5a8", "Wróć na stronę główną", L["home"])
save(d, "lubuskiedomy-404")

# =================================================================== GLOBAL STYLES
d = load("global")
d["title"] = "Style globalne – LubuskieDomy"
ps = d["page_settings"]
# palette taken from the LubuskieDomy.pl logo: blue #17539B + green #8CAD2A
SYS = {"secondary": ("Nagłówki", "#0F2440"), "primary": ("Tekst", "#3A4350"), "text": ("Biały", "#FFFFFF"), "accent": ("Przezroczysty 20%", "#FFFFFF2B")}
for c in ps["system_colors"]:
    c["title"], c["color"] = SYS[c["_id"]]
CUS = {"d49ac81": ("Przycisk (zielony z logo)", "#8CAD2A"), "332724a": ("Przycisk – hover", "#74931C"), "4d462f5": ("Linie (niebieski z logo)", "#17539B"),
       "cfa1f76": ("Jasne tło", "#E3EBF5"), "7fbea4f": ("Bardzo jasne tło", "#F2F6FA"), "044b931": ("Ciemne tło", "#0F3A6E"),
       "638d055": ("Bardzo ciemne tło", "#0A1F3A"), "a2c0d56": ("Akcent 1 – zielony", "#8CAD2A"), "ec3c7a7": ("Akcent 2 – niebieski", "#17539B"),
       "1d84241": ("Akcent 3 – granat", "#0F2440"), "262c9c6": ("Akcent 4 – niebieski", "#17539B")}
for c in ps["custom_colors"]:
    c["title"], c["color"] = CUS[c["_id"]]
TYP = {"Primary": "Główna", "Secondary": "Drugorzędna", "Text": "Tekst", "Accent": "Akcent", "Global Font": "Czcionka globalna",
       "Small Font": "Mała czcionka", "Header": "Nagłówek strony", "Footer": "Stopka", "Big Hero": "Duży nagłówek", "Button Text": "Tekst przycisku"}
for t in ps.get("system_typography", []) + ps.get("custom_typography", []):
    t["title"] = TYP.get(t["title"], t["title"])
with open(f"{OUT}/templates/global.json", "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=4)

# =================================================================== RECOLOR
# Colours hard-coded in the demo widgets (not linked to globals) -> logo palette. Alpha suffix is kept.
RECOLOR = {"77BFA3": "8CAD2A", "5E9779": "74931C", "3F6450": "17539B", "E1ECE7": "E3EBF5", "F2F6F4": "F2F6FA",
           "152D24": "0F3A6E", "080D0A": "0A1F3A", "1F2122": "0F2440", "353738": "3A4350", "FAFCFB": "FAFBFD"}
_hex = re.compile(r'"#(' + "|".join(RECOLOR) + r')([0-9A-Fa-f]{2})?"', re.I)
for fn in os.listdir(f"{OUT}/templates"):
    p = f"{OUT}/templates/{fn}"
    txt = open(p, encoding="utf-8").read()
    txt = _hex.sub(lambda mo: '"#' + RECOLOR[mo.group(1).upper()] + (mo.group(2) or "") + '"', txt)
    open(p, "w", encoding="utf-8").write(txt)

# =================================================================== MANIFEST
m = json.load(open(f"{SRC}/manifest.json", encoding="utf-8"))
old = {t["source"]: t for t in m["templates"]}
PLAN = [  # (name, new source, old source, screenshot from)
    ("Style globalne", "global", "global"),
    ("Strona Główna", "strona-glowna", "home"),
    ("Oferta", "oferta", "services"),
    ("Projekty", "projekty", "listing"),
    ("Oferta › Działki pod budowę", "dzialki-pod-budowe", "listing"),
    ("Oferta › Gotowe domy z działką", "gotowe-domy-z-dzialka", "listing"),
    ("Technologia Budowy", "technologia-budowy", "careers"),
    ("Technologia Budowy › Drewniana", "technologia-drewniana", "single-property"),
    ("Technologia Budowy › Ytong", "technologia-ytong", "single-property"),
    ("Realizacje", "realizacje", "agent"),
    ("O nas", "o-nas", "about-us"),
    ("Kontakt", "kontakt", "contact-us"),
    ("LubuskieDomy – Nagłówek", "lubuskiedomy-naglowek", "realia-header"),
    ("LubuskieDomy – Stopka", "lubuskiedomy-stopka", "realia-footer"),
    ("LubuskieDomy – Blog", "lubuskiedomy-blog", "realia-blog"),
    ("LubuskieDomy – Wpis", "lubuskiedomy-wpis", "realia-single-post"),
    ("LubuskieDomy – Błąd 404", "lubuskiedomy-404", "realia-error-404"),
]
SS_MAP = {}
new_templates = []
for name, new, src in PLAN:
    t = copy.deepcopy(old[f"templates/{src}.json"])
    t["name"] = name
    t["source"] = f"templates/{new}.json"
    t["metadata"].pop("additional_template_information", None)
    if src == "home":
        t["type"] = "page"
        t["metadata"]["template_type"] = "single-page"
    new_templates.append(t)
    SS_MAP.setdefault(f"templates/{src}.json", []).append((t["source"], name))
    # keep the template title inside the json consistent with the manifest
    p = f"{OUT}/templates/{new}.json"
    jd = json.load(open(p, encoding="utf-8"))
    jd["title"] = name
    if src == "home":
        jd["type"] = "page"
        jd["metadata"]["template_type"] = "single-page"
    json.dump(jd, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
m["templates"] = new_templates
m["title"] = "LubuskieDomy.pl – szablon Elementor (PL)"
for im in m["images"]:
    refs = []
    for r in im["templates"]:
        refs += [{"source": s, "name": n} for s, n in SS_MAP.get(r["source"], [])]
    im["templates"] = refs
m["images"] = [im for im in m["images"] if im["templates"]]
json.dump(m, open(f"{OUT}/manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
shutil.copytree(f"{SRC}/screenshots", f"{OUT}/screenshots", dirs_exist_ok=True)
print("ok")
