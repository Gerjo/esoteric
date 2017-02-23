//
//  swizzle.m
//  TestEnvironment
//
//  Created by Gerard Meier on 2/21/17.
//

#import <Foundation/Foundation.h>
#import <objc/runtime.h>

@protocol MyInterface
-(void) Foo;
@end

@interface SuperFoo : NSObject<MyInterface> {}

@end
@implementation SuperFoo
//-(void) Foo {
//    printf("SuperFoo's Foo\n");
//}
@end

@interface SuperFoo(Lurker) {}
@end
@implementation SuperFoo(Lurker)
//-(void) Foo {
//    printf("Lurker's Foo\n");
//}
@end

@interface SuperFoo(MyFoo) {}
@end

@implementation SuperFoo(MyFoo)
+(void) load {
    SEL sel[] = {@selector(Foo), @selector(FooBar)};
    Method met[] = {class_getInstanceMethod(self, sel[0]), class_getInstanceMethod(self, sel[1])};
    
    // Attempt to add method.
    BOOL wasAppended = class_addMethod(self, sel[0], method_getImplementation(met[1]), method_getTypeEncoding(met[1]));
    
    if(wasAppended) {
        // Method was added, because it did not exist. Override the 'old' selector to do nothing. This avoids
        // recursion when calling the super class within the overriden method.
        Method dummy = class_getInstanceMethod(self, @selector(gerardDummyMethodImplementation));
        class_replaceMethod(self, sel[1], method_getImplementation(dummy), method_getTypeEncoding(dummy));
        
    } else {
        // Append failed. This means the method already exists. In that case it's
        // trivial, just swap implementations.
        method_exchangeImplementations(met[0], met[1]);
    }
}
-(void) FooBar {
    printf("SuperFoo's Foo\n");
    
    [self FooBar];
}
-(void)gerardDummyMethodImplementation {
    // nop.
}
@end


int main(int argc, const char * argv[]) {
    
    SuperFoo* foo = [[SuperFoo new] autorelease];
    
    [foo Foo];

    
    return 0;
}
