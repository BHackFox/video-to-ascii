import sys
from PIL import Image
import cv2
import os, time
import argparse


def main(args):
    if (args.list):
        arr = returnCameraIndexes()
        print("\nList of all cameras (by index):\n")
        print('\n'.join(arr))
    elif(type(args.capture) == int and not args.list and not args.file):
        arr = returnCameraIndexes()
        if(str(args.capture) in arr):
            captureVideo(args.capture)
        else:
            print("Camera Not Found")
    elif(type(args.file) == str and not args.list and not args.capture):
        render_video(args.file)



def render_video(vid):
    cv2.waitKey(10)
    vidcap = cv2.VideoCapture(vid)
    success,image = vidcap.read()
    fps = vidcap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    total = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video: {vid}\tFrame: {total}\tFPS: {fps}\n\n")
    count = 0

    list_ascii_image = []
    while success:
        sys.stdout.write('\r')
        sys.stdout.write("Reading frame %s of %s   \t%s%%" %(count+1,total,int(((count+1)/total)*100)))
        sys.stdout.flush()
        framejpg = "data/frame%d.jpg" % count
        list_ascii_image.append(ascii_generator(Image.fromarray(image)))
        success,image = vidcap.read()
        count += 1

    for i in list_ascii_image:
        print_function(i,fps)



def ascii_generator(img):

    width, height = img.size
    aspect_ratio = height/width
    new_width = 120
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    img = img.convert('L')

    pixels = img.getdata()

    chars = list('$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`". ') #["B","S","#","&","@","$","%","*","!",":",".","/","\\","-"," "," "," "," "," "]
    new_pixels = [chars[pixel//40] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)

    return ascii_image


def captureVideo(camera_index):
    vid = cv2.VideoCapture(camera_index)
    block = True
    while block:
        try:
            ret, frame = vid.read()
            ascii_image = ascii_generator(Image.fromarray(frame))
            print_function(ascii_image,25)

        except KeyboardInterrupt as e:
            print("\n\nUser Exit...")
            block = False
    vid.release()
    print()


def print_function(i,fps):
    os.system("clear")
    print(i)
    time.sleep(1/fps)


def returnCameraIndexes():
    i = 0
    camera_list = []
    k = True
    while k:
        cam = cv2.VideoCapture(i)
        if not cam.read()[0]:
            print("\n\n")
            k = False
        else:
            camera_list.append(str(i))
        cam.release()
        i += 1
    if(len(camera_list)==0): return ["No Camera Found"]
    return camera_list

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='Genarate ascii video from MP4 or video capture')
    my_parser.add_argument('-f','--file',action='store',help='Choose a mp4 file',type=str,required=False)
    my_parser.add_argument('-c','--capture',action='store',help='Capture from camera',type=int,required=False)
    my_parser.add_argument('-l','--list',action='store_true',help='List of all camera interfaces')
    args = my_parser.parse_args()
    main(args)
