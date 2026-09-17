using System.Text.Json;
using PKHeX.Core;
using PokemonSaveReader.Models;
using PokemonSaveReader.Readers;
using SaveReader = PokemonSaveReader.Readers.ISaveReader;


if (args.Length != 1)
{
	Console.Error.WriteLine(
		"Usage: PokemonSaveReader.exe <save-file>"
	);

	return 1;
}


string savePath = args[0];


if (!File.Exists(savePath))
{
	Console.Error.WriteLine(
		$"Save file not found: {savePath}"
	);

	return 1;
}


try
{
	SaveFile? save = SaveUtil.GetSaveFile(savePath);

	if (save is null)
	{
		Console.Error.WriteLine(
			"PKHeX could not identify the save file."
		);

		return 1;
	}


	var readers = new SaveReader[]
	{
		new LegendsArceusReader(),
		new ScarletVioletReader()
	};


	SaveReader? reader = readers.FirstOrDefault(
		x => x.CanRead(save)
	);


	if (reader is null)
	{
		throw new InvalidOperationException(
			$"Unsupported save type: {save.GetType().Name}"
		);
	}


	SaveData result = reader.Read(save);


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