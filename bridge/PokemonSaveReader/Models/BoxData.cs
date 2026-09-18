namespace PokemonSaveReader.Models;


public sealed class BoxData
{
	public List<Box> Boxes { get; set; } = [];
}


public sealed class Box
{
	public int Number { get; set; }
	public List<BoxSlot> Slots { get; set; } = [];
}


public sealed class BoxSlot
{
	public int Slot { get; set; }
	public PokemonData? Pokemon { get; set; }
}