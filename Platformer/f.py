speed = 0
pos = 0
d = .2
s = 0
while pos < 80:
    speed += d
    pos += speed
    s += 1
print(pos, s)