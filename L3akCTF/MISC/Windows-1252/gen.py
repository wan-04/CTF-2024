from PIL import Image

img = Image.open(r"download.png")
px = img.load()

def getblock(n0,n1,n2,n3):
    block = []
    for i in range(n0,n1):
        for j in range(n2,n3):
            r, g, b= px[i,j]
            block.append("[" + str(r) + "," + str(g) + "," + str(b) + "]")
    return block

for _ in range(188):

    block0 = getblock(25*_, 25*(_+1), 0, 25)

    with open ("rgb.txt", "w") as f:
        for i in range(25):
            for j in range(25):
                f.write(block0[25*i + j] + " ")
            f.write("\n")
                
    with open("rgb.txt","r") as f:
        lines = f.readlines()
        width = len(lines)
        tmp = lines[1].split(" ")
        length = len(tmp) - 1
            
    imgsize = (width,length)
    img = Image.new("RGB", imgsize)
    pix = img.load()
    for i in range (width):
        temp = lines[i].split(" ")
        for j in range (length):
            temp[j] = temp[j].replace('[','')
            temp[j] = temp[j].replace(']','')
            t = temp[j].split(",")
            t2 = (int(t[0]), int(t[1]), int(t[2]))
            pix[i, j] = t2
    name = "flag" + str(_) + ".png"

    img.save(name)