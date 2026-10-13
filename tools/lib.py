import json, copy, random, re

SRC = None  # set by build.py
USED_IDS = set()
random.seed(20261013)


def load(name):
    with open(f"{SRC}/templates/{name}.json", encoding="utf-8") as f:
        d = json.load(f)
    for e in walk(d["content"]):
        USED_IDS.add(e["id"])
    return d


def walk(els):
    for e in els:
        yield e
        yield from walk(e.get("elements", []))


def new_id(n=7):
    while True:
        i = "%0*x" % (n, random.getrandbits(4 * n))
        if i not in USED_IDS:
            USED_IDS.add(i)
            return i


def find(doc, eid):
    def rec(lst):
        for i, e in enumerate(lst):
            if e["id"] == eid:
                return e, lst, i
            r = rec(e.get("elements", []))
            if r:
                return r
    r = rec(doc["content"] if isinstance(doc, dict) and "content" in doc else doc)
    if not r:
        raise KeyError(eid)
    return r


def el(doc, eid):
    return find(doc, eid)[0]


def st(doc, eid, **kw):
    e = el(doc, eid)
    if not isinstance(e["settings"], dict):
        e["settings"] = {}
    e["settings"].update(kw)
    return e


def remove(doc, *eids):
    for eid in eids:
        _, lst, i = find(doc, eid)
        del lst[i]


def clone(e):
    c = copy.deepcopy(e)
    for x in walk([c]):
        x["id"] = new_id()
        s = x.get("settings")
        if isinstance(s, dict):
            for v in s.values():
                if isinstance(v, list):
                    for it in v:
                        if isinstance(it, dict) and "_id" in it:
                            it["_id"] = new_id()
    return c


def children(doc, eid):
    return el(doc, eid).get("elements", [])


def link(url, external=False):
    return {"url": url, "is_external": "on" if external else "", "nofollow": "", "custom_attributes": ""}


def icon(cls, lib="skb_cife-lineawesome-icon"):
    return {"value": " " + cls if lib.startswith("skb") else cls, "library": lib}


def translate(obj, T):
    """Replace every string value that exactly matches a key of T (also stripped)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                if v in T:
                    obj[k] = T[v]
                elif v.strip() in T and v.strip():
                    obj[k] = T[v.strip()]
            else:
                translate(v, T)
    elif isinstance(obj, list):
        for x in obj:
            translate(x, T)


def widgets_in(container):
    return [x for x in walk(container.get("elements", [])) if x["elType"] == "widget"]


def set_card(doc, cid, title, sub, specs=None, loc=None, loc_icon=None, btn=None, href=None, images=None):
    """Fill a property-card container: accordion (title + subtitle), icon list,
    icon box (location), button, slides (images)."""
    c = el(doc, cid)
    for w in widgets_in(c):
        s = w["settings"]
        t = w["widgetType"]
        if t == "elementskit-accordion":
            s["ekit_accordion_items"][0]["acc_title"] = title
            s["ekit_accordion_items"][0]["acc_content"] = f"<p>{sub}</p>"
        elif t == "icon-list" and specs is not None:
            items = s["icon_list"]
            base = items[0]
            new = []
            for i, (txt, ic) in enumerate(specs):
                it = copy.deepcopy(items[i] if i < len(items) else base)
                it["text"] = txt
                it["selected_icon"] = icon(ic)
                if i >= len(items):
                    it["_id"] = new_id()
                new.append(it)
            s["icon_list"] = new
        elif t == "icon-box" and loc is not None:
            s["title_text"] = loc
            if loc_icon:
                s["selected_icon"] = icon(loc_icon)
        elif t == "button" and btn is not None:
            s["text"] = btn
            s["link"] = link(href)
        elif t == "slides" and images:
            for sl, img in zip(s["slides"], images):
                sl["background_image"] = dict(img)


def all_strings(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                yield path + "." + k, k, v
            else:
                yield from all_strings(v, path + "." + k)
    elif isinstance(obj, list):
        for i, x in enumerate(obj):
            yield from all_strings(x, f"{path}[{i}]")
