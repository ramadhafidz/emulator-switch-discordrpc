namespace PokemonSaveReader.Models;


public sealed class PlaytimeData
{
	public int Hours { get; set; }
	public int Minutes { get; set; }
	public int Seconds { get; set; }
	public long TotalSeconds { get; set; }
}