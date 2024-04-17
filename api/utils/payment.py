import requests
from lxml import etree
from datetime import datetime, date
from django.db.models import Q
from decimal import Decimal
from django.conf import settings


from api.models import User, Payment, Currency, PaymentType, Branch

from .get_data import get_data
from .customer import create_customer, check_customer_data

LOGIN = settings.SMARTUP_LOGIN
PASSWORD = settings.SMARTUP_PASSWORD
API_BASE = settings.SMARTUP_URL


def create_payments(branch_id: str, date: str):
    url = f"https://{API_BASE}/b/es/porting+exp$payment"

    xml_data = f"""
        <?xml version="1.0" encoding="utf-8"?>
        <Root>
            <Logon>
                <login>{LOGIN}</login>
                <password>{PASSWORD}</password>
                <filial>{branch_id}</filial>
                <date>{date}</date>
            </Logon>
        </Root>
        """
    xml_data = xml_data.strip()

    headers = {
        "Content-Type": "application/xml",
    }

    response = requests.post(url, data=xml_data, headers=headers)
    if response.status_code != 200:
        None

    parser = etree.XMLParser(recover=True)
    root = etree.fromstring(response.content, parser=parser)

    payments = root.xpath("//Оплата")

    for payment in payments:
        info = {
            "customer_id": payment.find("ИдКонтрагента").text,
            "payment_id": payment.find("ИдОплаты").text,
            "payment_type_id": payment.find("ИдТипаОплаты").text,
            "amount": payment.find("Сумма").text,
            "base_amount": payment.find("Базовая").text,
            "date_of_payment": payment.find("ДатаОплаты").text,
        }

        if Payment.objects.filter(smartup_id=info["payment_id"]).exists():
            continue

        if not User.objects.filter(smartup_id=info["customer_id"]).exists():
            if not create_customer(info["customer_id"], branch_id=branch_id):
                continue

        user = User.objects.get(smartup_id=info["customer_id"])
        check_customer_data(info["customer_id"], user, branch_id)

        payment_type = PaymentType.objects.get(smartup_id=info["payment_type_id"])
        amount = Decimal(info["amount"])
        base_amount = Decimal(info["base_amount"])
        date_of_payment = datetime.strptime(info["date_of_payment"], "%d.%m.%Y").date()

        payment = Payment.objects.create(
            smartup_id=info["payment_id"],
            customer=user,
            payment_type=payment_type,
            amount=amount,
            base_amount=base_amount,
            date_of_payment=date_of_payment.strftime("%Y-%m-%d"),
        )

        if Branch.objects.filter(smartup_id=str(branch_id)).exists():
            branch = Branch.objects.get(smartup_id=str(branch_id))
            payment.branch = branch
            payment.save()

    return True


def get_payment_list(branch_id: str, date_of_payment=None):
    payment_date = date.today()
    if date_of_payment:
        payment_date = date_of_payment

    payments_query = Payment.objects.filter(date_of_payment=payment_date)

    return payments_query


def get_debt_list(branch_id: str, currency=None, limit=50, customer_id=None):
    columns = ["legal_person_id", "currency_name", "total_amount"]
    filter = []
    if currency == "USD":
        currency_id = "200"
    elif currency == "UZS":
        currency_id = "0"

    if customer_id and currency:
        filter = [
            "and",
            [
                ["legal_person_id", "=", [customer_id]],
                ["currency_id", "=", [currency_id]],
            ],
        ]
    elif customer_id:
        filter = ["legal_person_id", "=", [customer_id]]
    elif currency:
        filter = ["currency_id", "=", [currency_id]]

    sort = ["total_amount"]

    response = get_data(
        endpoint="/b/cs/payment/payment_list+x&table",
        limit=limit,
        columns=columns,
        sort=sort,
        filter=filter,
        branch_id=branch_id,
    )
    if response["count"] <= 0:
        return None

    data = {
        "total_company_debt": {"USD": 0, "UZS": 0},
        "total_customer_debt": {"USD": 0, "UZS": 0},
        "total_uzs": 0,
        "total_usd": 0,
        "customers": [],
    }

    for customer in response["data"]:
        if not User.objects.filter(smartup_id=customer[0]).exists():
            if not create_customer(customer[0], branch_id=branch_id):
                continue
        user = User.objects.get(smartup_id=customer[0])
        currency = Currency.objects.get(name=customer[1])

        currency_name = currency.name
        if currency.name.lower() == "sum" or currency.name.lower() == "base sum":
            currency_name = "UZS"

        item = {
            "smartup_id": customer[0],
            "name": user.name,
            "phone": user.phone,
            "currency": currency_name,
            "amount": float(customer[2]),
        }

        if item["amount"] < 0:
            if item["currency"] == "USD":
                data["total_company_debt"]["USD"] += item["amount"]
            elif item["currency"] == "SUM":
                data["total_company_debt"]["UZS"] += item["amount"]
        else:
            if item["currency"] == "USD":
                data["total_customer_debt"]["USD"] += item["amount"]
            elif item["currency"] == "SUM":
                data["total_customer_debt"]["UZS"] += item["amount"]

        if user.district:
            item["district"] = user.district.name
            item["city"] = user.district.city.name
        data["customers"].append(item)

    data["total_usd"] = (
        data["total_company_debt"]["USD"] + data["total_customer_debt"]["USD"]
    )
    data["total_uzs"] = (
        data["total_company_debt"]["UZS"] + data["total_customer_debt"]["UZS"]
    )
    return data
