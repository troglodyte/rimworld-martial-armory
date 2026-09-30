using HarmonyLib;
using Verse;

namespace MartialArmory
{
    public class MartialArmoryMod : Mod
    {
        public MartialArmoryMod(ModContentPack content) : base(content)
        {
            var harmony = new Harmony("throwingfish.martialarmory");
            harmony.PatchAll();
        }
    }
}
