import json

from pygments import highlight, lexers, formatters


# Colorful JSON to terminal out
def format_json(data):
    formatted = json.dumps(data, sort_keys=True, indent=4)
    colorful = highlight(
        unicode(formatted, 'UTF-8'),
        lexers.JsonLexer(),
        formatters.TerminalFormatter()
    )
    print colorful
