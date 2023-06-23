""" 
int s
int nbytes;

struct socket_can addr;
struct can_frame frame;

frame.can_ID = 0x123;
frame.can_dlc = 2
frame.data[0] = 0x11;
frame.data[1] = 0x22;

nbytes = write(s, &frame, sizeof(struct can_frame));
print("Wrote %d bytes\n", nbytes):

return 0;

"""