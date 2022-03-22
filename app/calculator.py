

def get_payment(principal, rate, term, dues, taxes):
    # p = 100000  #principal
    # r = .06     #interest rate
    # t = 30      # term in years
    n = 12      #payments per year
    #taxes = 6500

    payment = round((principal * (rate / n) *(1 + rate / n)**(n*term))/((1 + rate / n)**(n*term) - 1), 2)
    total = payment + (taxes/12) + dues
    return total
