#importing the required libraries  
import cv2  
import numpy as np  
import types  

# shifting image 
def shift_image(img1):
   
   
    rows,cols,c=img1.shape
    trastation_matrix=np.float32([[1,0,sx],[0,1,0]])
    img_tr=cv2.warpAffine(img1,trastation_matrix,(cols,rows))
    cv2.imwrite('shifted_image_1.jpg',img_tr)
    
    edge=[]
    for i in range(rows):
        edge.append(img_tr[i][sx])
    for i in range (rows):
        for j in range(sx):
            img_tr[i][j]= edge[i]
    cv2.imwrite('shifted_image_2.jpg',img_tr)
    return img_tr
                
    
# converting to binary format
def to_bin(msg):  
    if type(msg) == str:  
        return ''.join([format(ord(i), "08b") for i in msg])  
    elif type(msg) == bytes or type(msg) == np.ndarray:  
        return [format(i, "08b") for i in msg]  
    elif type(msg) == int or type(msg) == np.uint8:  
        return format(msg, "08b")  
    else:  
        raise TypeError("Input type not supported")  
  
# hide the secret message into the image  
def hide_data(img, secret_msg):  
    
    # maximum bytes to encode  
    nBytes = img.shape[0] * sx * 3 // 8  
    print("Maximum Bytes for encoding:", nBytes)  
    # checking size of infrmation with space in image
    if len(secret_msg) > nBytes:  
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data!!")  
    # adding delimeter
    secret_msg += '$$$$$'        
    dataIndex = 0  
    # converting the input data to binary format using the to_bin() function  
    bin_secret_msg = to_bin(secret_msg)  
  
    # finding the length of data that requires to be hidden  
    datalen = len(bin_secret_msg) 
    for ROW in img:  
        i=0
        for pixel in ROW:  
           
            if i<sx: 
                # getting binary of pixel
                r, g, b = to_bin(pixel)  
                # hiding the data into 
                if dataIndex < datalen:  
                    # LSB of Red pixel  
                    pixel[0] = int(r[:-1] + bin_secret_msg[dataIndex], 2)  
                    dataIndex += 1  
                if dataIndex < datalen:  
                    # LSB of Green pixel  
                    pixel[1] = int(g[:-1] + bin_secret_msg[dataIndex], 2)  
                    dataIndex += 1  
                if dataIndex < datalen:  
                    # LSB of Blue pixel  
                    pixel[2] = int(b[:-1] + bin_secret_msg[dataIndex], 2)  
                    dataIndex += 1  
                # if data is encoded then break 
                if dataIndex >= datalen:  
                    break  
                i=i+1
      
    return img  
  
def get_data(img): 
   
    bin_data = ""
    
     
    for ROW in img:  
        i=0
        for pixel in ROW:  
            if i<sx:
                # converting the Red, Green, Blue value into binary 
                r, g, b = to_bin(pixel)  
                # data extraction from the LSB of red, green, blue pixel  
                bin_data += r[-1]  
                
                bin_data += g[-1]  
                
                bin_data += b[-1]  
                i=i+1
    # spliting binary data by 8-Bits  
    all_bytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]  
    # converting bytes to character  
    decoded_Data = ""  
    for bytes in all_bytes:  
        decoded_Data += chr(int(bytes, 2))  
        # checking if we have reached the delimiter '$$$$$"  
        if decoded_Data[-5:] == '$$$$$':  
            break  
     
    # returning data without delimeter
    return decoded_Data[:-5]  
  
# defining function to encode data into Image  
def encode_text():  
  
    img_name = input("Enter image name (with extension): ")  
    # reading the input image  
    img1 = cv2.imread(img_name)  
    # printing the details of the image 
    '''h,w,c=img1.shape 
    print("The shape of the image is: \n") # checking the image shape to calculate the number of bytes in it  
    print("height - ",h)
    print("width - ",w)
    '''
    img=shift_image(img1)
  

  
    data = input("Enter data to be encoded: ")  
    if (len(data) == 0):  
        raise ValueError('Data is Empty')  
      
    file_name = input("Enter the name of the new encoded image (with extension): ")  
    # calling the hide_data() function to hide the secret message into the selected image  
    encodedImage = hide_data(img, data)  
    cv2.imwrite(file_name, encodedImage)  
  
# defining the function to decode the data in the image  
def decodeText():  
   
    # reading the image containing the hidden image  
    img_name = input("Enter the name of the Steganographic image (with extension): ")  
    img = cv2.imread(img_name)  
    
  
    text = get_data(img)  
    return text  
if __name__=='__main__':
    n = int(input("Image Steganography \n1. Encode the data \n2. Decode the data \nSelect the option: "))  
    if (n == 1):  
        print("\nEncoding...") 
        sx=int(input("Enter shift value :"))   
        encode_text()  
  
    elif (n == 2):  
        print("\nDecoding...")  
        sx=int(input("Enter shift value :"))  
        print("Decoded message is " , decodeText())  
      
    else:  
        raise Exception("Inserted value is incorrect!")  

