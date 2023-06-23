import math

right_start = [661489.37,1509517.50]
right_stop = [661489.88,1509522.50]


ref_start = [661485.7114550700,1509583.749]
ref_stop =  [661485.3214350120,1509685.06490994]


left_start = [661377.31,1509667.16]
left_stop = [661376.99,1509653.56]


# dy = left_stop[1] - left_start[1]
# dx = left_stop[0] - left_start[0]
# d = math.sqrt( (dx**2)+(dy**2) )
# slope1 = dy/dx
# c = left_stop[1]-(slope1*left_stop[0])
# al = slope1
# bl = -1
# cl = c
# print(al,',',bl,',',cl)


dy = ref_stop[1] - ref_start[1]
dx = ref_stop[0] - ref_start[0]
d = math.sqrt( (dx**2)+(dy**2) )
slope1 = dy/dx
c = ref_stop[1]-(slope1*ref_stop[0])
a = slope1
b = -1
c = c
print(a,',',b,',',c)


# dy = right_stop[1] - right_start[1]
# dx = right_stop[0] - right_start[0]
# d = math.sqrt( (dx**2)+(dy**2) )
# slope1 = dy/dx
# c = right_stop[1]-(slope1*right_stop[0])
# ar = slope1
# br = -1
# cr = c
# print(ar,',',br,',',cr)
