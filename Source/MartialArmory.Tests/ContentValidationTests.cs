using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Xml.Linq;
using NUnit.Framework;

namespace MartialArmory.Tests
{
    [TestFixture]
    public class ContentValidationTests
    {
        private static readonly string[] ExpectedWeapons =
        {
            "MA_MeleeWeapon_Halberd",
            "MA_MeleeWeapon_Morningstar",
            "MA_MeleeWeapon_WarPick",
            "MA_MeleeWeapon_Scimitar",
            "MA_MeleeWeapon_Quarterstaff"
        };

        private static readonly string[] ExpectedShields =
        {
            "MA_Shield_Buckler",
            "MA_Shield_Round",
            "MA_Shield_Kite",
            "MA_Shield_Tower"
        };

        private string modRoot;
        private List<XElement> weaponDefs;
        private List<XElement> shieldDefs;
        private XDocument aboutDoc;

        [SetUp]
        public void Setup()
        {
            DirectoryInfo dir = new DirectoryInfo(AppDomain.CurrentDomain.BaseDirectory);
            while (dir != null && dir.Name != "MartialArmory" && dir.Name != "Source")
                dir = dir.Parent;
            if (dir?.Name == "Source")
                dir = dir.Parent;
            Assert.That(dir, Is.Not.Null, "Could not locate MartialArmory mod directory");
            modRoot = dir!.FullName;

            string weaponDefPath = Path.Combine(modRoot, "Defs", "ThingDefs", "Weapons_MartialArmory.xml");
            Assert.That(File.Exists(weaponDefPath), Is.True, $"File not found: {weaponDefPath}");
            weaponDefs = XDocument.Load(weaponDefPath).Root!.Elements("ThingDef").ToList();

            string shieldDefPath = Path.Combine(modRoot, "Defs", "ThingDefs", "Apparel_Shields.xml");
            Assert.That(File.Exists(shieldDefPath), Is.True, $"File not found: {shieldDefPath}");
            shieldDefs = XDocument.Load(shieldDefPath).Root!.Elements("ThingDef").ToList();

            string aboutPath = Path.Combine(modRoot, "About", "About.xml");
            Assert.That(File.Exists(aboutPath), Is.True, $"File not found: {aboutPath}");
            aboutDoc = XDocument.Load(aboutPath);
        }

        [Test]
        public void AboutXml_HasValidMetadata()
        {
            var root = aboutDoc.Root;
            Assert.That(root, Is.Not.Null);
            Assert.That(root.Element("name")?.Value, Is.EqualTo("Martial Armory"));
            Assert.That(root.Element("packageId")?.Value, Is.EqualTo("throwingfish.martialarmory"));
            Assert.That(root.Element("author")?.Value, Is.EqualTo("throwingfish"));

            var versions = root.Element("supportedVersions")?.Elements("li").Select(e => e.Value).ToList();
            Assert.That(versions, Does.Contain("1.6"));
        }

        [Test]
        public void AllWeaponsAndShields_UseMAPrefix()
        {
            foreach (var def in weaponDefs.Concat(shieldDefs))
            {
                string name = def.Element("defName")?.Value ?? def.Attribute("Name")?.Value;
                Assert.That(name, Does.StartWith("MA_"), $"{name} must use MA_ prefix");
            }
        }

        [TestCaseSource(nameof(ExpectedWeapons))]
        public void Weapon_HasGraphic_AndTextureFileExists(string defName)
        {
            var def = weaponDefs.First(d => d.Element("defName")?.Value == defName);
            string texPath = def.Element("graphicData")?.Element("texPath")?.Value;
            Assert.That(texPath, Is.Not.Null, $"Missing texPath in {defName}");

            string pngPath = Path.Combine(modRoot, "Textures", texPath + ".png");
            Assert.That(File.Exists(pngPath), Is.True, $"Texture missing on disk: {pngPath}");
        }

        [TestCaseSource(nameof(ExpectedShields))]
        public void Shield_HasGraphic_AndTextureFileExists(string defName)
        {
            var def = shieldDefs.First(d => d.Element("defName")?.Value == defName);
            string texPath = def.Element("graphicData")?.Element("texPath")?.Value;
            Assert.That(texPath, Is.Not.Null, $"Missing texPath in {defName}");

            string pngPath = Path.Combine(modRoot, "Textures", texPath + ".png");
            Assert.That(File.Exists(pngPath), Is.True, $"Shield texture missing on disk: {pngPath}");
        }

        [TestCaseSource(nameof(ExpectedShields))]
        public void Shield_HasValidCompPropertiesShield(string defName)
        {
            var def = shieldDefs.First(d => d.Element("defName")?.Value == defName);
            var comp = def.Element("comps")?.Elements("li")
                .FirstOrDefault(c => c.Attribute("Class")?.Value == "MartialArmory.CompProperties_Shield");
            
            Assert.That(comp, Is.Not.Null, $"Shield {defName} must have CompProperties_Shield");
            float meleeBlock = float.Parse(comp!.Element("meleeBlockChanceBase")!.Value);
            float rangedBlock = float.Parse(comp.Element("rangedBlockChanceBase")!.Value);
            Assert.That(meleeBlock, Is.GreaterThan(0f).And.LessThanOrEqualTo(1f));
            Assert.That(rangedBlock, Is.GreaterThan(0f).And.LessThanOrEqualTo(1f));
        }

        [Test]
        public void HalberdAndQuarterstaff_AreTaggedTwoHanded()
        {
            var halberd = weaponDefs.First(d => d.Element("defName")?.Value == "MA_MeleeWeapon_Halberd");
            var tags = halberd.Element("weaponTags")!.Elements("li").Select(e => e.Value).ToList();
            Assert.That(tags, Does.Contain("MA_TwoHanded"));

            var staff = weaponDefs.First(d => d.Element("defName")?.Value == "MA_MeleeWeapon_Quarterstaff");
            var staffTags = staff.Element("weaponTags")!.Elements("li").Select(e => e.Value).ToList();
            Assert.That(staffTags, Does.Contain("MA_TwoHanded"));
        }

        [Test]
        public void OneHandedWeapons_DoNotHaveTwoHandedTag()
        {
            string[] oneHanders = { "MA_MeleeWeapon_Morningstar", "MA_MeleeWeapon_WarPick", "MA_MeleeWeapon_Scimitar" };
            foreach (var name in oneHanders)
            {
                var def = weaponDefs.First(d => d.Element("defName")?.Value == name);
                var tags = def.Element("weaponTags")!.Elements("li").Select(e => e.Value).ToList();
                Assert.That(tags, Does.Not.Contain("MA_TwoHanded"));
            }
        }

        [Test]
        public void VanillaTwoHandedPatches_FileExistsAndValid()
        {
            string patchPath = Path.Combine(modRoot, "Patches", "Vanilla_TwoHandedWeapons.xml");
            Assert.That(File.Exists(patchPath), Is.True);
            var doc = XDocument.Load(patchPath);
            Assert.That(doc.Root?.Name.LocalName, Is.EqualTo("Patch"));
        }
    }
}
