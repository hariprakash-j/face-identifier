import face_recognition
from PIL import Image, ImageDraw
from os import listdir

#input faces with names dir
faces_file = "./faces/"
#processing images
proces_images = "./input/"
#output dirctory
output_dir = "./output/"

class FaceRecogniton():
    def __init__(self):
        self.face_encodings = []
        self.face_names = []

        _files = listdir(faces_file)

        for i in _files:
            temp = face_recognition.load_image_file(faces_file + i)
            self.face_encodings.append(face_recognition.face_encodings(temp)[0])

        for i in _files:
            self.face_names.append(i.split(".")[0])

        self.id_loading = []
        self.id_images_location = []
        self.id_images_encoding = []

        self.input_files = listdir(proces_images)

        for i in self.input_files:
            self.id_loading.append(face_recognition.load_image_file(proces_images + i))

        for i in self.id_loading:
            self.id_images_location.append(face_recognition.face_locations(i))

        for i,j in zip(self.id_loading,self.id_images_location):
            self.id_images_encoding.append(face_recognition.face_encodings(i, j))

        #convert images to PIL format
        self.pil_images = []
        for i in self.id_loading:
            self.pil_images.append(Image.fromarray(i))

        #creating the imagedraw instance
        self.draws = []
        for i in self.pil_images:
            self.draws.append(ImageDraw.Draw(i))

    def id_faces(self):
        for face_encodings, face_locations, draw, pil_image, image_file_name in zip(self.id_images_encoding, self.id_images_location, self.draws, self.pil_images, self.input_files):
            for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

                #tolerance is subjective the recomended value is 0.6, change it if you are having problems.
                matches = face_recognition.compare_faces(self.face_encodings, face_encoding, tolerance=0.49)

                name = "Unknown Person"

                # If match
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.face_names[first_match_index]

                # Draw box
                draw.rectangle(((left, top), (right, bottom)), outline=(255,255,0))

                # Draw label
                text_width, text_height = draw.textsize(name)
                draw.rectangle(((left,bottom - text_height - 10), (right, bottom)), fill=(255,255,0), outline=(255,255,0))
                draw.text((left + 6, bottom - text_height - 5), name, fill=(0,0,0))
            # Saveing and showing image
            pil_image.save(output_dir + image_file_name.split('.')[0] + '_output.'+ image_file_name.split('.')[1] )
            pil_image.show()

facesobj = FaceRecogniton()
facesobj.id_faces()
