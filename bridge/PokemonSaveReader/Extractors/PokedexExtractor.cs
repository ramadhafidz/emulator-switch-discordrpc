using PKHeX.Core;
using PokemonSaveReader.Models;

namespace PokemonSaveReader.Extractors;


public static class PokedexExtractor
{
	public static PokedexData Extract(SAV8LA save)
	{
		PokedexSave8a pokedex = save.Blocks.PokedexSave;

		int total = PokedexSave8a.GetDexTotalCount(
			PokedexType8a.Hisui
		);

		int caught = pokedex.GetDexGetCount(
			PokedexType8a.Hisui
		);

		return new PokedexData
		{
			Dexes =
			{
				["hisui"] = new DexStats
				{
					// See note below.
					Seen = caught,
					Caught = caught,
					Total = total
				}
			}
		};
	}
}