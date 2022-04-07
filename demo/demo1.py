class Cricle():
    def __init__(self, bankinh):
        self.R = bankinh

    def chuvi(self):
        return self.R *2*3.14

    def dientich(self):
        return self.R**2 * 3.14

def sample1():
    c = Cricle(5)
    print(c.R)
    print('chu vi ', c.chuvi())
    print('dien tich ', c.dientich())

if __name__ == '__main__':
    sample1()