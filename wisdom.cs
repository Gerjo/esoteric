using System;


public class Program {
	
	public enum MyEnum {
		Gerard,
		Purple,
		Monkey,
		Dishwasher,
	};
	
	public class MyClass<T> {
		public void Operation(T value) {
			System.Console.WriteLine(value);
		}
	}
	
	public static void Main(string[] args) {
		
		MyClass<MyEnum> worker = new MyClass<MyEnum>();
		
		worker.Operation(MyEnum.Monkey);
		
		System.Console.WriteLine("good");
	}
}