namespace PokemonSaveReader.Models;


public sealed class LocationData
{
	public string? Name { get; set; }

	public int? FieldID { get; set; }
	public int? LocationID { get; set; }

	public double? X { get; set; }
	public double? Y { get; set; }
	public double? Z { get; set; }
}