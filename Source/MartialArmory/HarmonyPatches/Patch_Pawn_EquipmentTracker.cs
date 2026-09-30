using HarmonyLib;
using RimWorld;
using Verse;

namespace MartialArmory.HarmonyPatches
{
    [HarmonyPatch(typeof(Pawn_EquipmentTracker), "AddEquipment")]
    public static class Patch_Pawn_EquipmentTracker_AddEquipment
    {
        [HarmonyPrefix]
        public static void Prefix(Pawn_EquipmentTracker __instance, ThingWithComps newEq)
        {
            if (newEq == null || __instance?.pawn == null) return;

            Pawn pawn = __instance.pawn;
            if (ShieldUtility.IsTwoHanded(newEq.def))
            {
                var shieldComp = ShieldUtility.GetEquippedShield(pawn);
                if (shieldComp != null && shieldComp.parent is Apparel shieldApparel)
                {
                    if (pawn.apparel.TryDrop(shieldApparel, out _, pawn.Position, true))
                    {
                        if (pawn.Faction == Faction.OfPlayer && pawn.Spawned)
                        {
                            Messages.Message("MA_DroppedShieldForTwoHanded".Translate(pawn.Named("PAWN"), shieldApparel.Named("SHIELD")), pawn, MessageTypeDefOf.NeutralEvent);
                        }
                    }
                }
            }
        }
    }
}
