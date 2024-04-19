from .get_data import get_data


def get_debt_list(branch_id: str, currency="USD", limit=50) -> dict:
    columns = [
        "legal_person_id",
        "legal_person_name",
        "currency_name",
        "debit_amount",
    ]

    currency_id = "200"
    if currency == "UZS":
        currency_id = "0"

    filter = ["currency_id", "=", [currency_id]]
    sort = ["-debit_amount"]

    response = get_data(
        endpoint="/b/cs/payment/payment_list+x&table",
        limit=limit,
        columns=columns,
        sort=sort,
        filter=filter,
        branch_id=branch_id,
    )

    if not response or response["count"] <= 0:
        return None

    data = {"total_debt": 0, "customers": []}

    for debt_info in response["data"]:
        item = {
            "id": debt_info[0],
            "name": debt_info[1],
            "currency": debt_info[2],
            "amount": float(debt_info[3]),
        }

        data["total_debt"] += item["amount"]
        data["customers"].append(item)
    return data
