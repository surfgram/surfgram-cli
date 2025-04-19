from rich.style import Style


class UIConfig:
    """Centralized configuration for UI styles and settings"""

    # Color palette
    ORANGE = "rgb(255,165,0)"
    DEEP_ORANGE = "rgb(255,140,0)"
    CORAL = "rgb(255,127,80)"
    STEEL_BLUE = "rgb(70,130,180)"
    SEA_GREEN = "rgb(46,139,87)"
    CRIMSON = "rgb(178,34,34)"

    # UI Styles
    BANNER_STYLE = Style(color=ORANGE, bold=True)
    BORDER_STYLE = Style(color=DEEP_ORANGE)
    FRAMEWORK_STYLE = Style(color=CORAL, italic=True)
    ACCENT_STYLE = Style(color=STEEL_BLUE, bold=True)
    SUCCESS_STYLE = Style(color=SEA_GREEN, bold=True)
    ERROR_STYLE = Style(color=CRIMSON, bold=True)

    # Banner settings
    BANNER_FONT = "slant"
    SEPARATOR_LENGTH = 50
    FRAMEWORK_DESCRIPTION = "🌊 Like a surfer on the waves"
