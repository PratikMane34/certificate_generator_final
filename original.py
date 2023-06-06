import os
import cv2

list_of_names = []


def delete_old_data():
   for i in os.listdir("./sample_data/generate_certificates/"):
      os.remove("./sample_data/generate_certificates/{}".format(i))


def cleanup_data():
   with open('name-data.txt') as f:
      for line in f:
          list_of_names.append(line.strip())


def generate_certificates():

   for index, name in enumerate(list_of_names):
      text = name.strip()#.encode("utf-8")
      text1 = name.encode("utf-8")
      print(f'text :  {text} and type {type(text)} and name : {name} name type {type(name)} encoded name {name.encode("utf-8")} decoded name : {text1.decode("utf-8")}')
      
      certificate_template_image = cv2.imread("certificate-template.jpg")
      cv2.putText(certificate_template_image,text1.decode("utf-8"), (659,455), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 150), 5, cv2.LINE_AA)
      cv2.imwrite("./sample_data/generate_certificates/{}.jpg".format(name.strip()), certificate_template_image)
      print("Processing {} / {}".format(index + 1,len(list_of_names)))
      
def main():
   delete_old_data()
   cleanup_data()
   generate_certificates()



if __name__ == '__main__':
   main()