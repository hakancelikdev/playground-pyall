import traceback

import panel as pn
from pyall.analyzer import Analyzer
from pyall.refactor import refactor_source


def refactor(source: str) -> str:
    analyzer = Analyzer(source=source)
    analyzer.traverse()

    return refactor_source(source, analyzer.expected_all)


def run_refactor(source: str) -> pn.widgets.Ace:
    try:
        refactored_source = refactor(source)
        language = "python"
    except Exception:
        refactored_source = traceback.format_exc()
        language = "text"

    return pn.widgets.Ace(
        value=refactored_source,
        language=language,
        readonly=True,
    )


pn.config.sizing_mode = "stretch_both"
pn.extension()


example_source_code = """\
class PublicKlass:
    pass

class _PrivateKlass:
    pass

class __PrivateKlass:
    pass

def public_func():
    pass

def _private_func():
    pass

def __private_func2():
    pass

PUBLIC_VARIABLE = 1

private_variable = 2
_private_variable = 3
__private_variable = 4
"""

source_editor = pn.widgets.Ace(value=example_source_code, language="python")
result_editor = pn.bind(run_refactor, source_editor)


docs_button = pn.widgets.Button(name="Go to docs", button_type="primary", width=100)
docs_button.js_on_click(code="window.open('https://pyall.hakancelik.dev')")
github_button = pn.widgets.Button(name="GitHub", button_type="primary", width=100)
github_button.js_on_click(code="window.open('https://github.com/hakancelikdev/pyall')")

app_row = pn.Row(source_editor, result_editor)

bootstrap = pn.template.MaterialTemplate(title="Try Pyall")
bootstrap.header.append(pn.Row(docs_button, github_button))
bootstrap.main.append(app_row)
bootstrap.servable()
