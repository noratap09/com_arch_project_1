#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define NUMMEMORY 65536 /* maximum number of words in memory */
#define NUMREGS 8 /* number of machine registers */
#define MAXLINELENGTH 1000

typedef struct stateStruct {
    int pc;
    int mem[NUMMEMORY];
    int reg[NUMREGS];
    int numMemory;
} stateType;

void printState(stateType *);
int convertNum(int);

int main(int argc, char *argv[])
{
    char line[MAXLINELENGTH];
    stateType state;
    FILE *filePtr;

    if (argc != 2) {
	printf("error: usage: %s <machine-code file>\n", argv[0]);
	exit(1);
    }

    filePtr = fopen(argv[1], "r");
    if (filePtr == NULL) {
	printf("error: can't open file %s", argv[1]);
	perror("fopen");
	exit(1);
    }

    /* read in the entire machine-code file into memory */
    for (state.numMemory = 0; fgets(line, MAXLINELENGTH, filePtr) != NULL;
	state.numMemory++) {
		if (sscanf(line, "%d", state.mem+state.numMemory) != 1) {
	 	   printf("error in reading address %d\n", state.numMemory);
	 	   exit(1);
		}
		printf("memory[%d]=%d\n", state.numMemory, state.mem[state.numMemory]);
    }

	for(int i = 0; i < NUMREGS; i++){
		state.reg[i] = 0;
	}
	bool halt_flag = false;
	int count = 0;
	state.pc = 0;
	int opcode;
	int regA;
	int regB;
	int destReg;
	int offSet;
	while(halt_flag == false){
		printState(&state);
		opcode = ( (state.mem[state.pc] >> 22) & 7 ); /*((state.mem[state.pc] & 29360128) >> 22) (111 0*22) */
    	regA = ( (state.mem[state.pc] >> 19) & 7 ); /*((state.mem[state.pc] & 3670016) >> 19) (111 0*19) */
    	regB = ( (state.mem[state.pc] >> 16) & 7 ); /* ((state.mem[state.pc] & 458752) >> 16) (111 0*16) */ 
    	destReg = ( (state.mem[state.pc] >> 0) & 7 ); /* (state.mem[state.pc] & 7) (111) */
		offSet = convertNum(state.mem[state.pc] & 65535);
		if(opcode == 0){
			/*add*/	
			state.reg[destReg] = state.reg[regA] + state.reg[regB];
			state.pc++;
		}else if(opcode == 1){
			/*nand*/
			state.reg[destReg] = ~(state.reg[regA] & state.reg[regB]);
			state.pc++;
		}else if(opcode == 2){
			/*load word*/
			state.reg[regB] = state.mem[state.reg[regA] + offSet];
			state.pc++;
		}else if(opcode == 3){
			/*store word*/
			state.mem[state.reg[regA] + offSet] = state.reg[regB];
			state.pc++;
		}else if(opcode == 4){
			/*beq*/
			if(state.reg[regA] == state.reg[regB]){
				state.pc = (state.pc + 1 + offSet);
			}else{
				state.pc++;
			}
		}else if(opcode == 5){
			/*jalr*/
			if(state.reg[regA] == state.reg[regB]){
				state.reg[regB] = state.pc + 1;
				state.pc = state.pc + 1;
			}else{
				state.reg[regB] = state.pc + 1;
				state.pc = state.reg[regA];
			}
		}else if(opcode == 6){
			printf("\n\nCPU HALTED\n\n\n");
			halt_flag = true;
			state.pc++;
		}else if(opcode == 7){
			/*do nothing*/
			state.pc++;
		}
		count++;
		
	}
		printf("machine halted\n");
  		printf("total of %d instructions executed\n", count);
  		printf("final state of machine:\n");
  		printState(&state);
    return(0);
}

void printState(stateType *statePtr)
{
    int i;
    printf("\n@@@\nstate:\n");
    printf("\tpc %d\n", statePtr->pc);
    printf("\tmemory:\n");
	for (i=0; i<statePtr->numMemory; i++) {
	    printf("\t\tmem[ %d ] %d\n", i, statePtr->mem[i]);
	}
    printf("\tregisters:\n");
	for (i=0; i<NUMREGS; i++) {
	    printf("\t\treg[ %d ] %d\n", i, statePtr->reg[i]);
	}
    printf("end state\n");
}

int convertNum(int num){
 	/* convert a 16-bit number into a 32-bit integer */
 	if (num & (1<<15) ) {
 		num -= (1<<16);
 	}
 	return(num);
 } 
