using NUnit.Framework;

namespace MartialArmory.Tests
{
    [TestFixture]
    public class ShieldLogicTests
    {
        [Test]
        public void TwoHandedTag_MatchesConstant()
        {
            Assert.That(ShieldUtility.TwoHandedTag, Is.EqualTo("MA_TwoHanded"));
        }

        [Test]
        public void IsTwoHanded_NullSafe()
        {
            Assert.That(ShieldUtility.IsTwoHanded(null), Is.False);
        }

        [Test]
        public void IsShield_NullSafe()
        {
            Assert.That(ShieldUtility.IsShield((Verse.ThingDef)null), Is.False);
            Assert.That(ShieldUtility.IsShield((Verse.Thing)null), Is.False);
        }

        [Test]
        public void HasShieldEquipped_NullPawnSafe()
        {
            Assert.That(ShieldUtility.HasShieldEquipped(null), Is.False);
            Assert.That(ShieldUtility.IsWieldingTwoHanded(null), Is.False);
        }
    }
}
