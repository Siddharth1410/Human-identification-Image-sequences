import cv2
def parse_frame_name(frame_filename):
    length = len(frame_filename)
    sequence_name = frame_filename[0:length-8]
    frame_string = frame_filename[(length-7):(length-4)]
    frame = int(frame_string)
    return sequence_name, frame

def get_other_image(image_path):
    img_current, frame_curr = parse_frame_name(image_path)
    if (frame_curr < 10):
        frame_prev=frame_curr+10
        frame_next=frame_curr+20
    elif (frame_curr > 114):
        frame_prev=frame_curr-10
        frame_next=frame_curr-20
    else:
        frame_prev=frame_curr-10
        frame_next=frame_curr+10
    img_prev=make_frame_name(img_current,frame_prev)
    img_next=make_frame_name(img_current,frame_next)
    return img_prev,img_next 

def find_bounding_box(image_path):
    
    coord = [0,0,0,0]
    result = [0,0,0,0]
    img_curr=cv2.imread(image_path)
    img_curr_gray=cv2.cvtColor(img_curr,cv2.COLOR_BGR2GRAY)
    
    img_prev_path,img_next_path=get_other_image(image_path)
    
    img_prev=cv2.imread(img_prev_path)
    img_prev_gray=cv2.cvtColor(img_prev,cv2.COLOR_BGR2GRAY)
    
    img_next=cv2.imread(img_next_path)
    img_next_gray=cv2.cvtColor(img_next,cv2.COLOR_BGR2GRAY)



    img_diff= cv2.absdiff(img_curr_gray,img_prev_gray)
    img_diff2= cv2.absdiff(img_curr_gray,img_next_gray)
    img_bin=cv2.min(img_diff,img_diff2)
    
    img_thr=cv2.threshold(img_bin,27,255,cv2.THRESH_BINARY)[1]
    img_thr2=cv2.dilate(img_thr,None,iterations=2)
    
    _, cons, _=cv2.findContours(img_thr2.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    
    cArea = [cv2.contourArea(i) for i in cons]
    max_area = max(cArea)
    
    if max_area >890:
        (coord[0],coord[1],coord[2],coord[3]) =cv2.boundingRect(cons[cArea.index(max_area)])
        cv2.rectangle(img_curr,(coord[0],coord[2]),(coord[0]+coord[2],coord[1]+coord[3]),(0,255,255),2)

    cv2.imshow('difference of frames',img_curr)
    if cv2.waitKey(0) % 0xFF == ord('q'):
        cv2.destroyAllWindows()
        cv2.waitKey(1)
    result[0]=coord[1]
    result[1]=coord[1]+coord[3]
    result[2]=coord[0]
    result[3]=coord[0]+coord[2]
    return result
    
def person_speed(image1,image2):
    img1_coord=find_bounding_box(image1)
    img2_coord=find_bounding_box(image2)
    img1_hor_cor=(img1_coord[0]-img1_coord[1])/2
    img1_ver_cor=(img1_coord[3]-img1_coord[2])/2
    img2_hor_cor=(img2_coord[0]-img2_coord[1])/2
    img2_ver_cor=(img2_coord[3]-img2_coord[2])/2
    img1_frame,img1_num=parse_frame_name(image1)
    img2_frame,img2_num=parse_frame_name(image2)
    tot_frames=img1_num-img2_num
    hor_speed=(img1_hor_cor-img2_hor_cor)/tot_frames
    ver_speed=(img1_ver_cor-img2_ver_cor)/tot_frames
    velocity=[hor_speed,ver_speed]
    return velocity
    

def make_frame_name(sequence_name, frame):
    if (frame < 10):
        frame_filename = sequence_name + '000' + str(frame) + '.tif'
    elif (frame < 100):
        frame_filename = sequence_name + '00' + str(frame) + '.tif' 
    else:
        frame_filename = sequence_name + '0' + str(frame) + '.tif'
    return frame_filename


def main():
	find_bounding_box('walkstraight/frame0001.tif')

if __name__=="__main__":
	main()


def person_present(image_path):
    coord = [0,0,0,0]
    img_curr=cv2.imread(image_path)
    img_curr_gray=cv2.cvtColor(img_curr,cv2.COLOR_BGR2GRAY)

    img_prev_path,img_next_path=get_other_image(image_path)
    
    img_prev=cv2.imread(img_prev_path)
    img_prev_gray=cv2.cvtColor(img_prev,cv2.COLOR_BGR2GRAY)
    
    img_next=cv2.imread(img_next_path)
    img_next_gray=cv2.cvtColor(img_next,cv2.COLOR_BGR2GRAY)
    
    img_diff= cv2.absdiff(img_curr_gray,img_prev_gray)
    img_diff2= cv2.absdiff(img_curr_gray,img_next_gray)
    
    img_bin=cv2.min(img_diff,img_diff2)
    
    img_thr=cv2.threshold(img_bin,27,255,cv2.THRESH_BINARY)[1]
    img_thr2=cv2.dilate(img_thr,None,iterations=2)
    
    person_exists=0
    
    _, cons, _=cv2.findContours(img_thr2.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cArea = [cv2.contourArea(i) for i in cons]
    max_area = max(cArea)
    
    if max_area >890:
        person_exists=1
        
    return person_exists



