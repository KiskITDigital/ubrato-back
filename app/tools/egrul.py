from typing import List

import requests
from schemas import models

EGRUL_URL = "https://egrul.nalog.ru/"


def get_org_by_query(query: str) -> List[models.EgrulCompany]:
    form_data = {
        "vyp3CaptchaToken": "",
        "page": "",
        "query": query,
        "region": "",
        "PreventChromeAutocomplete": "",
    }

    response = requests.post(EGRUL_URL, data=form_data)

    response = requests.get(
        EGRUL_URL + "search-result/" + response.json()["t"]
    )

    companies: List[models.EgrulCompany] = []

    for company_data in response.json()["rows"]:
        company = models.EgrulCompany(
            name=company_data.get("c", ""),
            director=company_data.get("g", ""),
            inn=company_data.get("i", ""),
            kpp=company_data.get("p", ""),
            ogrn=company_data.get("o", ""),
            registration_date=company_data.get("r", ""),
            region=company_data.get("rn", ""),
        )
        companies.append(company)

    return companies
