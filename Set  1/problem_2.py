# Problem Set 1, Problem 2: Paying Off Debt in a Year

def get_outstanding_balance():
    outstanding_balance = round(float(raw_input("Enter the outstanding balance on the credit card:  ")), 2)
    return outstanding_balance


def get_annual_interest_rate():
    annual_interest_rate = round(float(raw_input("Enter the annual interest rate as a decimal: ")), 2)
    return annual_interest_rate


def main():
    starting_balance = get_outstanding_balance()
    annual_interest_rate = get_annual_interest_rate()

    monthly_interest_rate = annual_interest_rate/12.0
    min_monthly_payment = 10.0

    outstanding_balance = starting_balance

    while outstanding_balance > 0:
        months = 0
        min_monthly_payment += 10.0
        outstanding_balance = starting_balance

        for month in range(1, 13):
            if outstanding_balance > 0:
                outstanding_balance = outstanding_balance * (1 + monthly_interest_rate) - min_monthly_payment
                months += 1

    print "\n" + "RESULT"
    print "Monthly payment to pay off debt in 1 year:", min_monthly_payment
    print "Number of months needed:", months
    print "Balance:", round(outstanding_balance, 2)


if __name__ == "__main__":
    main()


