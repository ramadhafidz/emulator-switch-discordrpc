namespace PokemonSaveReader.Models;

public sealed class SaveData
{
	public bool Success { get; set; }

	public GameData Game { get; set; } = new();

	public TrainerData Trainer { get; set; } = new();

	public PlaytimeData Playtime { get; set; } = new();

	public PokedexData Pokedex { get; set; } = new();

	public PartyData Party { get; set; } = new();

	public BoxData Boxes { get; set; } = new();

	public ItemData Items { get; set; } = new();

	public CoordinateData Location { get; set; } = new();

	public ProgressData Progress { get; set; } = new();
}


public sealed class GameData
{
	public string Version { get; set; } = "";
	public int Generation { get; set; }
}


public sealed class TrainerData
{
	public string? Name { get; set; }
}


public sealed class PlaytimeData
{
	public int Hours { get; set; }
	public int Minutes { get; set; }
	public int Seconds { get; set; }
	public long TotalSeconds { get; set; }
}


public sealed class PokedexData
{
	public int Caught { get; set; }
	public int Total { get; set; }
}


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


public sealed class PartyData
{
	public List<PokemonData> Members { get; set; } = [];
}


public sealed class BoxData
{
	public List<PokemonData> Pokemon { get; set; } = [];
}


public sealed class ItemData
{
	public List<object> Items { get; set; } = [];
}


public sealed class CoordinateData
{
	public double? X { get; set; }
	public double? Y { get; set; }
	public double? Z { get; set; }
}


public sealed class ProgressData
{
	public Dictionary<string, object?> Values { get; set; } = [];
}