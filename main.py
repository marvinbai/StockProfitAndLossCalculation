import sys, csv, collections

#### Helper function for output.
def printPairs(openTime, closeTime, symbol, quantity, openSide, closeSide, openPrice, closePrice):
    if openSide == 'B' and closeSide == 'S':
        pnl = (closePrice - openPrice) * quantity
    elif openSide == 'S' and closeSide == 'B':
        pnl = (openPrice - closePrice) * quantity
    else:
        print('ERROR IN PRINTPAIRS!')
    print(str(openTime) + ',' + str(closeTime) + ',' + symbol + ',' + str(quantity) + ',' + format(pnl, '.2f') + ',' + openSide + ',' + closeSide + ',' + str(openPrice) + ',' + str(closePrice))
    return pnl

#### Main function.
print('OPEN_TIME,CLOSE_TIME,SYMBOL,QUANTITY,PNL,OPEN_SIDE,CLOSE_SIDE,OPEN_PRICE,CLOSE_PRICE')   # Header.

f = open(sys.argv[1], 'rt')
reader = csv.reader(f)
_ = next(reader)    # Header.

mapOpen = {}    # A dictionary maps from symbol to its openning queue(tuple: (quantity, price)).
pnl_cum = 0     # Cumulative profit and loss.
 
for row in reader:
    time = int(row[0])
    symbol = row[1]
    side = row[2]
    price = float(row[3])
    quantity = int(row[4])
    if not symbol in mapOpen:   # First time see this stock.
        q = collections.deque()
        if side == 'B':
            q.append([quantity, price, time])
        elif side == 'S':
            q.append([-quantity, price, time])
        mapOpen[symbol] = q
    else:   # This stock has appeared before.
        q = mapOpen[symbol]
        if side == 'B':
            if len(q) > 0 and q[0][0] < 0:  # The item in queue is negative, meaning we sell short last time.
                while len(q) > 0 and quantity >= abs(q[0][0]):
                    pnl_cum += printPairs(q[0][2], time, symbol, -q[0][0], 'S', 'B', q[0][1], price)
                    quantity -= abs(q[0][0])
                    q.popleft()
                if quantity > 0 and len(q) == 0:
                    q.append([quantity, price, time])
                elif quantity > 0 and len(q) != 0:
                    pnl_cum += printPairs(q[0][2], time, symbol, quantity, 'S', 'B', q[0][1], price)
                    q[0][0] = -(abs(q[0][0]) - quantity)
                    quantity = 0
            else:
                q.append([quantity, price, time])
        elif side == 'S':
            if len(q) > 0 and q[0][0] > 0:  # The storage has something for sale.
                while len(q) > 0 and quantity >= q[0][0]:
                    pnl_cum += printPairs(q[0][2], time, symbol, q[0][0], 'B', 'S', q[0][1], price)
                    quantity -= q[0][0]
                    q.popleft()
                if quantity > 0 and len(q) == 0:
                    q.append([-quantity, price, time])
                elif quantity > 0 and len(q) != 0:
                    pnl_cum += printPairs(q[0][2], time, symbol, quantity, 'B', 'S', q[0][1], price)
                    q[0][0] = q[0][0] - quantity
                    quantity = 0
            else:
                q.append([-quantity, price, time])

print(format(pnl_cum, '.2f'))
f.close()




