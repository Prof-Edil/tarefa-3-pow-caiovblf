import hashlib
import os
import multiprocessing

def mine(start_nonce, step, prefix_hex, target_hex, queue):
    nonce = start_nonce
    target = bytes.fromhex(target_hex)
    prefix = bytes.fromhex(prefix_hex)
    max_nonce = 0xFFFFFFFFFFFFFFFF
    
    while nonce <= max_nonce:
        nonce_bytes = nonce.to_bytes(8, 'big')
        if hashlib.sha256(prefix + nonce_bytes).digest() <= target:
            queue.put((prefix + nonce_bytes).hex())
            return
        nonce += step

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    in_path = os.path.join(script_dir, 'solutions', 'exercise02.txt')
    
    with open(in_path, 'r', encoding='utf-8') as f:
        merkle_root = f.readline().strip()
        
    version = "00000002"
    prev_block = "00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee"
    timestamp = "495f8f09"
    prefix_hex = version + prev_block + merkle_root + timestamp
    target_hex = "00000000ffff0000000000000000000000000000000000000000000000000000"

    cores = multiprocessing.cpu_count()
    queue = multiprocessing.Queue()
    procs = []

    for i in range(cores):
        p = multiprocessing.Process(target=mine, args=(i, cores, prefix_hex, target_hex, queue))
        procs.append(p)
        p.start()

    header = queue.get()

    for p in procs:
        p.terminate()

    out_dir = os.path.join(script_dir, 'solutions')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'exercise03.txt')
    
    with open(out_path, 'w', newline='\n', encoding='utf-8') as f:
        f.write(header + '\n')

if __name__ == '__main__':
    multiprocessing.freeze_support()
    solve()