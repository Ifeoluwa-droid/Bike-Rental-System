from random import *
from datetime import *

MONTH_MAP = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

BASES_COSTS = {
    'hour': 5,
    'day': 20,
    'week': 60
}


class BikeRental:
    stock = 100
    bikes = [f'BK{i:03}' for i in range(1, stock + 1)]

    list_of_customer_accounts = {
    }

    def __init__(self, name, ):
        self.name = name
        self.account = []
        self.hours = 0
        self.days = 0
        self.weeks = 0
        self.rent_date = None
        self.due_date = None
        self.no_of_bikes = 0
        self.rental_id = ''
        self.total_bill = 0
        self.is_family_rental = False

        # Customer Transaction Process
        self.welcome_message()

    @staticmethod
    def get_available_stock():
        return ', '.join(BikeRental.bikes)

    @staticmethod
    def display_inventory():
        print(BikeRental.get_available_stock())

    def generate_rental_id(self):
        while True:
            rental_id = f"BK-USER{randint(1000, 9999)}{choice(['#', '@', '$', '%', '^', '&'])}"
            if rental_id not in BikeRental.list_of_customer_accounts.keys():
                self.rental_id = rental_id
                break

    def rent_bikes(self, basis):
        if basis != 'family':
            print(f'this rent costs ${BASES_COSTS[basis]} per {basis}')
            basis_count = int(input(f'How many {basis}s?: '))
            if basis == 'hour':
                self.hours = basis_count
            elif basis == 'day':
                self.days = basis_count
            elif basis == 'week':
                self.weeks = basis_count
            self.update_user_account(basis)
            self.issue_bill()
        else:
            self.is_family_rental = True
            print(
                'You can rent 3 to 5 bikes on any basis (hourly, daily or weekly) with a discount of 30% of the total '
                'price')
            user_choice = None
            while user_choice not in ('hourly', 'daily', 'weekly'):
                user_choice = input('On what basis do you want to rent? (hourly, daily, weekly): ').lower()
            if user_choice == 'hourly':
                self.hours = int(input('How many hours?: '))
            elif user_choice == 'daily':
                self.days = int(input('How many days?: '))
            elif user_choice == 'weekly':
                self.weeks = int(input('How many weeks?: '))
            _ = {
                'hourly': 'hour_family',
                'daily': 'day_family',
                'weekly': 'week_family'
            }
            self.update_user_account(_[user_choice])
            self.issue_bill()

    def return_bikes(self):
        rental_id = input('Enter your rental id: ')
        while rental_id not in BikeRental.list_of_customer_accounts.keys():
            rental_id = input('Enter your correct rental id: ')
        self.rental_id = rental_id
        print(
            f"You rented these bikes {', '.join(BikeRental.list_of_customer_accounts[self.rental_id][0])} on {BikeRental.list_of_customer_accounts[self.rental_id][1]}, your total bill is ${BikeRental.list_of_customer_accounts[self.rental_id][2]}")
        owner_answer = None
        while owner_answer != 'y':
            owner_answer = input('Owner has confirmed payment? (y/n): ').lower()
        print(BikeRental.list_of_customer_accounts[self.rental_id][3])
        BikeRental.stock += BikeRental.list_of_customer_accounts[self.rental_id][3]
        BikeRental.list_of_customer_accounts.pop(self.rental_id)

    def welcome_message(self):
        user_choice = input(
            f"Hey {self.name}!\nWhat would you like to do? (rent/return): ").lower()
        while user_choice not in ['rent', 'return']:
            user_choice = input(
                f"Hey {self.name}!\nWelcome to the bike shop\nWhat would you like to do? (rent/return): ").lower()
        return self.pick_rent_basis() if user_choice == 'rent' else self.return_bikes()

    def pick_rent_basis(self):
        print(f"Currently we have {BikeRental.stock} bikes available")
        user_choice = None
        while user_choice not in ('hourly', 'daily', 'weekly', 'family'):
            user_choice = input('On what basis? hourly, daily, weekly or family rental? (input \'family\' for family rental): ').lower()
        return self.rent_bikes(user_choice[:-2]) if user_choice != 'family' and user_choice != 'daily' else self.rent_bikes(user_choice) if user_choice == 'family' else self.rent_bikes('day')

    def calculate_total_bill(self):
        if self.is_family_rental:
            total_bill = round(self.hours * 5 * self.no_of_bikes * 0.7) + round(
                self.days * 20 * self.no_of_bikes * 0.7) + round(
                self.weeks * 60 * self.no_of_bikes * 0.7)
        else:
            total_bill = self.hours * 5 * self.no_of_bikes + self.days * 20 * self.no_of_bikes + self.weeks * 60 * self.no_of_bikes
        return total_bill

    def calculate_rent_date(self):
        self.rent_date = datetime.now()

    def calculate_due_date(self):
        due_date = self.rent_date + timedelta(days=self.days, hours=self.hours, weeks=self.weeks)
        return due_date

    @staticmethod
    def format_date(date_type: datetime):
        return f"{date_type.day}{'st' if str(date_type.day)[-1] == '1' else 'nd' if str(date_type.day)[-1] == '2' else 'rd' if str(date_type.day)[-1] == '3' else 'th'}, of the month of {MONTH_MAP[date_type.month]}, {date_type.year} at {date_type.hour % 12 if date_type.hour not in [12, 0] else date_type.hour if date_type.hour != 0 else 12}:{date_type.minute:02} {'PM' if date_type.hour >= 12 else 'AM'}"

    def issue_bill(self):
        print('Your bill is as stated below:\n\n' + '*' * 30)
        self.calculate_rent_date()
        self.due_date = self.calculate_due_date()
        self.generate_rental_id()
        print(f'NAME: {self.name}')
        print(f'RENTAL ID: {self.rental_id}')
        print(
            f"Date of purchase: {BikeRental.format_date(self.rent_date)}")
        print(
            f"Due date: {BikeRental.format_date(self.due_date)}")
        self.total_bill = self.calculate_total_bill()
        print(f'Your total bill is ${self.total_bill}')
        print('*' * 30 + '\n')
        user_choice = None
        while user_choice != 'y':
            user_choice = input('Complete transaction? (y/n): ').lower()
        BikeRental.list_of_customer_accounts[self.rental_id] = [self.account, self.rent_date, self.total_bill, len(self.account)]

    def update_user_account(self, tag_time):
        self.display_inventory()
        print('*' * 30)
        self.no_of_bikes = int(
            input('These are the current stock, how many bikes do you want? (Note family rental is between 3 to 5): '))
        while len(self.account) < self.no_of_bikes:
            for _ in range(0, self.no_of_bikes):
                random_bike = choice(BikeRental.bikes)
                if random_bike not in self.account:
                    self.account.append(random_bike)
        for bike in self.account:
            print(bike)
            BikeRental.bikes.remove(bike)
        BikeRental.stock -= len(self.account)
        tag_time_map = {
            'hour': f"You have rented the bikes with the following tags\n{', '.join(self.account)} for {self.hours} {tag_time.split('_')[0]}(s)\n",
            'day': f"You have rented the bikes with the following tags\n{', '.join(self.account)} for {self.days} {tag_time.split('_')[0]}(s)\n",
            'week': f"You have rented the bikes with the following tags\n{', '.join(self.account)} for {self.weeks} {tag_time.split('_')[0]}(s)\n",
            'hour_family': f"You have rented the bikes with the following tags\n{', '.join(self.account)} for {self.hours} {tag_time.split('_')[0]}(s) on family rental basis\n",
            'day_family': f"You have rented the bikes with the following tags\n{', '.join(self.account)} for {self.days} {tag_time.split('_')[0]}(s) on family rental basis\n",
            'week_family': f"You have rented the bikes with the following tags\n{', '.join(self.account)} for {self.weeks} {tag_time.split('_')[0]}(s) on family rental basis\n",
        }
        print(tag_time_map[tag_time])


while True:
    customer = BikeRental(input('Hello and welcome to our bike rental shop!\nWhat is your name?: ').title())
    if input("Want to close shop (y/n)? ").lower() == 'y':
        break
