using PKHeX.Core;
using PokemonSaveReader.Models;

namespace PokemonSaveReader.Extractors;


public static class LocationExtractor
{
	private const uint KPlayerCurrentFieldID = 0xF17EB014;
	private const uint KPlayerCurrentLocationID = 0x19FC5B7B;
	private const uint KCoordinates = 0x708D1511;


	public static LocationData Extract(SAV9SV save)
	{
		var coordinates = GetCoordinates(save);
		var locationID = GetLocationID(save);

		return new LocationData
		{
			Name = GetLocationName(save, locationID),

			FieldID = GetFieldID(save),
			LocationID = locationID,

			X = coordinates?.X,
			Y = coordinates?.Y,
			Z = coordinates?.Z
		};
	}


	private static string? GetLocationName(
		SAV9SV save,
		int? locationID
	)
	{
		if (locationID is null)
			return null;

		return PKHeX.Core.GameInfo.GetLocationName(
			isEggLocation: false,
			location: (ushort)locationID.Value,
			format: 9,
			generation: 9,
			version: save.Version
		);
	}


	private static CoordinateData? GetCoordinates(
		SAV9SV save
	)
	{
		if (!save.Blocks.TryGetBlock(
			KCoordinates,
			out var block
		))
		{
			return null;
		}

		var data = block.Raw.Span;

		if (data.Length < 12)
			return null;

		return new CoordinateData
		{
			X = BitConverter.ToSingle(
				data.Slice(0, 4)
			),

			Y = BitConverter.ToSingle(
				data.Slice(4, 4)
			),

			Z = BitConverter.ToSingle(
				data.Slice(8, 4)
			)
		};
	}


	private static int? GetFieldID(SAV9SV save)
	{
		if (!save.Blocks.TryGetBlock(
			KPlayerCurrentFieldID,
			out var block
		))
		{
			return null;
		}

		return block.Raw.Span[0];
	}


	private static int? GetLocationID(SAV9SV save)
	{
		if (!save.Blocks.TryGetBlock(
			KPlayerCurrentLocationID,
			out var block
		))
		{
			return null;
		}

		return BitConverter.ToInt32(
			block.Raw.Span
		);
	}
}