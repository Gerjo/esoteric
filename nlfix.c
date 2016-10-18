#include <stdio.h>
#include <string.h>

/// Read from stdin and convert pesky mac newlines into unix.
/// Leaves windows newlines intact. Most tools seem to interpret
/// these fine anyway - and our current repository is riddled 
/// with them.
/// 
/// compile with: gcc nlfix.c -o nlfix
/// example: echo -e "hello\rfoo" | nlfix
/// example: cat myfile.txt | nlfix | tee out.txt

int main(int argc, char** argv) {

	char buffer[128];
	
	int nWin = 0;
	int nUnix = 0;
	int nMac = 0;

	int doOut = 1;
	int doStats = 0;
	
	if(argc > 1 && strcmp(argv[1], "-s") == 0) {
		doOut = 0;
		doStats = 1;
	}
	
	int retrieved = 0;
	char last = 0;
	do {
		int retrieved = fread(buffer, 1, sizeof buffer, stdin);
	
		for(int i = 0; i < retrieved; ++i) {
			char current = buffer[i];
						
			if(current == '\r' && last == '\n') {
				++nWin;
				
				// Keep as-is. (don't mess up git)
				if(doOut)
					fputs("\r\n", stdout);
				
			} else if(current == '\r') {
				// withhold tentative Mac newline
			} else if(last == '\r') {
				++nMac;
				
				if(doOut)
					fputc('\n', stdout);
			} else if(current == '\n') {
				++nUnix;
				
				if(doOut)
					fputc(current, stdout);
			} else {
				if(doOut)
					fputc(current, stdout);
			}
			
			last = current;
		}
	} while( ! feof(stdin));
	
	if(last == '\r') {
		++nMac;
	
		if(doOut)
			fputc('\n', stdout);
	}
	
	
	// \r 0x0d ^M 
	// \n 0x0a ^J
	
	if(doStats) {
		printf(" os   | escape | hex       | count \n");
		printf("-------------------------------\n");
		printf(" win  | \\n\\r   | 0x0a 0x0d | %d\n", nWin);
		printf(" unix | \\n     | 0x0a (^J) | %d\n", nUnix);
		printf(" mac  | \\r     | 0x0d (^M) | %d\n", nMac);
	}
	
	return 0;
}
