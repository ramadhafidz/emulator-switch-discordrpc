using PKHeX.Core;
using PokemonSaveReader.Models;

namespace PokemonSaveReader.Extractors;


public static class PokemonExtractor
{
	public static PokemonData Extract(PKM pokemon)
	{
		return new PokemonData
		{
			Species = pokemon.Species,

			SpeciesName = SpeciesName.GetSpeciesName(
				pokemon.Species,
				(int)LanguageID.English
			),

			Form = pokemon.Form,
			Level = pokemon.CurrentLevel,
			IsShiny = pokemon.IsShiny,
			IsAlpha = pokemon is PA8 pa8 && pa8.IsAlpha,
			Nickname = pokemon.Nickname,

			Gender = pokemon.Gender,
			Nature = pokemon.Nature.ToString(),
			Ability = pokemon.Ability,
			HeldItem = pokemon.HeldItem
		};
	}
}