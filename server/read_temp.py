

def read_current_temperature():
    with open('current_temp.dat','r') as csvfile:
        for row in csvfile:
            if row.startswith('#'):
                continue
            print 'row = ',row
            row = row.split()
            timestamp = row[0]
            temperature = float(row[1])
            humidity = float(row[2])
            return timestamp, temperature, humidity


if __name__ == '__main__':
    print read_current_temp()
    

