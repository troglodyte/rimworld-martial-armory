using HarmonyLib;
using RimWorld;
using Verse;

namespace MartialArmory.HarmonyPatches
{
    [HarmonyPatch(typeof(EquipmentUtility), nameof(EquipmentUtility.CanEquip),
        new[] { typeof(Thing), typeof(Pawn), typeof(string), typeof(bool) },
        new[] { ArgumentType.Normal, ArgumentType.Normal, ArgumentType.Out, ArgumentType.Normal })]
    public static class Patch_EquipmentUtility_CanEquip
    {
        [HarmonyPostfix]
        public static void Postfix(Thing thing, Pawn pawn, ref string cantReason, ref bool __result)
        {
            if (!__result || thing == null || pawn == null) return;

            if (ShieldUtility.IsTwoHanded(thing.def) && ShieldUtility.HasShieldEquipped(pawn))
            {
                __result = false;
                cantReason = "MA_CantEquipTwoHandedWithShield".Translate();
            }
        }
    }
}
