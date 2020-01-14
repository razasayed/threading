import threading
import concurrent.futures
import time

# lock = threading.Lock()
# print(lock) #Unlocked
# lock.acquire()
# print(lock) #Locked
# lock.release()
# print(lock) #Unlocked

#Program to demonstrate solving the race condition problem with a lock

class Account:
    def __init__(self):
        self.balance = 100 #Shared data, like a database for example
        self.lock = threading.Lock()
    def update(self, transaction, amount):
        print(f'{transaction} thread updating...')
        with self.lock:
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
