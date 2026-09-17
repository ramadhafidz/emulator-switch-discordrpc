namespace PokemonSaveReader.Models;


public sealed class PokedexData
{
	public Dictionary<string, DexStats> Dexes { get; set; } = [];
}


public sealed class DexStats
{
	public int Seen { get; set; }
	public int Caught { get; set; }
	public int Total { get; set; }
}