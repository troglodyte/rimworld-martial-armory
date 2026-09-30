using Verse;

namespace MartialArmory
{
    public class CompProperties_Shield : CompProperties
    {
        public float meleeBlockChanceBase = 0.40f;
        public float rangedBlockChanceBase = 0.25f;
        public float damageToShieldFactor = 0.50f;

        public CompProperties_Shield()
        {
            compClass = typeof(CompShield);
        }
    }

    public class CompShield : ThingComp
    {
        public CompProperties_Shield Props => (CompProperties_Shield)props;

        public float MeleeBlockChanceBase => Props.meleeBlockChanceBase;
        public float RangedBlockChanceBase => Props.rangedBlockChanceBase;

        public float CalculateMeleeBlockChance(Pawn pawn)
        {
            if (pawn == null) return Props.meleeBlockChanceBase;
            
            // Scaling with melee skill: Skill 0 = 0.5x base, Skill 10 = 1.0x base, Skill 20 = 1.5x base
            int meleeSkill = pawn.skills?.GetSkill(RimWorld.SkillDefOf.Melee)?.Level ?? 5;
            float skillFactor = 0.5f + (meleeSkill * 0.05f);

            // Manipulation factor (100% manipulation = 1.0)
            float manipulation = pawn.health?.capacities?.GetLevel(RimWorld.PawnCapacityDefOf.Manipulation) ?? 1f;

            return UnityEngine.Mathf.Clamp(Props.meleeBlockChanceBase * skillFactor * manipulation, 0.05f, 0.85f);
        }

        public float CalculateRangedBlockChance(Pawn pawn)
        {
            if (pawn == null) return Props.rangedBlockChanceBase;

            float manipulation = pawn.health?.capacities?.GetLevel(RimWorld.PawnCapacityDefOf.Manipulation) ?? 1f;
            return UnityEngine.Mathf.Clamp(Props.rangedBlockChanceBase * manipulation, 0.05f, 0.80f);
        }
    }
}
