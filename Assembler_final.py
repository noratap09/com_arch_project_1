import sys
if(len(sys.argv) != 3):
	print("Input not match")
	exit(1)

def two_complement(num):
    if(num > 32767 or num < -32768):
        print("Out of range")
        exit(1)

    if(num<0):
        return bin((num-1)*-1)[2:].zfill(16).replace("0","_").replace("1","0").replace("_","1")
    else:
        return bin(num)[2:].zfill(16)

file_name = sys.argv[1]
print(file_name)
file = open(file_name,"r") 

ass_code_line = list()
symbolic_address = dict()
instructions_set = {"add":["000","R"],
                    "nand":["001","R"],
                    "lw":["010","I"],
                    "sw":["011","I"],
                    "beq":["100","I"],
                    "jalr":["101","J"],
                    "halt":["110","O"],
                    "noop":["111","O"]} 
	
count=0
for line in file:
    ass_code = line.split()
    if((line.split()[0][0]).isdigit()):
        print("First charactor is number")
        exit(1)
    if(len(line.split()[0]) > 6):
        print("Out of length label")
        exit(1)
    if(not(line.split()[0] in instructions_set.keys()) and line.split()[0] != ".fill"):
        if(ass_code[0] in symbolic_address.keys()):
            print("Used same Label", ass_code[0])
            exit(1)
        symbolic_address[line.split()[0]] = count
        ass_code.pop(0)
    ass_code_line.append(ass_code)
    count=count+1

mac_code_line = list()
count = 0
try:
	for line in ass_code_line:
		if(line[0] in instructions_set):
			instructions_type = instructions_set[line[0]][1]
			if(instructions_type=="R"):
				opcode = instructions_set[line[0]][0]
				if(int(line[1]) >= 0 and int(line[1]) <= 7 and int(line[2]) >= 0 and int(line[2]) <= 7 and int(line[3]) >= 0 and int(line[3]) <= 7):
					regA = bin(int(line[1]))[2:].zfill(3)
					regB = bin(int(line[2]))[2:].zfill(3)
					desReg = bin(int(line[3]))[2:].zfill(3)
				_ = "".zfill(13)
				mac_code = "0b"+opcode+regA+regB+_+desReg
				mac_code_line.append(int(mac_code,2))
			elif(instructions_type=="I"):
				if(line[0] == "beq"):
					opcode = instructions_set[line[0]][0]
					if(int(line[1]) >= 0 and int(line[1]) <= 7 and int(line[2]) >= 0 and int(line[2]) <= 7):
						regA = bin(int(line[1]))[2:].zfill(3)
						regB = bin(int(line[2]))[2:].zfill(3)
					if(line[3] in symbolic_address):
						if(int(symbolic_address[line[3]]) > count):
							offset = symbolic_address[line[3]]-count-1
						else:
							offset = symbolic_address[line[3]]-count+1
					else:
						try:
							offset = int(line[3])
						except:
							print("Undefined Label")
							exit(1)
					offset = two_complement(offset)
					mac_code = "0b"+opcode+regA+regB+offset
					mac_code_line.append(int(mac_code,2))
				else:
					opcode = instructions_set[line[0]][0]
					if(int(line[1]) >= 0 and int(line[1]) <= 7 and int(line[2]) >= 0 and int(line[2]) <= 7):
						regA = bin(int(line[1]))[2:].zfill(3)
						regB = bin(int(line[2]))[2:].zfill(3)
					if(line[3] in symbolic_address):
						offset = symbolic_address[line[3]]
					else:
						try:
							offset = int(line[3])
						except:
							print("Undefined Label")
							exit(1)
					offset = two_complement(offset)
					mac_code = "0b"+opcode+regA+regB+offset
					mac_code_line.append(int(mac_code,2))
			elif(instructions_type=="J"):
				opcode = instructions_set[line[0]][0]
				if(int(line[1]) >= 0 and int(line[1]) <= 7 and int(line[2]) >= 0 and int(line[2]) <= 7):
					regA = bin(int(line[1]))[2:].zfill(3)
					regB = bin(int(line[2]))[2:].zfill(3)
				_ = "".zfill(16)
				mac_code = "0b"+opcode+regA+regB+_
				mac_code_line.append(int(mac_code,2))
			elif(instructions_type=="O"):
				opcode = instructions_set[line[0]][0]
				_ = "".zfill(22)
				mac_code = "0b"+opcode+_
				mac_code_line.append(int(mac_code,2))
		elif(line[0]==".fill"):
			if(line[1] in symbolic_address):
				mac_code_line.append(symbolic_address[line[1]])
			else:
				try:
					mac_code_line.append(int(line[1]))
				except:
					print("Undefined Label")
					exit(1)			
		else:
			print("Out of opcode")
			exit(1)
		count = count+1
except:
	print("Assembly Syntax Error")
	exit(1)

file_out = sys.argv[2]

with open(file_out, 'w') as f:
    for item in mac_code_line:
        f.write("%s\n" % item)

print("Success !!!")
"""
for i in ass_code_line:
    print(i)
print(symbolic_address)
print(bin(1)[2:].zfill(3).replace("0","_").replace("1","0").replace("_","1"))
print(int("0b1001",2))
"""