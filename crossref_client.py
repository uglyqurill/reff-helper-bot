import requests

class CrossrefError(Exception):
    """Собственное исключение для ошибок CrossRef."""
    pass

def fetch_metadata_by_doi(doi: str) -> dict:
    """
    Запрашивает CrossRef API по DOI и возвращает словарь метаданных.
    """
    url = f"https://api.crossref.org/works/{doi}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise CrossrefError(f"Ошибка запроса к CrossRef: {e}")
    data = resp.json()
    if "message" not in data:
        raise CrossrefError("Неожиданный формат ответа от CrossRef")
    return data["message"]
