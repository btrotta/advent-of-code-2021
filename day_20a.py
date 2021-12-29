import numpy as np

with open("data.txt", "r") as f:
    data = f.readlines()

pixel_dict = {".": 0, "#": 1}

alg = []
for i, line in enumerate(data):
    if line == "\n":
        break
    alg += [pixel_dict[ch] for ch in line.strip()]

i += 1
img = []
for line in data[i:]:
    img.append([pixel_dict[ch] for ch in line.strip()])

img = np.array(img).astype(int)
fill_value = 0
for step in range(2):
    img_ext = np.zeros((img.shape[0] + 4, img.shape[1] + 4)).astype(int)
    if fill_value == 1:
        img_ext[:] = fill_value
    img_ext[2:(img.shape[0] + 2), 2:(img.shape[1] + 2)] = np.copy(img)
    img_out = np.zeros(img_ext.shape).astype(int)
    # calculate new fill value
    if fill_value == 0:
        fill_value = alg[0]
    elif fill_value == 1:
        fill_value = alg[511]
    # fill border of output with new fill value
    if fill_value == 1:
        img_out[:] = fill_value
    for i in range(1, img_ext.shape[0] - 1):
        for j in range(1, img_ext.shape[1] - 1):
            square = img_ext[(i - 1): (i + 2), (j - 1): (j + 2)]
            bin_str = "".join(str(x) for x in square.flatten())
            ind = int(bin_str, 2)
            img_out[i, j] = alg[ind]
    img = np.copy(img_out)

print(np.sum(img_out))
