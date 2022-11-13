import os

class Logs :
    def __init__(self, start=False) :
        if 'logs' not in os.listdir() :
            os.mkdir('logs')

        self.fpname = 'logs/logs.txt'

        if start :
            self.clear()



    def log(self, log_string, priority=0) :
        priority = '-' * 2 * (11 - priority)

        with open(self.fpname, 'a') as handler :
            handler.write(
                f'{priority} {log_string}\n'
            )




    def read(self, last=-1) :
        with open(self.fpname,'r') as handler :
            lines = handler.readlines()
            if last != -1 or len(lines) < last :
                lines = lines[-last:]

            for line in lines :
                print( line, end='' )




    def clear(self) :
        os.remove('logs/logs.txt')
        open('logs/logs.txt', 'w')
        self.log( 'New log history!', 10 )




if __name__ == '__main__' :
    log = Logs()
    log.log( 'something' )
    log.log( 'something', 5 )
    log.read(20)