import hashlib
import os

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, 'data', 'ex02_txid_list.txt')
    
    with open(input_path, 'r', encoding='utf-8') as f:
        txids = [line.strip() for line in f if line.strip()]
        
    target_hex = '49ff8cccf1ca12179e9ae7a4760f550b5a18401b27e1e057604e27c3e10c08fb'
    
    current_level = [bytes.fromhex(tx) for tx in txids]
    target_idx = txids.index(target_hex) if target_hex in txids else -1
        
    proof = []
    
    while len(current_level) > 1:
        next_level = []
        next_target_idx = -1
        
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            
            if target_idx != -1:
                if i == target_idx:
                    proof.append(right)
                    next_target_idx = i // 2
                elif i + 1 == target_idx:
                    proof.append(left)
                    next_target_idx = i // 2
                    
            combined = left + right
            h = hashlib.sha256(combined).digest()
            next_level.append(h)
            
        current_level = next_level
        target_idx = next_target_idx
        
    root = current_level[0].hex()
    proof_hex = [p.hex() for p in proof]
    
    out_dir = os.path.join(script_dir, 'solutions')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'exercise02.txt')
    
    with open(out_path, 'w', newline='\n', encoding='utf-8') as f:
        f.write(root + '\n')
        for p in proof_hex:
            f.write(p + '\n')

if __name__ == '__main__':
    solve()