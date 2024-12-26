import threading
from time import sleep

class User:
    name: str = ""
    money: float = 0
    invested_money: float = 0

    def __init__(self, name, starting_money: float):
        self.name = name
        self.money = starting_money
    
class StockInfo:
    start_money: float = 0
    money: float = 0
    increase: float = 0
    name: str = ""
    time: int = 0

class Stock:
    name: str = ""
    money: float = 0
    user_start_money: dict[str, int] = {} # users name : time of invest
    money_time: list[float] = [] # money over time
    time: int = 0
    update_thread: threading.Thread = None
    running: bool = True
    
    def __init__(self, name):
        self.name = name
        self.update_thread = threading.Thread(target=self.m_UpdateTime)
        self.update_thread.start()
    
    def CloseStock(self):
        self.running = False
        self.update_thread.join()
    
    def AddStock(self, user: User, amount: float):
        user.money -= amount
        self.money += amount
        user.invested_money += amount

        if user.name in self.user_start_money.values():
            self.user_start_money[user.name] += amount
        else:
            self.user_start_money[user.name] = amount
    
    def m_MoneyConvert(amount: float):
        return amount
    
    def RemoveStock(self, user: User, amount: float) -> bool:
        if (user.invested_money < amount):
            return False
        
        return True
    
    def GetStockInfo(self, start_time) -> StockInfo:
        if start_time < 0 or start_time >= len(self.money_time):
            return 0

        info: StockInfo = StockInfo()

        info.money = self.money
        info.start_money = self.money_time[start_time]
        info.time = self.time
        
        if (self.money_time[start_time] == 0):
            info.increase = self.money
        elif (self.money == 0):
            info.increase = -self.money_time[start_time]
        else:
            dif = abs(self.money_time[start_time] - self.money)
            average =(self.money_time[start_time] + self.money) / 2

            if self.money > self.money_time[start_time]:
                info.increase = dif / average
            else:
                info.increase = -(dif / average)
            
            info.increase *= 100
        
        info.name = self.name

        return info

    def m_UpdateTime(self):
        while self.running:
            self.money_time.append(self.money)
            self.time += 1
            sleep(1)
        

def main():
    guy: User = User("guy", 100)
    netflix: Stock = Stock("netflix")

    while True:
        u_input: str = input()
        command = u_input.split(" ")[0]
        u_length: int = len(u_input.split(" "))
        
        if command == "check" and u_length == 2:
            start_time = int(u_input.split(" ")[1])

            if not netflix.GetStockInfo(start_time):
                continue
            print("start stock money: ", netflix.GetStockInfo(start_time).start_money)
            print("stock money: ", netflix.GetStockInfo(start_time).money)
            print("stock increase: ", netflix.GetStockInfo(start_time).increase)
            print("time: ", netflix.GetStockInfo(start_time).time)
        elif command == "user":
            print("person money: ", guy.money)
            print("person investment: ", guy.invested_money)
        elif command == "add" and u_length == 2:
            amount = int(u_input.split(" ")[1])
            netflix.AddStock(guy, amount)
        elif command == "end":
            netflix.CloseStock()
            return
        
        print("")
    