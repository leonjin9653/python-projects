import matplotlib.pyplot as plt

class Investment:
    def __init__(self, principal, interest_rate, compound_frequency, contribution_amount, contribution_frequency):
        self.principal = principal
        self.interest_rate = interest_rate
        self.compound_frequency = compound_frequency
        self.contribution_amount = contribution_amount
        self.contribution_frequency = contribution_frequency
    def compound_interest_yby(self, years):
        if self.interest_rate == 0:
            total_contributions_per_year = self.contribution_amount * self.contribution_frequency
            balance = self.principal
            for year in range(1, int(years) + 1):
                balance += total_contributions_per_year
                ### print(f"year {year}: {balance:.2f}")
            print(f"Your total is {balance:.2f} after {years} years.")
            return

        period_rate_contrib = (1 + self.interest_rate / self.compound_frequency) ** (self.compound_frequency / self.contribution_frequency) - 1

        Balance = []

        for year in range(1, int(years) + 1):
            fv_principal = self.principal * (1 + self.interest_rate / self.compound_frequency) ** (year * self.compound_frequency)
            fv_contributions = self.contribution_amount * (((1 + period_rate_contrib) ** (year * self.contribution_frequency) - 1) / period_rate_contrib)
            fv = fv_principal + fv_contributions
            Balance.append(fv)
            print(f"year {year}: {fv:.2f}")

        print(f"Your total is {fv:.2f} after {years} years.")

        plt.plot(range(1, int(years) + 1), Balance)
        plt.xlabel("Year")
        plt.ylabel("Balance($)")
        plt.title("Compound Interest Growth")
        plt.show()

        return Balance 
    
    def compound_interest(self, years):
        if self.interest_rate == 0:
            total_contributions = self.contribution_amount * self.contribution_frequency * years
            future_value = self.principal + total_contributions
        else:
            period_rate_contrib = (1 + self.interest_rate / self.compound_frequency) ** (self.compound_frequency / self.contribution_frequency) - 1
            fv_principal = self.principal * (1 + self.interest_rate / self.compound_frequency) ** (years * self.compound_frequency)
            fv_contributions = self.contribution_amount * (((1 + period_rate_contrib) ** (years * self.contribution_frequency) - 1) / period_rate_contrib)
            future_value = fv_principal + fv_contributions
        print(f"Your total is {future_value:.2f} after {years} years.")
        return
    
    

    def user_input(self):
        principal = float(input("How much is your starting amount?" ))
        interest_rate = (input("What is your interest rate?" ))
        interest_rate = parse_interest_rate(interest_rate)
        years = int(input("How many years? "))
        compounds_frequency = float(input("How many compounds per year? "))
        contribution_ammount = float(input("What is your contribution amount? "))
        contribution_frequency = int(input("How many contributions per year? "))
        method = input("Would you like to see the year by year growth? (yes/no) ").lower().strip()
        if method == "yes":
            investment = Investment(principal, interest_rate, compounds_frequency, contribution_ammount, contribution_frequency)
            investment.compound_interest_yby(years)
        elif method == "no":
            investment = Investment(principal, interest_rate, compounds_frequency, contribution_ammount, contribution_frequency)
            investment.compound_interest(years)
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

investment= Investment(1000, 0.05, 12, 100, 12) ###creates the instance, __init__, which holds all the values minus years
investment.compound_interest(10) ###when the .compound_interest method is called, the only value needed that wasn't held in the instance is years

investment.compound_interest_yby(10) 
'''
#test 3.0
investment = Investment(0, 0, 0, 0, 0)
Investment.user_input(investment)
'''