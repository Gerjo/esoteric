#import <Foundation/Foundation.h>

#include <stdio.h>


volatile int refBarCounter = 0;
volatile int totalBarInits = 0;
volatile int refFooCounter = 0;
volatile int totalFooInits = 0;

@interface Bar : NSObject<NSCopying>
@end
@implementation Bar
- (instancetype) init {
	self = [super init];
	
	printf("Bar::init\n");
	
	++totalBarInits;
	++refBarCounter;
	
	return self;
}
-(instancetype)copyWithZone: (NSZone *)_ {
	return [[self class] new];
}
- (void) dealloc {
	[super dealloc];
	printf("Bar::dealloc\n");
	--refBarCounter;
}
@end


@interface Foo : NSObject 
//@property(nonatomic, assign) Bar* propbar; // Does nothing. YOLO
@property(nonatomic, copy) Bar* propbar; // You must release
//@property(nonatomic, retain) Bar* propbar; // You must release
@end
@implementation Foo

- (instancetype) init {
	// NSObject isn't going to fail... is it?
	self = [super init];
	
	printf("Foo::init\n");
	
	++refFooCounter;
	++totalFooInits;
	
	return self;
}

-(void) hello {
	printf("hello!\n");
}

- (void) dealloc {
	printf("Foo::dealloc\n");


	// Both are basically the same.
	[self.propbar release];
	
	--refFooCounter;

	[super dealloc];
}
@end

int main() {
	@autoreleasepool {
		Foo* feh = [[Foo new] autorelease];
		
		Foo* foo = [Foo new];
	
		Bar* bar = [[Bar new] autorelease];
		foo.propbar = bar;
		
		printf("Assigning nil to propbar\n");
		foo.propbar = nil;
		
		printf("Assigning new Bar to propbar\n");
		foo.propbar = [[Bar new] autorelease];
		
		
		[foo release];
	}

	printf("Leaked %d/%d Foo instances.\n", refFooCounter, totalFooInits);
	printf("Leaked %d/%d Bar instances.\n", refBarCounter, totalBarInits);
	
	// assert(refFooCounter == refBarCounter == 0)
}
