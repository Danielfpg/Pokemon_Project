from enum import Enum

class TipoCartaEnum(str, Enum):
    pokemon = "pokemon"
    entrenador = "entrenador"
    energia = "energia"

class TipoEnergiaEnum(str, Enum):
    fuego = "fuego"
    agua = "agua"
    planta="planta"
    incolora = "incolora"

from enum import Enum

class RarezaEnum(str, Enum):
    # Rarezas básicas
    comun = "común"
    poco_comun = "poco común"
    rara = "rara"
    rara_holo = "rara holográfica"
    doble_rara = "doble rara"
    rara_ilustracion = "rara de ilustración"
    rara_ilustracion_especial = "rara de ilustración especial"
    rara_brillante = "rara brillante"  # Shiny Rare

    # Rarezas especiales (modernas)
    character_rare = "rara de personaje"  # CHR
    character_super_rare = "super rara de personaje"  # CSR
    art_rare = "rara de arte"  # AR
    special_art_rare = "rara de arte especial"  # SAR
    super_shiny_rare = "súper rara brillante"  # SSR
    ultra_rara = "ultra rara"  # UR
    hiper_rara = "híper rara"  # HR
    rara_secreta = "rara secreta"  # SR
    promocional = "promocional"  # PR

    # Rarezas históricas / específicas de sets
    radiant = "rara radiant"
    amazing_rare = "rara asombrosa"
    legendaria = "legendaria"  # LEGEND (2 piezas)
    prime = "rara prime"
    delta = "especie delta"
    ace_spec = "ace spec"

    # No son rarezas, pero se suelen tratar como tales por coleccionistas
    ex = "ex"
    gx = "gx"
    v = "v"
    vmax = "vmax"
    vstar = "vstar"
    tag_team = "tag team"
