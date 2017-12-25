def f(x):
    
    return {
        "a" : lambda x: x,
        "b" : lambda x: x+1,
        "c" : lambda x: x+1
    }["b"](x)
#print(f(5))


def g(l,x):
    
    return {
        "a" : lambda x: x,
        "b" : lambda x: x+1,
        "c" : lambda x: x+2
    }.get(l,lambda x: x+4)(x)
    
print(g("b",3))


def position_under_constant_linear_acceleration( time, *args ):
	print("point 2")
	if len(args) == 3:
		if isinstance(args[0],(int, float)):
			
			# Define Variables
			position     = float(args[0])
			velocity     = float(args[1])
			acceleration = float(args[2])
			
			return position + velocity*time + (acceleration * time**2) / 2.0
			
		elif isinstance(args[0], (list, tuple)) and not isinstance(args[0], basestring):
			
			# Check Length and Composition
			same_length          = len(args[0]) == len(args[1]) and len(args[1]) == len(args[2])
			numeric_position     = all(isinstance(x, (int, float)) for x in args[0])
			numeric_velocity     = all(isinstance(x, (int, float)) for x in args[1])
			numeric_acceleration = all(isinstance(x, (int, float)) for x in args[2])
			acceptable_vars      = same_length and numeric_position and numeric_velocity and numeric_acceleration
			
			new_position = []
			if acceptable_vars:
				for i in range(0,len(args[0])):
					# Define Variables
					position     = float(args[0][i])
					velocity     = float(args[1][i])
					acceleration = float(args[2][i])
					
					new_position.append(position + velocity*time + (acceleration * time**2) / 2.0)
					
			else: print("error  bad inputs 1")	# ToDo Replace with real errors
			
			return new_position
			
		else: print("error bad inputs 2")	# ToDo Replace with real errors
	else: 
		print("Invalid Input Length:")
		print(len(args))
		print("Please Fix.")
ELECTRON_CHARGE = 1.60217662e-19
PI = 3.1415
def M_squared(m,n,L):
    return (((8*ELECTRON_CHARGE*L)/(PI**2))**2)*((m**2 * n**2)/((n**2 - m**2)**4))

#print("m={0}, n={1}, M^2={2}".format(4,5,M_squared(4,5,1.225e-9)))
#print("m={0}, n={1}, M^2={2}".format(4,7,M_squared(4,7,1.225e-9)))
#print("m={0}, n={1}, M^2={2}".format(3,6,M_squared(3,6,1.225e-9)))

PLANCKS_CONSTANT = 6.626070040e-34
ELECTRON_MASS = 9.10938356e-31
SPEED_OF_LIGHT = 299792458
def quantum_length(n,wavelength):
    return (PLANCKS_CONSTANT*wavelength*((n+1)**2 - n**2)*((SPEED_OF_LIGHT*8*ELECTRON_MASS)**-1))**(0.5)

def M(m,n,L):
    return ((-1)**((m-n+1)/2))* (8*ELECTRON_CHARGE*L/(PI**2)) * ((m * n)/((n**2 - m**2)**2))

#print("Cy1 Homo=3 Lumo=4 L={0} M={1}".format(quantum_length(3,450e-9),M(3,4,quantum_length(3,450e-9))**2))
#print("Cy3 Homo=4 Lumo=5 L={0} M={1}".format(quantum_length(4,550e-9),M(4,5,quantum_length(4,550e-9))**2))
#print("Cy5 Homo=5 Lumo=6 L={0} M={1}".format(quantum_length(5,649e-9),M(5,6,quantum_length(5,649e-9))**2))
#print("Cy7 Homo=6 Lumo=7 L={0} M={1}".format(quantum_length(6,749e-9),M(6,7,quantum_length(6,749e-9))**2))

#print("Cy1 Homo=3 Lumo=4 L={0} M^2_N={1}".format(quantum_length(3,450e-9),M_squared(3,4,quantum_length(3,450e-9))/M_squared(3,4,quantum_length(3,450e-9))))
#print("Cy3 Homo=4 Lumo=5 L={0} M^2_N={1}".format(quantum_length(4,550e-9),M_squared(4,5,quantum_length(4,550e-9))/M_squared(3,4,quantum_length(3,450e-9))))
#print("Cy5 Homo=5 Lumo=6 L={0} M^2_N={1}".format(quantum_length(5,649e-9),M_squared(5,6,quantum_length(5,649e-9))/M_squared(3,4,quantum_length(3,450e-9))))
#print("Cy7 Homo=6 Lumo=7 L={0} M^2_N={1}".format(quantum_length(6,749e-9),M_squared(6,7,quantum_length(6,749e-9))/M_squared(3,4,quantum_length(3,450e-9))))
#print("n={0}, wavelength={1}, quantum length={2}".format(3,450e-9,))
#print("n={0}, wavelength={1}, quantum length={2}".format(4,550e-9,))
#print("n={0}, wavelength={1}, quantum length={2}".format(5,649e-9,))
#print("n={0}, wavelength={1}, quantum length={2}".format(6,749e-9,))

#a = position_under_constant_linear_acceleration(1,2,3,time=10)
#print(a)
