using HarmonyLib;
using RimWorld;
using Verse;

namespace MartialArmory.HarmonyPatches
{
    [HarmonyPatch(typeof(Pawn_ApparelTracker), "Wear")]
    public static class Patch_Pawn_ApparelTracker_Wear
    {
        [HarmonyPrefix]
        public static void Prefix(Pawn_ApparelTracker __instance, Apparel newApparel)
        {
            if (newApparel == null || __instance?.pawn == null) return;

            Pawn pawn = __instance.pawn;
            if (ShieldUtility.IsShield(newApparel) && ShieldUtility.IsWieldingTwoHanded(pawn))
            {
                var primary = pawn.equipment?.Primary;
                if (primary != null)
                {
                    if (pawn.equipment.TryDropEquipment(primary, out _, pawn.Position, true))
                    {
                        if (pawn.Faction == Faction.OfPlayer && pawn.Spawned)
                        {
                            Messages.Message("MA_DroppedTwoHandedForShield".Translate(pawn.Named("PAWN"), primary.Named("WEAPON")), pawn, MessageTypeDefOf.NeutralEvent);
                        }
                    }
                }
            }
        }
    }
}
