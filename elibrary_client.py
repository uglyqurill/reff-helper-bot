import requests
from bs4 import BeautifulSoup
from datetime import datetime

class ELibError(Exception):
    pass

def fetch_metadata_by_elibrary(url: str) -> dict:
    """
    Загружает страницу по ссылке eLibrary и возвращает
    словарь метаданных, унифицированный под format_*().
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        raise ELibError(f"Страница eLibrary не доступна (status={resp.status_code})")
    soup = BeautifulSoup(resp.text, "lxml")

    # Пробуем вытянуть метатеги Dublin Core, которые есть на страницах eLibrary:
    def meta(name):
        tag = soup.find("meta", {"name": name})
        return tag["content"].strip() if tag and tag.get("content") else ""

    # Авторы в строку “Фамилия, И.О.; …”
    creators = meta("DC.Creator")
    authors = []
    if creators:
        for fam_init in creators.split(";"):
            fam_init = fam_init.strip()
            if not fam_init:
                continue
            parts = fam_init.split(",")
            if len(parts) == 2:
                family = parts[0].strip()
                given = parts[1].strip()
            else:
                # если не в формате «Фамилия, И.О.» — кладём всё в family
                family, given = fam_init, ""
            authors.append({"family": family, "given": given})

    title = meta("DC.Title")
    journal = meta("DC.Source")  # часто содержит название журнала
    year = meta("DCTERMS.issued") or meta("DC.Date")
    volume = meta("DC.Date") and meta("DC.Date").split(";")[0].split("=")[-1]  # hack-вариант
    issue = ""  # eLibrary не всегда метит выпуск
    pages = meta("DC.Identifier")  # иногда здесь номер тома/стр.
    doi_url = meta("DC.Identifier") if "doi.org" in meta("DC.Identifier") else ""
    access_date = datetime.now().strftime("%d.%m.%Y")

    # Собираем dict в стиле CrossRef
    return {
        "author": authors,
        "title": [title],
        "container-title": [journal],
        "issued": {"date-parts": [[int(year) if year.isdigit() else None]]},
        "volume": volume,
        "issue": issue,
        "page": pages,
        "URL": doi_url or url,
        "type": "journal-article"
    }

