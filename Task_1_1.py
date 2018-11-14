
## Mocking Bot - Task 1.1: Note Detection

#  Instructions
#  ------------
#
#  This file contains Main function and note_detect function. Main Function helps you to check your output
#  for practice audio files provided. Do not make any changes in the Main Function.
#  You have to complete only the note_detect function. You can add helper functions but make sure
#  that these functions are called from note_detect function. The final output should be returned
#  from the note_detect function.
#
#  Note: While evaluation we will use only the note_detect function. Hence the format of input, output
#  or returned arguments should be as per the given format.
#  
#  Recommended Python version is 2.7.
#  The submitted Python file must be 2.7 compatible as the evaluation will be done on Python 2.7.
#  
#  Warning: The error due to compatibility will not be entertained.
#  -------------


## Library initialisation

# Import Modules
# DO NOT import any library/module
# related to Audio Processing here
import numpy as np
import math
import wave
import os

# Teams can add helper functions
# Add all helper functions here

############################### Your Code Here ##############################################

def note_detect(audio_file):

	#   Instructions
	#   ------------
	#   Input   :   audio_file -- a single test audio_file as input argument
	#   Output  :   Detected_Note -- String corresponding to the Detected Note
	#   Example :   For Audio_1.wav file, Detected_Note = "A4"
	import struct
	FR = [ 27.50 , 30.87 , 16.35 , 18.35 , 20.60 , 21.83 , 24.50 ,
		  27.50*2 , 30.87*2 , 16.35*2 , 18.35*2 , 20.60*2 , 21.83*2 , 24.50*2 ,
		  27.50*4 , 30.87*4 , 16.35*4 , 18.35*4 , 20.60*4 , 21.83*4 , 24.50*4 ,
		  27.50*8 , 30.87*8 , 16.35*8 , 18.35*8 , 20.60*8 , 21.83*8 , 24.50*8 ,
		  27.50*16 , 30.87*16 , 16.35*16 , 18.35*16 , 20.60*16 , 21.83*16 , 24.50*16 ,
		  27.50*32 , 30.87*32 , 16.35*32 , 18.35*32 , 20.60*32 , 21.83*32 , 24.50*32 ,
		  27.50*64 , 30.87*64 , 16.35*64 , 18.35*64 , 20.60*64 , 21.83*64 , 24.50*64 ,
		  27.50*128 , 30.87*128 , 16.35*128 , 18.35*128 , 20.60*128 , 21.83*128 , 24.50*128 ,
		  27.50*256 , 30.87*256 , 16.35*256 , 18.35*256 , 20.60*256 , 21.83*256 , 24.50*256 ]

	NOTE = ['A0', 'B0', 'C0', 'D0', 'E0', 'F0', 'G0',
			 'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1',
			 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2',
			 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3',
			 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4',
			 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5',
			 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6',
			 'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7',
			 'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8']
	

	fl = audio_file.getnframes()
	frequency = audio_file.getframerate()
	sound = np.zeros(fl)
	for i in xrange(fl):
		data = audio_file.readframes(1)
		data = struct.unpack("<h",data)
		sound[i]=int(data[0])
	sound = np.divide(sound,float(2**15))

	win_size = 1

	i=0
	rms=[]
	while i<fl:
		j=0
		a=0
		while ((j<win_size) and (i<fl)) :
			a+=sound[i]*sound[i];
			j+=1
			i+=1
		rms.append(a);
	mx=max(rms)
	mn=min(rms)
	threshold=(mx+mn)/4
	# print threshold


	#	To store change from silence to sound and vice versa  	
	notes=[]
	#	Loop to detect silence 
	for i in range(len(rms)):
		if i==0:
			i+=1
		if rms[i]<threshold:
			rms[i]=0
		if rms[i]>threshold and rms[i-1]<threshold:
			notes.append(i)
		if rms[i]<threshold and rms[i-1]>threshold:
			notes.append(i)

	#	If no note is added 
	if len(notes)==0:
		notes.append(0)
		notes.append(len(rms)-2)
	if len(notes)==1:
		if notes[0]==0:
			notes.append(len(rms)-2)
		else:
			notes.append(notes[0])
			notes[0]=0


	dft = []
	dft = np.array(dft) # applying fourier transform function
	dft = np.fft.fft(sound[(int)(notes[0]*win_size):(int)(notes[-1]*win_size)])
	dft=np.argsort(dft)

	if(dft[0]>dft[-1] and dft[1]>dft[-1]):
		i_max = dft[-1]
	elif(dft[1]>dft[0] and dft[-1]>dft[0]):
		i_max = dft[0]
	else :	
		i_max = dft[1]
	
	# claculating frequency				
	
	freq = ((i_max*frequency)/((int)(notes[0]*win_size)-(int)(notes[-1])*win_size)*(-1))
	
	err=[]
	for i in FR:
		err.append(i-freq)
	x=0
	for i in xrange(len(err)):
		if abs(err[x])>abs(err[i]):
			x=i

	Detected_Note = NOTE[x]


	# Add your code here

	return Detected_Note


############################### Main Function ##############################################

if __name__ == "__main__":

	#   Instructions
	#   ------------
	#   Do not edit this function.

	# code for checking output for single audio file
	path = os.getcwd()
	
	file_name = path + "\Task_1.1_Audio_files\Audio_1.wav"
	audio_file = wave.open(file_name)

	Detected_Note = note_detect(audio_file)

	print("\n\tDetected Note = " + str(Detected_Note))

	# code for checking output for all audio files
	x = raw_input("\n\tWant to check output for all Audio Files - Y/N: ")
	
	if x == 'Y':

		Detected_Note_list = []

		file_count = len(os.listdir(path + "\Task_1.1_Audio_files"))

		for file_number in range(1, file_count):

			file_name = path + "\Task_1.1_Audio_files\Audio_"+str(file_number)+".wav"
			audio_file = wave.open(file_name)

			Detected_Note = note_detect(audio_file)
			
			Detected_Note_list.append(Detected_Note)

		print("\n\tDetected Notes = " + str(Detected_Note_list))
	
	
