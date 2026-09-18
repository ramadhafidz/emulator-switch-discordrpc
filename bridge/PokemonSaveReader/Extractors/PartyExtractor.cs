using PKHeX.Core;
using PokemonSaveReader.Models;

namespace PokemonSaveReader.Extractors;


public static class PartyExtractor
{
	public static PartyData Extract(SaveFile save)
	{
		var party = new PartyData();

		int count = Math.Min(save.PartyCount, 6);

		for (int i = 0; i < count; i++)
		{
			PKM pokemon = save.GetPartySlotAtIndex(i);

			if (pokemon.Species == 0)
				continue;

			party.Members.Add(
				PokemonExtractor.Extract(pokemon)
			);
		}

		return party;
	}
}