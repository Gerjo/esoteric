#include <stdio.h>
#include <math.h>
#include <stdlib.h>


void shape(int radius) {
	
	int w = radius * 2 - 1;
	
	for(int i = 0; i < w; ++i) {
		
		int h = abs(radius - i - 1);

		//h += (i & 1);

		int o = (h & 1);

		for(int j = 0; j < h; ++j) {
			printf(" ");
		}

		for(int j = h; j < w-h + o; ++j) {
			printf("*");
		}
		
		printf("\n");
		//break;	
	}	
}

int main() {
	
	shape(9); 
	
	
}