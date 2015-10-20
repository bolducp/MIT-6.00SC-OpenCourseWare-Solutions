# Problem Set 1, Problem 1: Paying the Minimum

def get_outstanding_balance():
    outstanding_balance = round(float(raw_input("Enter the outstanding balance on the credit card:  ")), 2)
    return outstanding_balance


def get_annual_interest_rate():
    annual_interest_rate = round(float(raw_input("Enter the annual interest rate as a decimal: ")), 2)
    return annual_interest_rate


def get_minimum_monthly_payment_rate():
    minimum_monthly_payment_rate = round(float(raw_input("Enter the minimum monthly payment rate as a decimal: ")), 2)
    return minimum_monthly_payment_rate


def calculate_minimum_payment(minimum_monthly_payment_rate, outstanding_balance):
    month_min_payment = minimum_monthly_payment_rate * outstanding_balance
    return month_min_payment


def calculate_month_interest_paid(annual_interest_rate, outstanding_balance):
    monthly_interest_rate = annual_interest_rate/12.0
    month_interest_paid = monthly_interest_rate * outstanding_balance
    return month_interest_paid


def calculate_month_principle_paid(month_min_payment, month_interest_paid):
    return month_min_payment - month_interest_paid


def main():
    outstanding_balance = get_outstanding_balance()
    annual_interest_rate = get_annual_interest_rate()
    minimum_monthly_payment_rate = get_minimum_monthly_payment_rate()
    total_paid = 0

    for month in range(1, 13):
        month_min_payment = calculate_minimum_payment(minimum_monthly_payment_rate, outstanding_balance)
        month_interest_paid = calculate_month_interest_paid(annual_interest_rate, outstanding_balance)
        month_principal_paid = calculate_month_principle_paid(month_min_payment, month_interest_paid)

        outstanding_balance -= month_principal_paid
        total_paid += month_min_payment

        print "Month: ", month
        print "Minimum monthly payment: $", round(month_min_payment, 2)
        print "Interest paid: $", round(month_interest_paid, 2)
        print "Principal paid: $", round(month_principal_paid, 2)
        print "Remaining balance: $", round(outstanding_balance, 2), "\n"

    print "RESULT"
    print "Total amount paid: $", round(total_paid, 2)
    print "Remaining balance: $", round(outstanding_balance, 2)

if __name__ == "__main__":
    main()