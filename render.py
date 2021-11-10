import sys
from PIL import Image
import cv2
import os, time
import argparse

def render_video(vid):
    cv2.waitKey(10)
    vidcap = cv2.VideoCapture(vid)
    success,image = vidcap.read()
    fps = vidcap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    total = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video: {vid}\tFrame: {total}\tFPS: {fps}\n\n")
    count = 0
    with open("ascii_image.txt", "w") as f:
        f.write(f"{fps} {vid}\n")
    if not os.path.exists('data'):
        os.system("mkdir data")
    os.system("rm data/*.jpg")
    while success:
        sys.stdout.write('\r')
        sys.stdout.write("Reading frame %s of %s   \t%s%%" %(count+1,total,int(((count+1)/total)*100)))
        sys.stdout.flush()
        framejpg = "data/frame%d.jpg" % count
        cv2.imwrite(framejpg, image)
        success,image = vidcap.read()
        ascii_generator(framejpg)
        count += 1



def ascii_generator(image_path):
    img = Image.open(image_path)

    width, height = img.size
    aspect_ratio = height/width
    new_width = 120
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    img = img.convert('L')

    pixels = img.getdata()

    chars = ["B","S","#","&","@","$","%","*","!",":",".","/","\\","-"]
    new_pixels = [chars[pixel//20] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)

    with open("ascii_image.txt", "a") as f:
        f.write(ascii_image+"\n\n")


def print_ascii():
    op = open("ascii_image.txt").readlines()
    display = []
    time.sleep(3)
    os.system("clear")
    fps = float(op[0].strip().split()[0])
    timing = 1 / fps
    for i in range(len(op)):
        display.append(op[i])
        if op[i] == "\n" or i == len(op)-1:
            os.system("clear")
            print("".join(display))
            time.sleep(timing)
            display = []

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='Genarate ascii video from MP4')
    my_parser.add_argument('-f','--file',action='store',help='Choose a file',type=str,required=True)
    args = my_parser.parse_args()
    render_video(args.file)
    print_ascii()
