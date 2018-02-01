#######################################################
###########
#AUTHOR(S): Kelsey Herndon
#EMAIL: keh0023@uah.edu
#ORGANIZATION: UAH
#CREATION DATE: March 2017
#LAST MOD DATE: March 2017
#PURPOSE: Calculate processing time for reclassifying image as boolean
#DEPENDENCIES: numpy, matplotlib, timeit
###########

##import modules
import numpy as np
import matplotlib.pyplot as plt
import timeit

##identify file
infile = r'/Users/keherndo/Desktop/UAH_courses/Spring_17/ESS 508/huntsville.asc'

##open file
f = open(infile, 'r')
lines = f.readlines()

#Get the number of columns (x)
x_dim = len(lines[7].split(' ')[:-1]) 

#Get the number of rows (y)
y_dim = len(lines[6:])

#storing the data as a numpy array
img = np.zeros([y_dim, x_dim])

#taking out the header in the file
lines = lines[6:]

##looping through the data to get the x and y dimensions
for i in range(img.shape[0]): 
    row = lines[i].split(' ')[:-1]
    for j in range(img.shape[1]):
        img[i,j] = row[j]

##get start time        
tic1=timeit.default_timer()

#creating a boolean image where values > than 150 are TRUE and < than 150 are FALSE         
w = np.where(bool,img>150,img<150) 

##get end time
toc1 =timeit.default_timer()

##calculate end time - start time to get total processing time
print 'Image 1 has completed processing. It took', toc1-tic1 , 'seconds.'

plt.imshow(w,cmap='gray')
plt.show()

infile = r'/Users/keherndo/Desktop/UAH_courses/Spring_17/ESS 508/huntsville.asc'
f = open(infile, 'r')
lines = f.readlines()

#To get the x dimensions (aka number of columns)
x_dim = len(lines[7].split(' ')[:-1]) 

#To get the y dimensions (aka number of rows)
y_dim = len(lines[6:])

imge = np.zeros([y_dim, x_dim])

lines = lines[6:]

for i in range(imge.shape[0]): 
    row = lines[i].split(' ')[:-1]
    for j in range(imge.shape[1]):
        imge[i,j] = row[j]

##get start time        
tic2=timeit.default_timer()
        
for x in range(imge.shape[0]):
    for y in range(imge.shape[1]):
        if imge [x,y] >100: 
            imge [x,y] = 1
        else:
            imge[x,y] = 0

##get end time
toc2=timeit.default_timer()

##calculate end time - start time to get total processing time
print 'Image 2 has completed processing. It took',toc2-tic2,'seconds.'

plt.imshow(imge,cmap='gray')
plt.show()
