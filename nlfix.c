#include <stdio.h>
#include <string.h>

/// Read from stdin and convert  mac and windows newlines into unix.
///
/// compile with: gcc nlfix.c -o nlfix
/// example: echo -e "hello\rfoo" | nlfix
/// example: cat myfile.txt | nlfix | tee out.txt

typedef struct {
	int win;
	int unix;
	int mac;
} Stats;

void analyse(FILE* file, int doOut, Stats* stats);
void print_stats(Stats* stats);

int main(int argc, char** argv) {

	int doStats = 0;
	
	for(int i = 1; i < argc; ++i) {
		if(strcmp(argv[i], "-s") == 0) {
			doStats = i;			
			break;
		}
	}
	
	Stats stats = {0, 0, 0};
	
	if(argc > 2 || (!doStats && argc > 1)) {
		
		for(int i = 1; i < argc; ++i) {
			if(i != doStats) {
				FILE* file = fopen(argv[i], "r");
				
				if(file) {
					analyse(file, !doStats, &stats);
					
					fclose(file);
				} else {
					fprintf(stderr, "Error: Could not open '%s' for reading.\n", argv[i]);
				}
			}
		}
		
		// files.
	} else {
		analyse(stdin, !doStats, &stats);
	}
	
	if(doStats) {
		print_stats(&stats);
	}
	
	return 0;
}

void analyse(FILE* file, int doOut, Stats* stats) {
	char buffer[128];

	char last = 0;
	do {
		int retrieved = fread(buffer, 1, sizeof buffer, file);
	
		for(int i = 0; i < retrieved; ++i) {
			char current = buffer[i];
						
            if(current == '\n' && last == '\r') {
				++stats->win;
				
				if(doOut)
					fputs("\n", stdout);
				
			} else if(current == '\r') {
				// withhold tentative Mac newline
			} else if(last == '\r') {
				++stats->mac;
				
				if(doOut)
					fputc('\n', stdout);
			} else if(current == '\n') {
				++stats->unix;
				
				if(doOut)
					fputc(current, stdout);
			} else {
				if(doOut)
					fputc(current, stdout);
			}
			
			last = current;
		}
	} while( ! feof(file));
	
	if(last == '\r') {
		++stats->mac;
	
		if(doOut)
			fputc('\n', stdout);
	}
}

void print_stats(Stats* stats) {
    printf(" os   | escape | name | hex       | count \n");
    printf("-------------------------------\n");
    printf(" win  | \\r\\n   | CRLF | 0x0d 0x0a | %d\n", stats->win);
    printf(" unix | \\n     |  LF  | 0x0a (^J) | %d\n", stats->unix);
    printf(" mac  | \\r     |  CR  | 0x0d (^M) | %d\n", stats->mac);
}
