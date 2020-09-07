using System;

public interface IItem { }

public class Item : IItem { }
public class Test { }

public class Collection<T> {
	
	public void Add<TTT>(IItem item) where TTT:T, IItem {
		Console.WriteLine("A alt generic item was added.");
	}
	
	public void Add<TT>(TT item) where TT:T {
		Console.WriteLine("A generic item was added.");
	}
	
}

public static class main {
	public static void Main(string[] args) {
		{	
			Collection<Item> collection = new Collection<Item>();
			collection.Add(new Item());
		}
		{	
			Collection<Test> collection = new Collection<Test>();
			collection.Add(new Test());
		}
		{
			//Collection<float> collection = new Collection<float>();
			//collection.Add(1987.07f);
		}
	}
}