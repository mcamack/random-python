from dictdiffer import diff
import yaml

with open('d1.yaml') as f:
    d1 = yaml.load(f, Loader=yaml.FullLoader)

with open('d2.yaml') as f:
    d2 = yaml.load(f, Loader=yaml.FullLoader)

# for d in diff(d1, d2):
#     print(d)

changes = []
adds = []
removes = []
for d in diff(d1, d2):
    if d[0] == "change":
        changes.append(d[1:])
    elif d[0] == "add":
        adds.append(d[1:])
    elif d[0] == "remove":
        removes.append(d[1:])
    else:
        pass

print(f"changes: {changes}")
print(f"adds: {adds}")
print(f"removes: {removes}")