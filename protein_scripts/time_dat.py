if (__name__ == "__main__"):
    import sys

def time(steps, per_step=1, path= "time.dat"):
    time_file = open(path,"w+")
    
    for i in range(1,steps,1):                          # Step size is always 1 since this is just used for number of lines.
        time_file.write("{0}\n".format(i*per_step))     # Default per_step = 1 ps
    time_file.close()                                   #

if (__name__ == "__main__"):
    steps = int(sys.argv[1])
    time(steps)
