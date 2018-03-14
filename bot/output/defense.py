from bot.output.thresholds import OutputThresholds
from models import Build


def get_resistances(build: Build, normal_res_cap: int, force_display=False):
    """
    Creates the resistance string
    :param build: build we want to output
    :param normal_res_cap: values above this threshold are displayed
    :param force_display:  override threshold
    :return: string containing all resistances or and empty string if nothing is noteworthy
    """
    output = "**Resistances**: "
    resistances = ['Fire', 'Cold', 'Lightning', 'Chaos']
    emojis = [':fire:', ':snowflake:', ':zap:', ':skull:']
    show = False
    for i, res in enumerate(resistances):
        res_val = build.get_stat('Player', res + 'Resist')
        res_over_cap = build.get_stat('Player', res + 'ResistOverCap')

        if res_val and (force_display or res_val > normal_res_cap):
            output += emojis[i] + " {:.0f}".format(res_val)
            show = True
            if res_over_cap and res_over_cap > 0:
                output += "(+{:.0f}) ".format(res_over_cap)
            output += " "
    output += "\n"
    return output if show else ""


def get_basic_line(name, basic_stat, basic_stat_percent, stat_unreserved=0, basic_stat_regen=0):
    output = ""
    print("Mana",basic_stat,basic_stat_percent) if 'Mana' in name else None
    if basic_stat and basic_stat_percent:
        output = "**" + name + "**: "
        if stat_unreserved and basic_stat - stat_unreserved > 0:
            output += "{unreserved:.0f}/".format(unreserved=stat_unreserved)
        output += "{stat:.0f}".format(stat=basic_stat)
        output += " ({stat_percent:.0f}%)".format(stat_percent=basic_stat_percent)
        if basic_stat_regen:
            # Total regen, if displayed is regen - degen.
            output += " | Regen: {regen:.0f}/s".format(regen=basic_stat_regen)
        output += "\n"
    return output


def get_secondary_def(build: Build):
    """
    Parse all secondary defenses such as armor, eva, dodge, block and display them if they are higher than the thresholds.
    :param build: current build
    :return: String containing noteworthy secondary defense, Empty string as default
    """
    output = "**Secondary:** "
    stats = []
    armour = build.get_stat('Player', 'Armour')
    stats.append("Armour: {}".format(armour) if armour and armour > OutputThresholds.ARMOUR.value else None)
    evasion = build.get_stat('Player', 'Evasion')
    stats.append(
        "Evasion: {}".format(evasion) if evasion and evasion > OutputThresholds.EVASION.value else None)

    dodge = build.get_stat('Player', 'AttackDodgeChance')
    stats.append("Dodge: {}%".format(dodge) if dodge and dodge > OutputThresholds.DODGE.value else None)

    spell_dodge = build.get_stat('Player', 'SpellDodgeChance')
    stats.append("Spell Dodge: {}%".format(
        spell_dodge) if spell_dodge and spell_dodge > OutputThresholds.SPELL_DODGE.value else None)

    block = build.get_stat('Player', 'BlockChance')
    stats.append("Block: {}%".format(block) if block and block > OutputThresholds.BLOCK.value else None)

    spell_block = build.get_stat('Player', 'SpellBlockChance')
    stats.append("Spell Block: {}%".format(
        spell_block) if spell_block and spell_block > OutputThresholds.SPELL_BLOCK.value else None)
    output += " | ".join([s for s in stats if s]) + "\n"
    return output if output != "" else None


def get_defense(build: Build):
    output = ""
    output += get_basic_line("Life", build.get_stat('Player', 'Life'),
                             build.get_stat('Player', 'Spec:LifeInc', OutputThresholds.LIFE_PERCENT.value),
                             basic_stat_regen=build.get_stat('Player', 'LifeRegen', OutputThresholds.LIFE_REGEN.value),
                             stat_unreserved=build.get_stat('Player','LifeUnreserved'))


    output += get_basic_line("Energy Shield", build.get_stat('Player', 'EnergyShield'),
                             build.get_stat('Player', 'Spec:EnergyShieldInc', OutputThresholds.ES_PERCENT.value),
                             basic_stat_regen=build.get_stat('Player', 'EnergyShieldRegen',OutputThresholds.ES_REGEN.value))

    output += "**Net Regen**: {:.0f}/s\n".format(build.get_stat('Player','NetLifeRegen'))

    output += get_basic_line("Mana", build.get_stat('Player', 'Mana'), build.get_stat('Player', 'Spec:ManaInc'),
                             basic_stat_regen=build.get_stat('Player', 'ManaRegen'),
                             stat_unreserved=build.get_stat('Player', 'ManaUnreserved'))

    # todo: only pass necessary values to the following options:
    output += get_secondary_def(build)
    output += get_resistances(build, OutputThresholds.MAX_RES.value)

    return output
