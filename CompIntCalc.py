class Investment:
    def __init__(self, principal, interest_rate, compound_frequency, contribution_amount, contribution_frequency):
        self.principal = principal
        self.interest_rate = interest_rate
        self.compound_frequency = compound_frequency
        self.contribution_amount = contribution_amount
        self.contribution_frequency = contribution_frequency
    def compound_interest_yby(self, principal, interest_rate, compound_frequency, contribution_amount, contribution_frequency, years):
        years = years 
        if interest_rate == 0:
            total_contributions_per_year = contribution_amount * contribution_frequency
            balance = principal
            for year in range(1, int(years) + 1):
                balance += total_contributions_per_year
                print(f"year {year}: {balance:.2f}")
            print(f"Your total is {balance:.2f} after {years} years.")
            return

        period_rate_contrib = (1 + interest_rate / compound_frequency) ** (compound_frequency / contribution_frequency) - 1

        for year in range(1, int(years) + 1):
            fv_principal = principal * (1 + interest_rate / compound_frequency) ** (year * compound_frequency)
            fv_contributions = contribution_amount * (((1 + period_rate_contrib) ** (year * contribution_frequency) - 1) / period_rate_contrib)
            fv = fv_principal + fv_contributions
            print(f"year {year}: {fv:.2f}")

        print(f"Your total is {fv:.2f} after {years} years.")
    def compound_interest(self, principal, interest_rate, compound_frequency, contribution_amount, contribution_frequency, years):
        if interest_rate == 0:
            total_contributions = contribution_amount * contribution_frequency * years
            future_value = principal + total_contributions
        else:
            period_rate_contrib = (1 + interest_rate / compound_frequency) ** (compound_frequency / contribution_frequency) - 1
            fv_principal = principal * (1 + interest_rate / compound_frequency) ** (years * compound_frequency)
            fv_contributions = contribution_amount * (((1 + period_rate_contrib) ** (years * contribution_frequency) - 1) / period_rate_contrib)
            future_value = fv_principal + fv_contributions
        print(f"Your total is {future_value:.2f} after {years} years.")
        return
    
    

def user_input():
    principal = float(input("How much is your starting amount?" ))
    interest_rate = (input("What is your interest rate?" ))
    interest_rate = parse_interest_rate(interest_rate)
    years = int(input("How many years? "))
    compounds_frequency = float(input("How many compounds per year? "))
    contribution_ammount = float(input("What is your contribution amount? "))
    contribution_frequency = int(input("How many contributions per year? "))
    method = input("Would you like to see the year by year growth? (yes/no) ").lower().strip()
    if method == "yes":
        Investment.compound_interest_yby(principal, interest_rate, compounds_frequency, contribution_ammount, contribution_frequency, years)
    elif method == "no":
        Investment.compound_interest(principal, interest_rate, compounds_frequency, contribution_ammount, contribution_frequency, years)
    else:
        print("Please enter yes or no.")


def parse_interest_rate(user_interest_input):
    if isinstance(user_interest_input, (int, float)):
        user_input = str(user_interest_input)
    else: 
        user_input = user_interest_input
    cleaned = user_input.strip()
    cleaned_new = cleaned.replace('%', '').strip() #replace("old value", "new value")
    if not cleaned_new:
        raise ValueError("Interest rate cannot be empty")
    try:
        interest_rate = float(cleaned_new)
        if interest_rate > 1 or cleaned_new != cleaned: ###assumes user input "%5", thus converting to 0.05.
            return interest_rate/100
        else: ###assumes user input 0.05 and no conversions need to be made
            return interest_rate
    except ValueError:
        raise ValueError(f"Could not parse {user_interest_input} as a valid interest rate")





###test
'''
type = input("Would you like to see the year by year by year growth?").lower().strip()
if type == "yes":
    compound_interest_yby(user_input)
elif type == "no":
    compound_interest(user_input)
else:
    print("yes or no.")
'''

#test 2.0
Investment.compound_interest(1000, 0.05, 12, 100, 12, 10)