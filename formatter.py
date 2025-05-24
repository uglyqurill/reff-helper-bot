from datetime import datetime


def format_authors(authors: list) -> str:
    """
    Форматирует список авторов по ГОСТ Р 7.0.5–2008: 'Фамилия И.О., Фамилия И.О. [и др.]'
    Принимает список словарей с полями family и given.
    """
    formatted = []
    for a in authors[:3]:
        fam = a.get("family", "")
        initials = "".join(part[0].upper() + "." for part in a.get("given", "").split() if part)
        formatted.append(f"{fam} {initials}")
    if len(authors) > 3:
        formatted[-1] += " [и др.]"
    # Разделяем авторов запятой
    return ", ".join(formatted)


def format_book(meta: dict) -> str:
    """
    Форматирование книги по ГОСТ Р 7.0.5–2008.
    """
    authors = format_authors(meta.get("author", []))
    title = meta.get("title", [""])[0]
    subtitle = meta.get("subtitle", "")
    place = meta.get("publisher-location", "")
    publisher = meta.get("publisher", "")
    year = meta.get("issued", {}).get("date-parts", [[None]])[0][0]
    pages = meta.get("page", "")
    isbn = meta.get("ISBN", [""])[0]

    parts = []
    if authors:
        parts.append(f"{authors}.")
    if subtitle:
        parts.append(f"{title} : {subtitle}.")
    else:
        parts.append(f"{title}.")
    parts.append(f"{place} : {publisher}, {year}.")
    if pages:
        parts.append(f"{pages} с.")
    if isbn:
        parts.append(f"ISBN {isbn}.")
    return " ".join(parts)


def format_article(meta: dict) -> str:
    """
    Форматирование статьи из журнала по ГОСТ.
    """
    authors = format_authors(meta.get("author", []))
    title = meta.get("title", [""])[0]
    journal = meta.get("container-title", [""])[0]
    year = meta.get("issued", {}).get("date-parts", [[None]])[0][0]
    volume = meta.get("volume", "")
    issue = meta.get("issue", "")
    pages = meta.get("page", "")
    url = meta.get("URL", "")

    # Замена дефиса на длинное тире в номере страниц
    pages = pages.replace("-", "–")

    parts = []
    if authors:
        parts.append(f"{authors}.")
    parts.append(f"{title} // {journal}.")
    parts.append(f"– {year}.")
    if volume:
        vol_part = f"Т. {volume}"
        if issue:
            vol_part += f", № {issue}"
        parts.append(f"– {vol_part}.")
    elif issue:
        parts.append(f"– № {issue}.")
    if pages:
        parts.append(f"– С. {pages}.")
    if url:
        parts.append(f"– DOI: {url}")
    return " ".join(parts)


def format_electronic(meta: dict) -> str:
    """
    Форматирование электронного ресурса по ГОСТ.
    """
    authors = format_authors(meta.get("author", []))
    title = meta.get("title", [""])[0]
    url = meta.get("URL", "")
    access_date = datetime.now().strftime("%d.%m.%Y")

    parts = []
    if authors:
        parts.append(f"{authors}.")
    parts.append(f"{title} [Электронный ресурс].")
    if url:
        parts.append(f"URL: {url} (дата обращения: {access_date}).")
    return " ".join(parts)


def format_chapter(meta: dict) -> str:
    """
    Форматирование главы сборника или книги по ГОСТ.
    """
    authors = format_authors(meta.get("author", []))
    chapter_title = meta.get("title", [""])[0]
    book_title = meta.get("container-title", [""])[0]
    editors = meta.get("editor", [])
    ed_strs = []
    for ed in editors:
        fam = ed.get("family", "")
        initials = "".join(part[0].upper() + "." for part in ed.get("given", "").split() if part)
        ed_strs.append(f"{initials} {fam}")
    ed_part = ""
    if ed_strs:
        ed_part = f" / под ред. {ed_strs[0]}"

    place = meta.get("publisher-location", "")
    publisher = meta.get("publisher", "")
    year = meta.get("issued", {}).get("date-parts", [[None]])[0][0]
    pages = meta.get("page", "")
    url = meta.get("URL", "")
    access_date = datetime.now().strftime("%d.%m.%Y")

    pages = pages.replace("-", "–")

    parts = []
    if authors:
        parts.append(f"{authors}.")
    parts.append(f"{chapter_title} // {book_title}{ed_part}.")
    parts.append(f"{place} : {publisher}, {year}.")
    if pages:
        parts.append(f"– С. {pages}.")
    if url:
        parts.append(f"– DOI: {url} (дата обращения: {access_date}).")
    return " ".join(parts)
