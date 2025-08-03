#taskgen/renderer.py

def render(template: str, name: str, layer: str) -> str:
    return template.format(
        UP=name.upper(),
        low=name.lower(),
        layer=layer
    )