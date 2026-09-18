using PKHeX.Core;
using PokemonSaveReader.Models;

namespace PokemonSaveReader.Extractors;


public static class BoxExtractor
{
	public static BoxData Extract(SaveFile save)
	{
		var boxes = new BoxData();

		for (int box = 0; box < save.BoxCount; box++)
		{
			var boxData = new Box
			{
				Number = box + 1
			};

			for (int slot = 0; slot < save.BoxSlotCount; slot++)
			{
				PKM pokemon = save.GetBoxSlotAtIndex(
					box,
					slot
				);

				if (pokemon.Species == 0)
					continue;

				boxData.Slots.Add(
					new BoxSlot
					{
						Slot = slot + 1,
						Pokemon = PokemonExtractor.Extract(pokemon)
					}
				);
			}

			boxes.Boxes.Add(boxData);
		}

		return boxes;
	}
}