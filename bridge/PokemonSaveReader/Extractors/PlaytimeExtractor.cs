using PKHeX.Core;
using PokemonSaveReader.Models;

namespace PokemonSaveReader.Extractors;

public static class PlaytimeExtractor
{
	public static PlaytimeData Extract(SAV8LA save)
	{
		int hours = save.PlayedHours;
		int minutes = save.PlayedMinutes;
		int seconds = save.PlayedSeconds;

		return new PlaytimeData
		{
			Hours = hours,
			Minutes = minutes,
			Seconds = seconds,
			TotalSeconds = (hours * 3600L) + (minutes * 60L) + seconds
		};
	}
}