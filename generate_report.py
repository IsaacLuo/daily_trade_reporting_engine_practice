"""generate report shows:
    Amount in USD settled incoming everyday
    Amount in USD settled outgoing everyday
    Ranking of entities based on incoming and outgoing amount.
"""
import sys

def generate_report(data):
    """
    Args:
        data: the sample_data dict
    """
    #sort data by amount
    for item in data:
        item['amount'] = item['fx'] * item['units'] * item['unit_price']
    
    data.sort(key=lambda item: item['amount'], reverse=True)
    rank = 1
    date_buckets = {'B': {}, 'S': {}}
    for item in data:
        item['rank'] = rank
        rank+= 1
        settlement_date = item['set_date']
        buy_sell = item['buy_sell']
        if settlement_date in date_buckets[buy_sell]:
            date_buckets[buy_sell][settlement_date] += item['amount']
        else:
            date_buckets[buy_sell][settlement_date] = item['amount']

    def print_report_csv(pipe=sys.stdout):
        # show incoming everyday
        print('incoming report', file=pipe)
        for date in sorted(date_buckets['S'].keys()):
            print(date, date_buckets['S'][date], sep=', ', file=pipe)
        print(file=pipe)

        # show outgoing everyday
        print('outgoing report', file=pipe)
        for date in sorted(date_buckets['B'].keys()):
            print(date, date_buckets['B'][date], sep=', ', file=pipe)
        print(file=pipe)
        # show rank
        print('Rank, Entity, Buy/Sell, AgreedFx, Currency, InstructionDate, '\
            'SettlementDate, Units, Price per Unit', file=pipe)
        for item in data:
            print(item['rank'], item['entity'], item['buy_sell'], item['fx'], 
                item['currency'], item['ins_date'], item['set_date'], item['units'], 
                item['unit_price'], sep=', ', file=pipe)

    print_report_csv()
