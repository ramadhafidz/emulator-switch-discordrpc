using PKHeX.Core;
using PokemonSaveReader.Models;

namespace PokemonSaveReader.Extractors;

public static class TrainerExtractor
{
	public static TrainerData Extract(SAV8LA save)
	{
		return new TrainerData
		{
			Name = save.OT
		};
	}
}