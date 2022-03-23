

def get_payment(principal, rate, term, dues, taxes):
    n = 12      #payments per year
    payment = round((principal * (rate / n) *(1 + rate / n)**(n*term))/((1 + rate / n)**(n*term) - 1), 2)
    total = payment + (taxes/12) + dues
    return total
