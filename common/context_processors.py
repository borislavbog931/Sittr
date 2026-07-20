from .translations import DEFAULT_LANGUAGE, get_translations


def language(request):
    lang = request.session.get("language", DEFAULT_LANGUAGE)
    return {
        "t": get_translations(lang),
        "current_language": lang,
    }
