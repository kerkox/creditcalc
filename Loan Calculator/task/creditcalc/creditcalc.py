import argparse
from math import ceil, log, floor

parser = argparse.ArgumentParser(description="This program is a calculator for loans")
parser.add_argument("--type")
parser.add_argument("--payment")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")

args = parser.parse_args()
correct_parameters = True
principal = 0
periods = 0
interest = 0
payment = 0

if args.type is None or (args.type != "diff" and args.type != "annuity"):
    correct_parameters = False
elif args.type == "diff" and (args.payment is not None):
    correct_parameters = False
elif args.interest is None or args.interest == "":
    correct_parameters = False
elif args.type != "annuity" and args.principal is None:
    correct_parameters = False

if args.principal is not None:
    principal = float(args.principal)
if args.periods is not None:
    periods = int(args.periods)
if args.interest is not None:
    interest = float(args.interest)

if args.payment is not None:
    payment = float(args.payment)

if principal < 0 or periods < 0 or interest < 0 or payment < 0:
    correct_parameters = False


def calculate_diff_payment(principal_, interest_, month, periods_n):
    p, n, m = principal_, periods_n, month
    i = (interest_ / 100) / 12
    diff = ceil((p / n) + (i * (p - ((p * (m - 1)) / n))))
    return diff


def differentiated_payments(principal_, interest_, periods_n):
    payment_per_month = []
    total = 0
    for n in range(1, periods_n + 1):
        month_payment = calculate_diff_payment(principal_, interest_, n, periods_n)
        payment_per_month.append(month_payment)
        total += month_payment
    overpayment = ceil(total - principal_)
    return payment_per_month, overpayment


def print_differentiated_payment(payment_per_month, overpayment):
    for month in range(len(payment_per_month)):
        print(f"Month {month + 1}: payment is {payment_per_month[month]}")
    print(f"\nOverpayment = {overpayment}")


def number_monthly_payments(loan_principal, monthly_payment, loan_interest):
    i = (loan_interest / 100) / 12
    n = ceil(log((monthly_payment / (monthly_payment - (i * loan_principal))), 1 + i))
    years = floor(n / 12)
    months = n - (years * 12)
    years_str = f"{years} years" if years > 0 else ""
    months_str = f"{months} months" if months > 0 else ""
    connector_and = f" and " if years_str != "" and months_str != "" else ""
    overpayment = ceil((n * monthly_payment) - principal)
    print(f"It will take {years_str}{connector_and}{months_str} to repay this loan!")
    print(f"Overpayment = {overpayment}")


def annuity_monthly_payment_amount(principal_, periods_, interest_):
    i = (interest_ / 100) / 12
    payment_ = ceil(principal_ * ((i * pow(1 + i, periods_)) / (pow(1 + i, periods_) - 1)))
    print(f"Your monthly payment = {payment_}!")


def loan_principal_value(payment_, periods_, interest_):
    i = (interest_ / 100) / 12
    loan_principal = floor(payment_ / ((i * pow(1 + i, periods_)) / (pow(1 + i, periods_) - 1)))
    overpayment = ceil((payment_ * periods_) - loan_principal)
    print(f"Your loan principal = {loan_principal}!")
    print(f"Overpayment = {overpayment}")


def make_calculations(type_, principal_, periods_, interest_, payment_):
    if type_ == "diff":
        (payment_list, overpayment) = differentiated_payments(principal_, interest_, periods_)
        print_differentiated_payment(payment_list, overpayment)
    elif type_ == "annuity":
        if principal_ > 0:
            if payment_ > 0:
                number_monthly_payments(principal_, payment_, interest_)
            else:
                annuity_monthly_payment_amount(principal_, periods_, interest_)
        else:
            loan_principal_value(payment_, periods_, interest_)


if correct_parameters:
    make_calculations(args.type, principal, periods, interest, payment)
else:
    print("Incorrect parameters")
