from enum import Enum

class TipoCartaEnum(str, Enum):
    pokemon = "pokemon"
    entrenador = "entrenador"
    energia = "energia"

class TipoEnergiaEnum(str, Enum):
    fuego = "fuego"
    agua = "agua"
    planta = "planta"
    incolora = "incolora"
    rayo = "rayo"
    psiquico = "psiquico"
    lucha = "lucha"
    oscura = "oscura"
    metalica = "metalica"
    hada = "hada"


class RarezaEnum(str, Enum):
    # Rarezas básicas
    comun = "común"
    poco_comun = "poco_común"
    rara = "rara"
    rara_holo = "rara_holográfica"
    doble_rara = "doble_rara"
    rara_ilustracion = "rara_de_ilustración"
    rara_ilustracion_especial = "rara_de_ilustración_especial"
    rara_brillante = "rara_brillante"  # Shiny Rare

    # Rarezas especiales (modernas)
    character_rare = "rara_de_personaje"  # CHR
    character_super_rare = "super_rara_de_personaje"  # CSR
    art_rare = "rara_de_arte"  # AR
    special_art_rare = "rara_de_arte_especial"  # SAR
    super_shiny_rare = "súper_rara_brillante"  # SSR
    ultra_rara = "ultra_rara"  # UR
    hiper_rara = "híper_rara"  # HR
    rara_secreta = "rara_secreta"  # SR
    promocional = "promocional"  # PR

    # Rarezas históricas / específicas de sets
    radiant = "rara_radiant"
    amazing_rare = "rara_asombrosa"
    legendaria = "legendaria"  # LEGEND (2 piezas)
    prime = "rara_prime"
    delta = "especie_delta"
    ace_spec = "ace_spec"

    # No son rarezas, pero se suelen tratar como tales por coleccionistas
    ex = "ex"
    gx = "gx"
    v = "v"
    vmax = "vmax"
    vstar = "vstar"
    tag_team = "tag_team"
