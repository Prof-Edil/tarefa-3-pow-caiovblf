import csv
import os

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'data', 'mempool.csv')
    
    txs = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                continue
            txid = row[0].strip().lower()
            if not txid:
                continue
            try:
                fee = int(row[1])
                weight = int(row[2])
            except ValueError:
                continue
            
            parents = []
            if len(row) >= 4 and row[3].strip():
                parents = [p.strip().lower() for p in row[3].split(';') if p.strip()]
            
            txs[txid] = {'fee': fee, 'weight': weight, 'parents': parents}

    included = []
    included_set = set()
    current_weight = 0

    def get_ancestors(txid, ancestors_set):
        if txid not in txs:
            return False
        for p in txs[txid]['parents']:
            if p not in included_set and p not in ancestors_set:
                ancestors_set.add(p)
                if not get_ancestors(p, ancestors_set):
                    return False
        return True

    def add_tx_and_ancestors(txid):
        nonlocal current_weight
        if txid in included_set:
            return True
        
        missing_ancestors = set()
        if not get_ancestors(txid, missing_ancestors):
            return False
        
        missing_list = list(missing_ancestors)
        missing_list.append(txid)
        
        def do_add(tid):
            nonlocal current_weight
            if tid in included_set:
                return
            for p in txs[tid]['parents']:
                do_add(p)
            included.append(tid)
            included_set.add(tid)
            current_weight += txs[tid]['weight']

        total_new_weight = sum(txs[t]['weight'] for t in missing_list)
        
        if current_weight + total_new_weight <= 4000000:
            do_add(txid)
            return True
        return False

    req_txid = '4c50e3dad7f98bceb6441f96b23748dea84fbdb7cedd603441e6ea4a574d04a6'
    add_tx_and_ancestors(req_txid)

    sorted_txids = sorted(txs.keys(), key=lambda t: txs[t]['fee'] / txs[t]['weight'], reverse=True)
    
    for txid in sorted_txids:
        add_tx_and_ancestors(txid)

    solutions_dir = os.path.join(script_dir, 'solutions')
    os.makedirs(solutions_dir, exist_ok=True)
    output_path = os.path.join(solutions_dir, 'exercise01.txt')
    
    with open(output_path, 'w', newline='\n', encoding='utf-8') as f:
        for txid in included:
            f.write(txid + '\n')

if __name__ == '__main__':
    solve()