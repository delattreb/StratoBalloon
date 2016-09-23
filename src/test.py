# message = "Chuc"
message = "Chuck "

bin_message = ""
cpt = 0
for i in message:
    binary = bin(ord(i))[2:]

    if cpt > 1:
        if len(binary) < 8:
            for j in range(8 - len(binary)):
                binary = "0" + binary

    bin_message += binary
    cpt += 1

print(bin_message)

# check serie
serie = 0
last = bin_message[0]
out = ""
cpt = 0
for i in bin_message:
    cpt += 1
    if i == last:
        serie += 1
    else:
        if last == "0":
            out += "00 "
        else:
            out += "0 "
        for j in range(serie):
            out += "0"
        out += " "
        serie = 1
    last = i
    if cpt == len(bin_message):
        if last == "0":
            out += "00 "
        else:
            out += "0 "
        for j in range(serie):
            out += "0"

print(out)
