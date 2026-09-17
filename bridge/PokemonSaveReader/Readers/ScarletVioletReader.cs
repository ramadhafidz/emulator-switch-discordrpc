using PKHeX.Core;
using PokemonSaveReader.Models;
using GameInfo = PokemonSaveReader.Models.GameInfo;

namespace PokemonSaveReader.Readers;


public class ScarletVioletReader : ISaveReader
{
	public bool CanRead(SaveFile save)
	{
		return save is SAV9SV;
	}


	public SaveData Read(SaveFile save)
	{
		if (save is not SAV9SV sv)
			throw new ArgumentException(
				"Save file is not a Scarlet/Violet save."
			);

		var playtime = sv.Played;
		var dexStats = GetDexStats(sv);

		return new SaveData
		{
			Success = true,

			Game = new GameInfo
			{
				Version = sv.Version.ToString(),
				Generation = 9,
				Type = "scarlet_violet"
			},

			Trainer = new TrainerData
			{
				Name = sv.MyStatus.OT,
				ID = sv.MyStatus.ID32
			},

			Playtime = new PlaytimeData
			{
				Hours = playtime.PlayedHours,
				Minutes = playtime.PlayedMinutes,
				Seconds = playtime.PlayedSeconds,
				TotalSeconds =
					(playtime.PlayedHours * 3600L)
					+ (playtime.PlayedMinutes * 60L)
					+ playtime.PlayedSeconds
			},

			Pokedex = new PokedexData
			{
				Dexes =
				{
					["paldea"] = dexStats.Paldea,
					["kitakami"] = dexStats.Kitakami,
					["blueberry"] = dexStats.Blueberry
				}
			}
		};
	}


	private static DexResult GetDexStats(SAV9SV save)
	{
		var paldeaSeen = 0;
		var paldeaCaught = 0;

		var kitakamiSeen = 0;
		var kitakamiCaught = 0;

		var blueberrySeen = 0;
		var blueberryCaught = 0;


		for (
			ushort species = 1;
			species <= save.MaxSpeciesID;
			species++
		)
		{
			var group = GetDexGroup(save, species);

			if (group == 0)
				continue;

			var seen = GetSeen(save, species);
			var caught = GetCaught(save, species);


			switch (group)
			{
				case 1:
					if (seen)
						paldeaSeen++;

					if (caught)
						paldeaCaught++;

					break;


				case 2:
					if (seen)
						kitakamiSeen++;

					if (caught)
						kitakamiCaught++;

					break;


				case 3:
					if (seen)
						blueberrySeen++;

					if (caught)
						blueberryCaught++;

					break;
			}
		}


		return new DexResult
		{
			Paldea = new DexStats
			{
				Seen = paldeaSeen,
				Caught = paldeaCaught,
				Total = 400
			},

			Kitakami = new DexStats
			{
				Seen = kitakamiSeen,
				Caught = kitakamiCaught,
				Total = 200
			},

			Blueberry = new DexStats
			{
				Seen = blueberrySeen,
				Caught = blueberryCaught,
				Total = 243
			}
		};
	}


	private static byte GetDexGroup(
		SAV9SV save,
		ushort species
	)
	{
		var pi = save.Personal.GetFormEntry(species, 0);


		for (
			byte form = 0;
			form <= pi.FormCount;
			form++
		)
		{
			pi = save.Personal.GetFormEntry(species, form);


			if (pi.DexPaldea != 0)
				return 1;


			if (pi.DexKitakami != 0)
				return 2;


			if (pi.DexBlueberry != 0)
				return 3;
		}


		return 0;
	}


	private static bool GetSeen(
		SAV9SV save,
		ushort species
	)
	{
		return save.Zukan.GetRevision() switch
		{
			0 => save.Zukan.DexPaldea.GetSeen(species),
			1 => save.Zukan.DexKitakami.GetSeen(species),
			_ => false
		};
	}


	private static bool GetCaught(
		SAV9SV save,
		ushort species
	)
	{
		return save.Zukan.GetRevision() switch
		{
			0 => save.Zukan.DexPaldea.GetCaught(species),
			1 => save.Zukan.DexKitakami.GetCaught(species),
			_ => false
		};
	}


	private sealed class DexResult
	{
		public DexStats Paldea { get; set; } = new();

		public DexStats Kitakami { get; set; } = new();

		public DexStats Blueberry { get; set; } = new();
	}
}