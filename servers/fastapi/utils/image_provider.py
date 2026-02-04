from enums.image_provider import ImageProvider
from utils.get_env import (
    get_disable_image_generation_env,
    get_image_provider_env,
)
from utils.parsers import parse_bool_or_none


def is_image_generation_disabled() -> bool:
    return parse_bool_or_none(get_disable_image_generation_env()) or False


def is_pixabay_selected() -> bool:
    return get_image_provider_env() == ImageProvider.PIXABAY


def is_pixels_selected() -> bool:
    return get_image_provider_env() == ImageProvider.PEXELS


def is_gemini_flash_selected() -> bool:
    return get_image_provider_env() == ImageProvider.GEMINI_FLASH


def is_nanobanana_pro_selected() -> bool:
    return get_image_provider_env() == ImageProvider.NANOBANANA_PRO


def is_dalle3_selected() -> bool:
    return get_image_provider_env() == ImageProvider.DALLE3


def is_comfyui_selected() -> bool:
    return get_image_provider_env() == ImageProvider.COMFYUI


def is_gpt_image_1_5_selected() -> bool:
    return get_image_provider_env() == ImageProvider.GPT_IMAGE_1_5


def get_selected_image_provider() -> ImageProvider | None:
    """
    Get the selected image provider from environment variables.
    Returns:
        ImageProvider: The selected image provider.
    """
    image_provider_env = get_image_provider_env()
    if image_provider_env:
        return ImageProvider(image_provider_env)
    return None
