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
kv_adds= {}
kv_deletes= {}
for change in changes:
    print(f"key: {change[0]}")
    d = change[1][0]
    a = change[1][1]
    print(f"  del: {d}")
    print(f"  add: {a}")

    print("  check if add is None which means key was totally removed")
    if a is None:
        if type(d) is dict:
            print(f"key deleted completely: {d.keys()}")
            for k,v in d.items():
                for i in v:
                    kv_deletes.setdefault('.'.join([change[0], k]), []).append(i)
        elif type(d) is list:
            for i in d:
                kv_deletes.setdefault(change[0], []).append(i)
    else:
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
            print(f"^^^{'.'.join(change[0][:-1])}")
            # kv_deletes['.'.join(change[0][:-1])].append(d)
            kv_deletes.setdefault('.'.join(change[0][:-1]), []).append(d)
            # ['.'.join(change[0][:-1])].append(d)

        if a in eval(s1):
            print(f"{a} actually moved (not added)")
        else:
            actual_adds.append(a)
            kv_adds.setdefault('.'.join(change[0][:-1]), []).append(a)



print("\n\ncheck if an add is actually a move")
for add in adds:
    print(f"add[0]: {add[0]}")
    print(f"add[1]: {add[1]}")
    for item in add[1]:
        print(f"item: {item}")

        if type(item[0]) is not int: #new key added
            if type(item[1]) == list:
                for j in item[1]:
                    kv_adds.setdefault(add[0] + "." + item[0], []).append(j)
            else:
                kv_adds.setdefault(add[0]+"."+item[0], []).append(item[1])
        else:

            #build indexer
            s = "d1"
            for k in add[0].split("."):
                s += "[\'" + k + "\']"
                print(f"s: {s}")

            # if item[1] in list(eval("d1"+".keys()")):
            if item[1] in eval(s):
                print(f"{item[1]} moved positions (not added)")
            else:
                actual_adds.append(item[1])
                kv_adds.setdefault(add[0], []).append(item[1])

for remove in removes:
    print(f"remove[0]: {remove[0]}")
    print(f"remove[1]: {remove[1]}")
    for item in remove[1]:
        print(f"item: {item}")

        # build indexer
        s = "d2"
        for k in remove[0].split("."):
            s += "[\'" + k + "\']"
            print(f"s: {s}")
        if item[1] in eval(s):
            print(f"{item[1]} moved positions (not deleted)")
        else:
            actual_dels.append(item[1])
            kv_deletes.setdefault(remove[0], []).append(item[1])

print("\n\n#### OUT ####")
# print(f"kv_deletes: {kv_deletes}")
# print(f"kv_adds: {kv_adds}")

for k,v in kv_deletes.items():
    k = k.replace(".", "/")
    for i in v:
        print(f"delete {k}/{i}")

for k,v in kv_adds.items():
    k = k.replace(".", "/")
    for i in v:
        print(f"create {k}/{i}")

# Look for new keys