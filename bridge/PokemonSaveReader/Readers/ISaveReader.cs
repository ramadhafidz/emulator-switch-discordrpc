using PKHeX.Core;
using PokemonSaveReader.Models;

namespace PokemonSaveReader.Readers;

public interface ISaveReader
{
	bool CanRead(SaveFile save);
	SaveData Read(SaveFile save);
}