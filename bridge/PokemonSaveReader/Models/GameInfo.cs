namespace PokemonSaveReader.Models;


public sealed class GameInfo
{
	public string Version { get; set; } = "";
	public int Generation { get; set; }
	public string Type { get; set; } = "";
}