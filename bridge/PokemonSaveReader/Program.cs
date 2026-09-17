using System.Text.Json;
using PKHeX.Core;

if (args.Length != 1)
{
	Console.Error.WriteLine("Usage: PokemonSaveReader.exe <save-file>");
	return 1;
}

string savePath = args[0];

if (!File.Exists(savePath))
{
	Console.Error.WriteLine($"Save file not found: {savePath}");
	return 1;
}

try
{
	SaveFile? save = SaveUtil.GetSaveFile(savePath);

	if (save is null)
	{
		Console.Error.WriteLine("PKHeX could not identify the save file.");
		return 1;
	}

	var result = ReadSave(save, savePath);

	Console.WriteLine(
		JsonSerializer.Serialize(
			result,
			new JsonSerializerOptions
			{
				WriteIndented = true
			}
		)
	);

	return 0;
}
catch (Exception error)
{
	Console.Error.WriteLine(error);
	return 1;
}


static object ReadSave(SaveFile save, string savePath)
{
	return save switch
	{
		SAV8LA pla => ReadArceus(pla, savePath),
		SAV9SV sv => ReadScarletViolet(sv, savePath),
		_ => throw new InvalidOperationException(
			$"Unsupported save type: {save.GetType().Name}"
		)
	};
}


static object ReadArceus(SAV8LA save, string savePath)
{
	var playtime = save.Played;

	return new
	{
		success = true,

		game = new
		{
			version = save.Version.ToString(),
			generation = save.Generation,
			type = "legends_arceus"
		},

		file = new
		{
			name = Path.GetFileName(savePath),
			size = new FileInfo(savePath).Length
		},

		trainer = new
		{
			name = save.MyStatus.OT,
			id = save.MyStatus.ID32
		},

		playtime = new
		{
			hours = playtime.PlayedHours,
			minutes = playtime.PlayedMinutes,
			seconds = playtime.PlayedSeconds
		},

		pokedex = new
		{
			seen = save.PokedexSave.GetDexGetCount(PokedexType8a.Hisui),
			total = PokedexSave8a.GetDexTotalCount(PokedexType8a.Hisui)
		}
	};
}


static object ReadScarletViolet(SAV9SV save, string savePath)
{
	var playtime = save.Played;

	return new
	{
		success = true,

		game = new
		{
			version = save.Version.ToString(),
			generation = save.Generation,
			type = "scarlet_violet"
		},

		file = new
		{
			name = Path.GetFileName(savePath),
			size = new FileInfo(savePath).Length
		},

		trainer = new
		{
			name = save.MyStatus.OT,
			id = save.MyStatus.ID32
		},

		playtime = new
		{
			hours = playtime.PlayedHours,
			minutes = playtime.PlayedMinutes,
			seconds = playtime.PlayedSeconds
		},

		pokedex = new
		{
			seen = save.Zukan.SeenCount,
			caught = save.Zukan.CaughtCount,
			total = save.MaxSpeciesID
		}
	};
}