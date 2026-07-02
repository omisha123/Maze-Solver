import os
import cv2
import numpy as np

def maze(img_path, out_path):
    img = cv2.imread(img_path)
    if img is None:
        return None
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower1 = np.array([0, 70, 50])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([170, 70, 50])
    upper2 = np.array([180, 255, 255])
    
    m1 = cv2.inRange(hsv, lower1, upper1)
    m2 = cv2.inRange(hsv, lower2, upper2)
    walls = m1 + m2
    
    grid = np.zeros((40, 40), dtype=int)
    for r in range(40):
        for c in range(40):
            ystart, yend = r * 20, (r + 1) * 20
            xstart, xend = c * 20, (c + 1) * 20
            box = walls[ystart+3:yend-3, xstart+3:xend-3]
            if np.sum(box == 255) > 10:
                grid[r, c] = 1
            else:
                grid[r, c] = 0
                
    start = (0, 0)
    end = (39, 39)
    
    if grid[start] == 1 or grid[end] == 1:
        blue = np.zeros((800, 800, 3), dtype=np.uint8)
        blue[:] = [255, 0, 0]
        text = "IMPOSSIBLE, LACHURE SIR TRICKED ME"
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, 1.1, 3)[0]
        text_x = (800 - text_size[0]) // 2
        text_y = (800 + text_size[1]) // 2
        cv2.putText(blue, text, (text_x, text_y), font, 1.1, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.imwrite(out_path, blue)
        return None

    queue = [start]
    visited = {start: None}
    found = False
    
    while queue:
        curr = queue.pop(0)
        if curr == end:
            found = True
            break
            
        cr, cc = curr
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < 40 and 0 <= nc < 40 and grid[nr, nc] == 0:
                nxt = (nr, nc)
                if nxt not in visited:
                    visited[nxt] = curr
                    queue.append(nxt)
                    
    if not found:
        blue = np.zeros((800, 800, 3), dtype=np.uint8)
        blue[:] = [255, 0, 0]
        text = "IMPOSSIBLE, LACHURE SIR TRICKED ME"
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, 1.1, 3)[0]
        text_x = (800 - text_size[0]) // 2
        text_y = (800 + text_size[1]) // 2
        cv2.putText(blue, text, (text_x, text_y), font, 1.1, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.imwrite(out_path, blue)
        return None

    clean_out = img.copy()
    path_list = []
    curr = end
    while curr is not None:
        path_list.append(curr)
        curr = visited[curr]
    path_list.reverse()
    
    for i in range(len(path_list) - 1):
        r1, c1 = path_list[i]
        r2, c2 = path_list[i+1]
        p1 = (c1 * 20 + 10, r1 * 20 + 10)
        p2 = (c2 * 20 + 10, r2 * 20 + 10)
        cv2.line(clean_out, p1, p2, (0, 255, 0), 12)
        
    cv2.imwrite(out_path, clean_out)
    return len(path_list)

def main():
    mazefile = './mazes'
    ansfile = './answers'
    
    if not os.path.exists(ansfile):
        os.makedirs(ansfile)
        
    valid_lengths = []
    print("Processing all challenge assets in strict numerical order...")
    
    for i in range(1, 101):
        if i < 10:
            name = f"maze_{i:02d}.png"
        else:
            name = f"maze_{i}.png"
            
        img_path = os.path.join(mazefile, name)
        out_path = os.path.join(ansfile, f"solved_{name}")
        
        if os.path.exists(img_path):
            length = maze(img_path, out_path)
            if length is not None:
                valid_lengths.append(length)
                print(f"✅ {name}: Solved! Steps = {length}")
            else:
                print(f"❌ {name}: Trap! Blue screen generated.")
        else:
            print(f"⚠️ FILE NOT FOUND: Looked for '{name}' at path: {img_path}")
                
    MOD = int(1e9 + 7)
    password = 1
    for length in valid_lengths:
        password = (password * length) % MOD
        
    print("\n" + "="*45)
    print(f"  SUCCESSFULLY DECRYPTED!")
    print(f"  FINAL PASSWORD NUMBER: {password}")
    print("="*45)
    
    with open("password.txt", "w") as f_out:
        f_out.write(str(password))

if __name__ == "__main__":
    main()