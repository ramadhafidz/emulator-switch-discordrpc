namespace PokemonSaveReader.Models;


public sealed class PokemonData
{
	public int Species { get; set; }
	public string? SpeciesName { get; set; }
	public int Form { get; set; }
	public int Level { get; set; }
	public bool IsShiny { get; set; }
	public bool IsAlpha { get; set; }
	public string? Nickname { get; set; }
}