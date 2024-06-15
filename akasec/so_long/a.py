from PIL import Image
import cv2
import io
from base64 import*


def getblock(n0,n1,n2,n3,px,x):
    block = []
    for i in range(n0,n1):
        for j in range(n2,n3):
            r, g, b= px[i,j]
            block.append("[" + str(r) + "," + str(g) + "," + str(b) + "]")
    with open ("rgb.txt", "w") as f:
        for i in range(25):
            for j in range(25):
                f.write(block[25*i + j] + " ")
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
            if t2 == (0, 0, 255):
                t2 = (255, 255, 255)
            pix[i, j] = t2
    name = "chall" + str(x) + ".png"
    img.save(name)

def bytes_to_image(byte_data):
    # Tạo một đối tượng BytesIO từ dãy byte
    byte_stream = io.BytesIO(byte_data)

    # Mở ảnh từ đối tượng BytesIO
    image = Image.open(byte_stream)

    return image

def img_to_pixel(image_path):
    img = Image.open(image_path)
    pixel = img.load()
    pixel_of_image = []
    for x in range(img.size[0]):
        out = []
        for y in range(img.size[1]):
            r, g, b= pixel[x, y]
            out.append("[" + str(r) + "," + str(g) + "," + str(b) + "] ")
        pixel_of_image.append(out)
    return pixel_of_image

def compare_images(image1_path, image2_path):

    if image1_path == image2_path:
        return True
    
chall_file = ["chall0.png","chall1.png","chall2.png","chall3.png","chall4.png"]
lst_file = ['flag0.png', 'flag1.png', 'flag2.png', 'flag3.png', 'flag4.png', 'flag5.png', 'flag6.png', 'flag7.png', 'flag8.png', 'flag9.png', 'flag10.png', 'flag11.png', 'flag12.png', 'flag13.png', 'flag14.png', 'flag15.png', 'flag16.png', 'flag17.png', 'flag18.png', 'flag19.png', 'flag20.png', 'flag21.png', 'flag22.png', 'flag23.png', 'flag24.png', 'flag25.png', 'flag26.png', 'flag27.png', 'flag28.png', 'flag29.png', 'flag30.png', 'flag31.png', 'flag32.png', 'flag33.png', 'flag34.png', 'flag35.png', 'flag36.png', 'flag37.png', 'flag38.png', 'flag39.png', 'flag40.png', 'flag41.png', 'flag42.png', 'flag43.png', 'flag44.png', 'flag45.png', 'flag46.png', 'flag47.png', 'flag48.png', 'flag49.png', 'flag50.png', 'flag51.png', 'flag52.png', 'flag53.png', 'flag54.png', 'flag55.png', 'flag56.png', 'flag57.png', 'flag58.png', 'flag59.png', 'flag60.png', 'flag61.png', 'flag62.png', 'flag63.png', 'flag64.png', 'flag65.png', 'flag66.png', 'flag67.png', 'flag68.png', 'flag69.png', 'flag70.png', 'flag71.png', 'flag72.png', 'flag73.png', 'flag74.png', 'flag75.png', 'flag76.png', 'flag77.png', 'flag78.png', 'flag79.png', 'flag80.png', 'flag81.png', 'flag82.png', 'flag83.png', 'flag84.png', 'flag85.png', 'flag86.png', 'flag87.png', 'flag88.png', 'flag89.png', 'flag90.png', 'flag91.png', 'flag92.png', 'flag93.png', 'flag94.png', 'flag95.png', 'flag96.png', 'flag97.png', 'flag98.png', 'flag99.png', 'flag100.png', 'flag101.png', 'flag102.png', 'flag103.png', 'flag104.png', 'flag105.png', 'flag106.png', 'flag107.png', 'flag108.png', 'flag109.png', 'flag110.png', 'flag111.png', 'flag112.png', 'flag113.png', 'flag114.png', 'flag115.png', 'flag116.png', 'flag117.png', 'flag118.png', 'flag119.png', 'flag120.png', 'flag121.png', 'flag122.png', 'flag123.png', 'flag124.png', 'flag125.png', 'flag126.png', 'flag127.png', 'flag128.png', 'flag129.png', 'flag130.png', 'flag131.png', 'flag132.png', 'flag133.png', 'flag134.png', 'flag135.png', 'flag136.png', 'flag137.png', 'flag138.png', 'flag139.png', 'flag140.png', 'flag141.png', 'flag142.png', 'flag143.png', 'flag144.png', 'flag145.png', 'flag146.png', 'flag147.png', 'flag148.png', 'flag149.png', 'flag150.png', 'flag151.png', 'flag152.png', 'flag153.png', 'flag154.png', 'flag155.png', 'flag156.png', 'flag157.png', 'flag158.png', 'flag159.png', 'flag160.png', 'flag161.png', 'flag162.png', 'flag163.png', 'flag164.png', 'flag165.png', 'flag166.png', 'flag167.png', 'flag168.png', 'flag169.png', 'flag170.png', 'flag171.png', 'flag172.png', 'flag173.png', 'flag174.png', 'flag175.png', 'flag176.png', 'flag177.png', 'flag178.png', 'flag179.png', 'flag180.png', 'flag181.png', 'flag182.png', 'flag183.png', 'flag184.png', 'flag185.png', 'flag186.png', 'flag187.png']
hello = ["2b","c6","49","d4","7d","c7","e0","e1","43","25","3e","40","f6","e7","b6","d6","fa","d5","b0","cf","a4","6c","da","b8","b3","74","de","53","37","7e","aa","d8","24","23","30","67","5a","ff","b7","e4","be","2c","f9","2f","f4","3c","4c","ab","d3","ec","76","57","b9","b4","c2","e9","ed","3a","c0","4a","4f","21","fb","28","45","68","39","48","54","75","60","ae","bb","22","ba","77","a2","5d","cd","a7","fe","35","7a","d9","f5","f7","46","34","65","50","55","4b","c1","a8","ea","d1","7c","e3","52","2e","cb","fd","78","79","59","58","a3","3b","70","eb","ca","69","d2","ef","41","a9","c5","ce","e8","f3","5f","5c","64","6b","5e","29","dc","51","3f","f2","4e","fc","44","ee","47","cc","71","df","dd","f1","c4","db","33","a5","42","ac","c3","af","b5","6a","2a","3d","31","e5","27","a1","63","6e","56","a6","6f","c9","61","bc","36","e6","73","38","5b","d0","b1","62","f0","d7","2d","e2","c8","72","7b","66","6d","bf","b2","4d","f8","26","32","bd"]
from pwn import *

rgb_list_file = []
for i in lst_file:
    rgb_list_file.append(img_to_pixel(i))


viet = remote("35.229.44.203", 6666)
viet.sendlineafter(b'> ', b'1')
count = 0
while True:
    viet.recvuntil(b': ')
    b6666 = viet.recvuntil(b'\n',drop=True).decode()
    data = b64decode(b6666)
                    
    image = bytes_to_image(data)

    # Hiển thị ảnh
    image.save("chall.png")

    img = Image.open(r"chall.png")
    px = img.load()
    for i in range(5):
        getblock(25*i,25*(i+1),0,25,px,i)

    rgb_list_chall = []
    for f in chall_file:
        rgb_list_chall.append(img_to_pixel(f))
    result = ""
    for f in rgb_list_chall:
        max_compare = 0
        fi = 0
        for lst in range(len(rgb_list_file)):
            a = compare_images(rgb_list_file[lst],f)
            if a:
                fi = lst
                break
        result += (hello[fi])
    viet.sendlineafter(b'> ',(result).encode())
    print(count)
    count += 1

