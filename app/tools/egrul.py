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
            name=company_data["c"],
            director=company_data["g"],
            inn=company_data["i"],
            kpp=company_data["p"],
            ogrn=company_data["o"],
            registration_date=company_data["r"],
            region=company_data["rn"],
        )

        companies.append(company)

    return companies
