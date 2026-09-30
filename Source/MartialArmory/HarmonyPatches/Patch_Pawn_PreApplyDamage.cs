using HarmonyLib;
using RimWorld;
using UnityEngine;
using Verse;

namespace MartialArmory.HarmonyPatches
{
    [HarmonyPatch(typeof(Pawn), "PreApplyDamage")]
    public static class Patch_Pawn_PreApplyDamage
    {
        [HarmonyPrefix]
        public static bool Prefix(Pawn __instance, ref DamageInfo dinfo, ref bool absorbed)
        {
            if (absorbed) return true;
            if (__instance == null || !__instance.Spawned || __instance.Dead || __instance.Downed) return true;

            var shield = ShieldUtility.GetEquippedShield(__instance);
            if (shield == null) return true;

            var damageDef = dinfo.Def;
            if (damageDef == null || damageDef.isExplosive || !damageDef.harmsHealth) return true;

            // Determine if the incoming attack is melee or ranged
            bool isRanged = dinfo.Weapon != null && dinfo.Weapon.IsRangedWeapon;
            float blockChance = isRanged
                ? shield.CalculateRangedBlockChance(__instance)
                : shield.CalculateMeleeBlockChance(__instance);

            if (Rand.Chance(blockChance))
            {
                absorbed = true;

                // Shield absorbs damage to its durability
                if (shield.parent is Apparel shieldApparel && shield.Props.damageToShieldFactor > 0f)
                {
                    int shieldDmg = Mathf.Max(1, Mathf.RoundToInt(dinfo.Amount * shield.Props.damageToShieldFactor));
                    shieldApparel.TakeDamage(new DamageInfo(DamageDefOf.Blunt, shieldDmg, 0, -1, dinfo.Instigator));
                }

                // Visual and audio feedback
                if (__instance.Map != null)
                {
                    MoteMaker.ThrowText(__instance.DrawPos, __instance.Map, "MA_ShieldBlocked".Translate(), Color.white);
                }

                return false; // Absorbed! Skip normal damage pipeline
            }

            return true;
        }
    }
}
