import mem

GPIO1_MODE_REG=int("10000060",16)
GPIO2_MODE_REG=int("10000064",16)

GPIO_CTRL_BASE=int("10000600",16)

GPIO_DATA_BASE=int("10000620",16)

#define which bits should be set/cleared in registers to initialize its gpio function
gpio_setup_rules={}
gpio_setup_rules[43]= { GPIO2_MODE_REG : ( {3:0} , {2:1} ) }
gpio_setup_rules[42]= { GPIO2_MODE_REG : ( {5:0} , {4:1} ) }

gpio_setup_rules[11]= { GPIO1_MODE_REG : ( {0:0}, {1:0} ) }

gpio_setup_rules[12]= { GPIO1_MODE_REG : ( {9:0},{8:1} ) }
gpio_setup_rules[13]={ GPIO1_MODE_REG : ( {9:0},{8:1} ) }

gpio_setup_rules[19] ={ GPIO1_MODE_REG : ( {26:1}, {27:0} ) }
gpio_setup_rules[18]={ GPIO1_MODE_REG : ( {26:1}, {27:0} ) }
gpio_setup_rules[20] ={ GPIO1_MODE_REG : ( {26:1}, {27:0} ) }
gpio_setup_rules[21]={ GPIO1_MODE_REG : ( {26:1}, {27:0} ) }

gpio_setup_rules[3]={ GPIO1_MODE_REG : ( {7:0}, {6:1} ) }
gpio_setup_rules[2]={ GPIO1_MODE_REG : ( {7:0}, {6:1} ) }

gpio_setup_rules[0]= { GPIO1_MODE_REG : ( {7:0}, {6:1} ) }
gpio_setup_rules[1]  = { GPIO1_MODE_REG : ( {7:0}, {6:1} ) }

gpio_setup_rules[22]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
gpio_setup_rules[23]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
gpio_setup_rules[24]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
gpio_setup_rules[25]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
gpio_setup_rules[26]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
gpio_setup_rules[27]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
gpio_setup_rules[28]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }
gpio_setup_rules[29]= { GPIO1_MODE_REG : ( {11:0} , {10:1} ) }

#define which bit should be set to init periphial function
periphial_setup_rules={}

periphial_setup_rules['UART0']={GPIO1_MODE_REG : ( {9:0},{8:0} ) }



def setup(gpioNum, direction):
	#rist set gpio mux to gpio function if needed

	if(gpioNum in gpio_setup_rules):
		registerRules = gpio_setup_rules[gpioNum]
		for registerAddr, bitsValues in registerRules.iteritems():
			for bitNumValuePair in bitsValues:
				bitNum=bitNumValuePair.keys()[0]
				bitValue=bitNumValuePair[bitNum]
				mem.write_bit(registerAddr,bitNum,bitValue)
				print("initialization rule for GPIO"+str(gpioNum)+",bit: "+ str(bitNum)+",value: "+str(bitValue)," in register "+hex(registerAddr))

		#set gpio direction
		gpioCtrlReg = GPIO_CTRL_BASE + ((gpioNum/32)*4)
		bitNumber   = gpioNum % 32 if gpioNum>0 else 0

		mem.write_bit(gpioCtrlReg,bitNumber,direction)
		print("GPIO"+str(gpioNum)+" direction set to: "+str(direction))

def setupPeriphial(periphialName):
	if(periphialName in periphial_setup_rules):
		registerRules = periphial_setup_rules[periphialName]
		for registerAddr, bitsValues in registerRules.iteritems():
			for bitNumValuePair in bitsValues:
				bitNum=bitNumValuePair.keys()[0]
				bitValue=bitNumValuePair[bitNum]
				mem.write_bit(registerAddr,bitNum,bitValue)
				print("initialization rule for periphial: "+periphialName+", bit: "+ str(bitNum)+",value: "+str(bitValue)," in register "+hex(registerAddr))


def data(gpioNum, value=-1):
	gpioDataReg = GPIO_DATA_BASE + ((gpioNum/32)*4)
	bitNumber   = gpioNum % 32 if gpioNum>0 else 0

	if(value != -1):
		mem.write_bit(gpioDataReg,bitNumber,value)
	else:
		value=mem.read_bit(gpioDataReg,bitNumber)

	return value
