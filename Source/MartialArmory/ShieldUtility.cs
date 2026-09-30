using RimWorld;
using Verse;

namespace MartialArmory
{
    public static class ShieldUtility
    {
        public const string TwoHandedTag = "MA_TwoHanded";

        public static bool IsTwoHanded(ThingDef def)
        {
            if (def == null) return false;
            return def.weaponTags != null && def.weaponTags.Contains(TwoHandedTag);
        }

        public static bool IsShield(ThingDef def)
        {
            if (def == null) return false;
            return def.HasComp(typeof(CompShield));
        }

        public static bool IsShield(Thing thing)
        {
            return thing != null && IsShield(thing.def);
        }

        public static CompShield GetEquippedShield(Pawn pawn)
        {
            if (pawn?.apparel?.WornApparel == null) return null;

            foreach (var apparel in pawn.apparel.WornApparel)
            {
                var comp = apparel.GetComp<CompShield>();
                if (comp != null)
                {
                    return comp;
                }
            }
            return null;
        }

        public static bool HasShieldEquipped(Pawn pawn)
        {
            return GetEquippedShield(pawn) != null;
        }

        public static bool IsWieldingTwoHanded(Pawn pawn)
        {
            var primary = pawn?.equipment?.Primary;
            return primary != null && IsTwoHanded(primary.def);
        }
    }
}
