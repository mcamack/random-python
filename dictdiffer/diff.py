from dictdiffer import diff
import yaml

with open('d-old.yaml') as f:
    d1 = yaml.load(f, Loader=yaml.FullLoader)

with open('d-new.yaml') as f:
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

print("\nChange parsing")
actual_adds=[]
actual_dels=[]
for change in changes:
    print(f"key: {change[0]}")
    d = change[1][0]
    a = change[1][1]
    print(f"  del: {d}")
    print(f"  add: {a}")

    print("  check if a change is actually a move")
    s1 = "d1"
    s2 = "d2"
    for k in change[0][:-1]:
        s1 += "[\'" + k + "\']"
        s2 += "[\'" + k + "\']"
        print(f"s: {s1}")
        print(f"s: {s2}")
    if d in eval(s2):
        print(f"{d} actually moved (not deleted)")
    else:
        actual_dels.append(d)

    if a in eval(s1):
        print(f"{a} actually moved (not added)")
    else:
        actual_adds.append(a)



print("\n\ncheck if an add is actually a move")
for add in adds:
    print(f"add[0]: {add[0]}")
    print(f"add[1]: {add[1]}")
    for item in add[1]:
        print(f"item: {item}")
        check_if_moved = item[1]
        # if item[1] in d1["key1"]["names"]:
        #build indexer
        s = "d1"
        for k in add[0].split("."):
            s += "[\'" + k + "\']"
            print(f"s: {s}")
        if item[1] in eval(s):
            print(f"{item[1]} moved positions (not added)")
        else:
            actual_adds.append(item[1])

print(f"actual_adds: {actual_adds}")
print(f"actual_dels: {actual_dels}")