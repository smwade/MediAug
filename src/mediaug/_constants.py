"""Named constants for MediAug.

Mask encoding: cell masks use grayscale intensity values to distinguish
cytoplasm from nucleus regions. These are stored as RGB triplets where
all three channels have the same value.
"""

# Mask colors for cell regions (RGB triplets)
COLOR_CYTO_MASK: tuple[int, int, int] = (51, 51, 51)
COLOR_NUC_MASK: tuple[int, int, int] = (170, 170, 170)

# Grayscale equivalents for single-channel mask operations
CYTO_GRAY: int = 51
NUC_GRAY: int = 170

# Alpha blending values used during cell insertion.
# Cytoplasm gets a softer blend (160/255 ≈ 63% opacity) and
# nucleus gets a stronger blend (250/255 ≈ 98% opacity) so the
# nucleus remains visually distinct after compositing.
CYTO_BLEND_ALPHA: int = 160
NUC_BLEND_ALPHA: int = 250

# SIPaKMeD cell type names
SIPAKMED_CLASSES: list[str] = [
    "dyskeratotic",
    "koilocytotic",
    "metaplastic",
    "parabasal",
    "superficial-intermediate",
]
