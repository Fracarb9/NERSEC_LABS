frames = {}
with open("frames.txt","r") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) >=4:
            frame_number = int(parts[0])
            pn = parts[1]
            data = bytes.fromhex(parts[3])
            frames[frame_number] = (pn, data)

c1 = frames[148][1]
c2 = frames[331][1]

xor_payload = bytes(a^b for a,b in zip(c1[48:-8],c2[48:-8]))

with open("expense-form.txt","rb") as f:
    p1=f.read()

p2 = bytes(x ^ y for x, y in zip(xor_payload, p1))
print(p2.decode("utf-8", errors="replace"))