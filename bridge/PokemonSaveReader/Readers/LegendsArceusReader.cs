using PKHeX.Core;
using PokemonSaveReader.Extractors;
using PokemonSaveReader.Models;
using GameInfo = PokemonSaveReader.Models.GameInfo;

namespace PokemonSaveReader.Readers;


public class LegendsArceusReader : ISaveReader
{
	public bool CanRead(SaveFile save)
	{
		return save is SAV8LA;
	}


	public SaveData Read(SaveFile save)
	{
		if (save is not SAV8LA pla)
			throw new ArgumentException(
				"Save file is not a Pokémon Legends: Arceus save."
			);

		var trainer = TrainerExtractor.Extract(pla);
		var playtime = PlaytimeExtractor.Extract(pla);
		var pokedex = PokedexExtractor.Extract(pla);

		return new SaveData
		{
			Success = true,

			Game = new GameInfo
			{
				Version = pla.Version.ToString(),
				Generation = 8,
				Type = "legends_arceus"
			},

			Trainer = trainer,

			Playtime = playtime,

			Pokedex = pokedex
		};
	}
}