namespace PokemonSaveReader.Models;


public sealed class SaveData
{
	public bool Success { get; set; }
	public GameInfo Game { get; set; } = new();
	public TrainerData Trainer { get; set; } = new();
	public PlaytimeData Playtime { get; set; } = new();
	public PokedexData Pokedex { get; set; } = new();
	public PartyData Party { get; set; } = new();
	public BoxData Boxes { get; set; } = new();
	public ItemData Items { get; set; } = new();
	public CoordinateData Location { get; set; } = new();
	public ProgressData Progress { get; set; } = new();
}