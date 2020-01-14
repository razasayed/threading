import concurrent.futures
import time

#Program to demonstrate a race condition

class Account:
    def __init__(self):
        self.balance = 100 #Shared data, like a database for example
    def update(self, transaction, amount):
        print(f'{transaction} thread updating...')
        #Simulate reading from a database
        local_copy = self.balance
        local_copy += amount
        time.sleep(1)
        #Write the new value back to the database
        self.balance = local_copy
        print(f'{transaction} thread finishing...')

if __name__ == '__main__':
    account = Account()
    print(f'Starting with balance of {account.balance}')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        for transaction, amount in [('deposit', 50), ('withdrawal', -150)]:
            ex.submit(account.update, transaction, amount)
    print(f'ending balance in account is {account.balance}')