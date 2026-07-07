#!/usr/bin/env python3
"""Generate Bloc VS Code themes from palette definitions."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = ROOT / "themes"

PALETTES = {
    "Ash": ["#ACACAE", "#6E6E70", "#49494B", "#343436", "#2C2C2E", "#262628"],
    "Stone": ["#928B88", "#605E5E", "#363636", "#2A2A2A", "#19191A", "#0A0A0A"],
    "Slate": ["#CCCAD1", "#616565", "#3B403E", "#2B302E", "#1C2220", "#0C1212"],
    "Carbon": ["#DBDBDB", "#999999", "#5F6062", "#373839", "#1F1F20", "#0A0A0A"],
    "Midnight": ["#5D6880", "#3E4759", "#202937", "#14171E", "#0C1014", "#050304"],
    "Sand": ["#EBD49D", "#A4A4A4", "#777674", "#4B4A48", "#262625", "#131313"],
    "Graphite": ["#F7F7F7", "#C4C4C4", "#7F7F7F", "#404040", "#2E2E2E", "#232323"],
}

ACCENTS = {
    "Ash": {
        "keyword": "#7AA2F7",
        "operator": "#91B4F9",
        "string": "#98C379",
        "number": "#E5C07B",
        "function": "#56B6C2",
        "type": "#C678DD",
        "constant": "#E06C75",
        "tag": "#61AFEF",
        "property": "#8FB6F3",
        "parameter": "#6EC4CF",
        "variable": "#B8BAC0",
        "punctuation": "#7A7C80",
        "decorator": "#D19A66",
        "invalid": "#F7768E",
    },
    "Stone": {
        "keyword": "#89B4FA",
        "operator": "#9FC2FB",
        "string": "#A6D189",
        "number": "#E5C890",
        "function": "#8CAAEE",
        "type": "#CA9EE6",
        "constant": "#E78284",
        "tag": "#99D1DB",
        "property": "#A5C4F7",
        "parameter": "#7EB8D8",
        "variable": "#B5B0AC",
        "punctuation": "#787674",
        "decorator": "#EF9F76",
        "invalid": "#EA999C",
    },
    "Slate": {
        "keyword": "#7FB4CA",
        "operator": "#95C4D6",
        "string": "#A3BE8C",
        "number": "#EBCB8B",
        "function": "#88C0D0",
        "type": "#B48EAD",
        "constant": "#D08770",
        "tag": "#81A1C1",
        "property": "#94BFD4",
        "parameter": "#7ECAD8",
        "variable": "#B8BCC0",
        "punctuation": "#6E7472",
        "decorator": "#EBCB8B",
        "invalid": "#BF616A",
    },
    "Carbon": {
        "keyword": "#5EA1FF",
        "operator": "#7CB4FF",
        "string": "#78C47B",
        "number": "#F0B35E",
        "function": "#4FB8CC",
        "type": "#B684E0",
        "constant": "#E06A8D",
        "tag": "#6EA8FF",
        "property": "#8EB4FF",
        "parameter": "#67C6D4",
        "variable": "#C8C8C8",
        "punctuation": "#8A8B8D",
        "decorator": "#DDAA66",
        "invalid": "#FF6B6B",
    },
    "Midnight": {
        "keyword": "#82AAFF",
        "operator": "#9ABEFF",
        "string": "#C3E88D",
        "number": "#F78C6C",
        "function": "#89DDFF",
        "type": "#C792EA",
        "constant": "#FF5370",
        "tag": "#7FDBCA",
        "property": "#96B8FF",
        "parameter": "#7AD9F0",
        "variable": "#A8B0C0",
        "punctuation": "#5A6478",
        "decorator": "#F78C6C",
        "invalid": "#FF757F",
    },
    "Sand": {
        "keyword": "#8AB4F8",
        "operator": "#A0C3FA",
        "string": "#8FB573",
        "number": "#E6B566",
        "function": "#78A6C8",
        "type": "#B790C2",
        "constant": "#C97A63",
        "tag": "#6FA8DC",
        "property": "#A0C0F0",
        "parameter": "#86B8D4",
        "variable": "#C4C0B8",
        "punctuation": "#8A8884",
        "decorator": "#D8A15B",
        "invalid": "#D06D6D",
    },
    "Graphite": {
        "keyword": "#82AAFF",
        "operator": "#99BBFF",
        "string": "#A6E3A1",
        "number": "#F9E2AF",
        "function": "#89DCEB",
        "type": "#CBA6F7",
        "constant": "#F38BA8",
        "tag": "#74C7EC",
        "property": "#9EB8FF",
        "parameter": "#7EDCE8",
        "variable": "#D8D8D8",
        "punctuation": "#949494",
        "decorator": "#FAB387",
        "invalid": "#F38BA8",
    },
}


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02X}{g:02X}{b:02X}"


def with_alpha(color: str, alpha: int) -> str:
    return f"{color}{alpha:02X}"


def mix(a: str, b: str, ratio: float) -> str:
    ar, ag, ab = hex_to_rgb(a)
    br, bg, bb = hex_to_rgb(b)
    return rgb_to_hex(
        int(ar + (br - ar) * ratio),
        int(ag + (bg - ag) * ratio),
        int(ab + (bb - ab) * ratio),
    )


def build_colors(name: str, c1: str, c2: str, c3: str, c4: str, c5: str, c6: str) -> dict:
    text = resolve_text(c1)
    muted = c2
    border = c3
    surface = c4
    editor = c5
    chrome = c6

    return {
        "activityBar.background": chrome,
        "activityBar.foreground": text,
        "activityBarBadge.background": c3,
        "activityBarBadge.foreground": text,
        "badge.background": c3,
        "badge.foreground": text,
        "button.background": c3,
        "button.foreground": text,
        "debugTokenExpression.number": text,
        "debugTokenExpression.value": muted,
        "debugToolBar.background": surface,
        "debugView.stateLabelBackground": surface,
        "debugView.stateLabelForeground": text,
        "debugView.valueChangedHighlight": c3,
        "diffEditor.insertedTextBackground": with_alpha(mix(c3, "#FFFFFF", 0.35), 64),
        "diffEditor.removedTextBackground": with_alpha(mix(c3, "#000000", 0.35), 64),
        "dropdown.background": surface,
        "dropdown.listBackground": editor,
        "editor.background": editor,
        "editor.foreground": text,
        "editor.lineHighlightBackground": with_alpha(surface, 72),
        "editor.selectionBackground": with_alpha(c3, 96),
        "editor.selectionHighlightBorder": with_alpha(c2, 96),
        "editor.wordHighlightBackground": with_alpha(c3, 72),
        "editor.wordHighlightStrongBackground": with_alpha(c2, 72),
        "editorCursor.foreground": text,
        "editorGroup.border": chrome,
        "editorGroup.dropBackground": with_alpha(chrome, 160),
        "editorGroupHeader.tabsBackground": chrome,
        "editorWidget.foreground": text,
        "editorHoverWidget.background": surface,
        "editorHoverWidget.border": border,
        "editorIndentGuide.activeBackground": border,
        "editorIndentGuide.background": surface,
        "editorLineNumber.activeForeground": text,
        "editorLineNumber.foreground": muted,
        "editorSuggestWidget.background": surface,
        "editorSuggestWidget.border": border,
        "editorSuggestWidget.foreground": text,
        "editorSuggestWidget.highlightForeground": text,
        "editorSuggestWidget.selectedBackground": c3,
        "editorWhitespace.foreground": with_alpha(muted, 96),
        "editorWidget.background": surface,
        "editor.findMatchBackground": with_alpha(c3, 160),
        "editor.findMatchBorder": c2,
        "editor.findMatchHighlightBackground": with_alpha(c3, 96),
        "editor.findMatchHighlightBorder": border,
        "extensionButton.prominentBackground": c3,
        "extensionButton.prominentForeground": text,
        "extensionButton.prominentHoverBackground": c2,
        "focusBorder": c2,
        "gitDecoration.addedResourceForeground": mix(c1, "#A0A0A0", 0.5),
        "gitDecoration.modifiedResourceForeground": text,
        "gitDecoration.deletedResourceForeground": muted,
        "gitDecoration.untrackedResourceForeground": c2,
        "gitDecoration.ignoredResourceForeground": with_alpha(muted, 200),
        "gitDecoration.conflictingResourceForeground": mix(c1, c3, 0.5),
        "gitDecoration.submoduleResourceForeground": muted,
        "input.background": surface,
        "input.foreground": text,
        "input.border": border,
        "input.placeholderForeground": with_alpha(muted, 160),
        "inputOption.activeForeground": text,
        "inputOption.activeBackground": with_alpha(c3, 96),
        "inputOption.activeBorder": c2,
        "inputValidation.errorBackground": with_alpha(mix(c3, "#000000", 0.2), 128),
        "inputValidation.errorBorder": muted,
        "inputValidation.infoBackground": surface,
        "inputValidation.infoBorder": c2,
        "inputValidation.warningBackground": with_alpha(c3, 128),
        "inputValidation.warningBorder": c2,
        "list.activeSelectionBackground": c3,
        "list.activeSelectionForeground": text,
        "list.dropBackground": surface,
        "list.focusBackground": c3,
        "list.highlightForeground": text,
        "list.hoverBackground": surface,
        "list.hoverForeground": text,
        "list.inactiveSelectionBackground": c3,
        "list.inactiveSelectionForeground": text,
        "menu.background": surface,
        "menu.foreground": text,
        "notifications.foreground": text,
        "panel.border": chrome,
        "panelTitle.activeBorder": text,
        "panelTitle.activeForeground": text,
        "panelTitle.inactiveForeground": muted,
        "peekView.border": border,
        "peekViewEditor.background": editor,
        "peekViewEditor.matchHighlightBackground": with_alpha(c3, 128),
        "peekViewResult.background": surface,
        "peekViewResult.matchHighlightBackground": with_alpha(c3, 96),
        "peekViewResult.selectionBackground": c3,
        "peekViewTitle.background": chrome,
        "pickerGroup.foreground": text,
        "progressBar.background": c2,
        "selection.background": with_alpha(c3, 160),
        "settings.dropdownForeground": text,
        "settings.headerForeground": text,
        "settings.modifiedItemIndicator": text,
        "settings.numberInputBackground": surface,
        "settings.numberInputForeground": text,
        "settings.textInputBackground": surface,
        "settings.textInputForeground": text,
        "sideBar.background": chrome,
        "sideBar.foreground": text,
        "sideBarSectionHeader.background": chrome,
        "sideBarSectionHeader.foreground": text,
        "statusBar.background": surface,
        "statusBar.foreground": text,
        "statusBar.debuggingBackground": chrome,
        "statusBar.noFolderBackground": chrome,
        "statusBarItem.remoteBackground": c3,
        "tab.border": chrome,
        "tab.inactiveBackground": chrome,
        "tab.activeBorder": text,
        "tab.inactiveForeground": muted,
        "tab.activeForeground": text,
        "terminal.ansiBlack": chrome,
        "terminal.ansiBlue": c2,
        "terminal.ansiBrightBlack": c3,
        "terminal.ansiBrightBlue": c1,
        "terminal.ansiBrightCyan": text,
        "terminal.ansiBrightGreen": mix(c1, "#FFFFFF", 0.2),
        "terminal.ansiBrightMagenta": mix(c1, c2, 0.5),
        "terminal.ansiBrightRed": muted,
        "terminal.ansiBrightWhite": text,
        "terminal.ansiBrightYellow": c1,
        "terminal.ansiCyan": c2,
        "terminal.ansiGreen": mix(c2, c1, 0.4),
        "terminal.ansiMagenta": mix(c2, c3, 0.5),
        "terminal.ansiRed": mix(c2, "#000000", 0.2),
        "terminal.ansiWhite": text,
        "terminal.ansiYellow": c1,
        "titleBar.activeBackground": chrome,
        "titleBar.activeForeground": text,
        "titleBar.inactiveBackground": chrome,
        "titleBar.inactiveForeground": muted,
        "widget.shadow": "#00000080",
        **build_symbol_icon_colors(name, c1, c2, c3, c4, c5, c6),
    }


def build_symbol_icon_colors(name: str, c1: str, c2: str, c3: str, c4: str, c5: str, c6: str) -> dict:
    s = build_syntax_colors(name, c1, c2, c3, c4, c5, c6)

    return {
        "symbolIcon.arrayForeground": s["type"],
        "symbolIcon.booleanForeground": s["constant"],
        "symbolIcon.classForeground": s["class"],
        "symbolIcon.colorForeground": s["string"],
        "symbolIcon.constantForeground": s["constant"],
        "symbolIcon.constructorForeground": s["function"],
        "symbolIcon.enumeratorForeground": s["type"],
        "symbolIcon.enumeratorMemberForeground": s["constant"],
        "symbolIcon.eventForeground": s["property"],
        "symbolIcon.fieldForeground": s["property"],
        "symbolIcon.fileForeground": s["variable"],
        "symbolIcon.folderForeground": s["variable"],
        "symbolIcon.functionForeground": s["function"],
        "symbolIcon.interfaceForeground": s["interface"],
        "symbolIcon.keyForeground": s["property"],
        "symbolIcon.keywordForeground": s["keyword"],
        "symbolIcon.methodForeground": s["method"],
        "symbolIcon.moduleForeground": s["namespace"],
        "symbolIcon.namespaceForeground": s["namespace"],
        "symbolIcon.nullForeground": s["constant"],
        "symbolIcon.numberForeground": s["number"],
        "symbolIcon.objectForeground": s["type"],
        "symbolIcon.operatorForeground": s["operator"],
        "symbolIcon.packageForeground": s["namespace"],
        "symbolIcon.propertyForeground": s["property"],
        "symbolIcon.referenceForeground": s["variable"],
        "symbolIcon.snippetForeground": s["string"],
        "symbolIcon.stringForeground": s["string"],
        "symbolIcon.structForeground": s["type"],
        "symbolIcon.textForeground": s["variable"],
        "symbolIcon.typeParameterForeground": s["interface"],
        "symbolIcon.unitForeground": s["number"],
        "symbolIcon.variableForeground": s["variable"],
    }


def resolve_text(c1: str) -> str:
    return c1 if sum(hex_to_rgb(c1)) > 400 else "#E8E8E8"


def is_bright_palette(c1: str) -> bool:
    return sum(hex_to_rgb(c1)) > 400


def build_syntax_colors(name: str, c1: str, c2: str, c3: str, c4: str, c5: str, c6: str) -> dict[str, str]:
    text = resolve_text(c1)
    accent = ACCENTS[name]

    if is_bright_palette(c1):
        return {
            "default": c1,
            "keyword": accent["keyword"],
            "string": accent["string"],
            "number": accent["number"],
            "comment": c3,
            "function": accent["function"],
            "method": accent["function"],
            "type": accent["type"],
            "class": accent["type"],
            "interface": accent["type"],
            "enum": accent["type"],
            "struct": c1,
            "variable": accent["variable"],
            "parameter": accent["parameter"],
            "property": accent["property"],
            "tag": accent["tag"],
            "attribute": mix(accent["property"], accent["tag"], 0.45),
            "constant": accent["constant"],
            "operator": accent["operator"],
            "punctuation": accent["punctuation"],
            "escape": accent["number"],
            "regex": accent["string"],
            "namespace": accent["type"],
            "macro": accent["decorator"],
            "decorator": accent["decorator"],
            "label": c3,
            "invalid": accent["invalid"],
        }

    return {
        "default": text,
        "keyword": accent["keyword"],
        "string": accent["string"],
        "number": accent["number"],
        "comment": c2,
        "function": accent["function"],
        "method": accent["function"],
        "type": accent["type"],
        "class": accent["type"],
        "interface": accent["type"],
        "enum": accent["type"],
        "struct": text,
        "variable": accent["variable"],
        "parameter": accent["parameter"],
        "property": accent["property"],
        "tag": accent["tag"],
        "attribute": mix(accent["property"], accent["tag"], 0.45),
        "constant": accent["constant"],
        "operator": accent["operator"],
        "punctuation": accent["punctuation"],
        "escape": accent["number"],
        "regex": accent["string"],
        "namespace": accent["type"],
        "macro": accent["decorator"],
        "decorator": accent["decorator"],
        "label": c2,
        "invalid": accent["invalid"],
    }


def semantic_style(color: str, font_style: str | None = None) -> str | dict:
    if font_style:
        return {"foreground": color, "fontStyle": font_style}
    return color


def token(name: str | None, scope: str | list[str], settings: dict) -> dict:
    entry = {"scope": scope, "settings": settings}
    if name:
        entry["name"] = name
    return entry


def build_token_colors(name: str, c1: str, c2: str, c3: str, c4: str, c5: str, c6: str) -> list:
    s = build_syntax_colors(name, c1, c2, c3, c4, c5, c6)

    return [
        token(None, ["meta.embedded", "source.groovy.embedded", "meta.interpolation"], {"foreground": s["default"]}),
        token("Comment", ["comment", "comment.line", "comment.block", "comment.block.documentation", "punctuation.definition.comment"], {"foreground": s["comment"], "fontStyle": "italic"}),
        token("String", ["string", "string.quoted", "string.quoted.single", "string.quoted.double", "string.quoted.single.jsx", "string.quoted.double.jsx", "string.quoted.single.tsx", "string.quoted.double.tsx", "string.template", "string.template.jsx", "string.template.tsx", "string.interpolated", "string.other.link"], {"foreground": s["string"]}),
        token("String Escape", ["constant.character.escape", "constant.other.placeholder"], {"foreground": s["escape"], "fontStyle": "bold"}),
        token("Regexp", ["string.regexp", "constant.regexp"], {"foreground": s["regex"]}),
        token("Number", ["constant.numeric", "constant.numeric.integer", "constant.numeric.float", "constant.numeric.hex", "constant.numeric.binary", "constant.numeric.octal"], {"foreground": s["number"]}),
        token("Boolean", ["constant.language.boolean", "constant.language.true", "constant.language.false"], {"foreground": s["constant"], "fontStyle": "bold"}),
        token("Constant", ["constant.language", "constant.language.null", "constant.language.undefined", "constant.language.nan", "constant.other", "constant.character"], {"foreground": s["constant"]}),
        token("Keyword", ["keyword", "keyword.control", "keyword.control.flow", "keyword.control.conditional", "keyword.control.loop", "keyword.control.import", "keyword.control.export", "keyword.control.from", "keyword.control.as", "keyword.control.async", "keyword.control.await", "keyword.control.new", "keyword.control.return", "keyword.control.throw", "keyword.control.try", "keyword.control.catch", "keyword.control.finally", "keyword.control.switch", "keyword.control.case", "keyword.control.default", "keyword.control.break", "keyword.control.continue", "keyword.control.yield", "keyword.control.while", "keyword.control.for", "keyword.control.if", "keyword.control.else", "keyword.other", "keyword.other.important", "keyword.other.unit"], {"foreground": s["keyword"], "fontStyle": "bold"}),
        token("Operator", ["keyword.operator", "keyword.operator.new", "keyword.operator.expression", "keyword.operator.logical", "keyword.operator.assignment", "keyword.operator.arithmetic", "keyword.operator.comparison", "keyword.operator.rest", "keyword.operator.spread", "keyword.operator.type.annotation", "keyword.operator.optional", "keyword.operator.ternary"], {"foreground": s["operator"]}),
        token("Storage", ["storage", "storage.type", "storage.type.function", "storage.type.class", "storage.type.struct", "storage.type.enum", "storage.type.interface", "storage.type.primitive", "storage.modifier", "storage.modifier.import", "storage.modifier.package"], {"foreground": s["keyword"], "fontStyle": "bold"}),
        token("Template", ["punctuation.definition.template-expression", "punctuation.section.embedded", "meta.template.expression"], {"foreground": s["operator"]}),
        token("Variable", ["variable", "variable.other", "variable.other.readwrite", "variable.other.object"], {"foreground": s["variable"]}),
        token("Variable Property", ["variable.other.property"], {"foreground": s["property"]}),
        token("Variable Language", ["variable.language", "variable.language.this", "variable.language.self", "variable.language.super"], {"foreground": s["constant"], "fontStyle": "italic"}),
        token("Variable Constant", ["variable.other.constant", "variable.other.enummember"], {"foreground": s["constant"]}),
        token("Parameter", ["variable.parameter", "variable.parameter.function"], {"foreground": s["parameter"], "fontStyle": "italic"}),
        token("Function", ["entity.name.function", "meta.function-call entity.name.function", "meta.function entity.name.function", "support.function", "support.function.builtin", "support.function.misc", "support.function.dom", "support.function.console", "support.function.any-method"], {"foreground": s["function"], "fontStyle": "underline"}),
        token("Method", ["entity.name.function.member", "meta.method-call entity.name.function", "meta.method entity.name.function"], {"foreground": s["method"], "fontStyle": "underline"}),
        token("Class", ["entity.name.type", "entity.name.class", "entity.name.struct", "entity.name.enum", "entity.name.union", "entity.name.namespace", "entity.name.scope-resolution", "support.class", "support.type", "support.type.object"], {"foreground": s["class"], "fontStyle": "bold"}),
        token("Interface", ["entity.name.type.interface", "entity.name.type.alias", "entity.name.type.enum", "entity.name.type.parameter"], {"foreground": s["interface"], "fontStyle": "italic"}),
        token("Inherited", ["entity.other.inherited-class"], {"foreground": s["type"], "fontStyle": "italic underline"}),
        token("Type", ["storage.type.generic", "support.type.property-name", "support.type.builtin", "support.type.primitive"], {"foreground": s["type"], "fontStyle": "italic"}),
        token("Property", ["variable.other.property", "support.variable.property", "meta.object-literal.key", "meta.object-literal.key string", "meta.object-literal.key entity.name.tag", "string.unquoted.plain.out.yaml", "entity.name.tag.yaml"], {"foreground": s["property"]}),
        token("Tag", ["entity.name.tag", "entity.name.tag.localname", "meta.tag", "meta.tag.sgml"], {"foreground": s["tag"]}),
        token("TSX Component", ["support.class.component", "support.class.component.tsx", "support.class.component.jsx"], {"foreground": s["type"], "fontStyle": "bold"}),
        token("JSX Tag", ["entity.name.tag.jsx", "entity.name.tag.tsx"], {"foreground": s["tag"]}),
        token("JSX Attribute", ["entity.other.attribute-name.jsx", "entity.other.attribute-name.tsx", "entity.other.attribute-name.class.jsx", "entity.other.attribute-name.class.tsx"], {"foreground": s["attribute"]}),
        token("JSX Delimiter", ["punctuation.section.embedded.begin.jsx", "punctuation.section.embedded.end.jsx", "punctuation.section.embedded.begin.tsx", "punctuation.section.embedded.end.tsx"], {"foreground": s["operator"]}),
        token("Import Path", ["meta.import string.quoted", "string.quoted.double.import", "string.quoted.single.import"], {"foreground": s["string"]}),
        token("TypeScript Type", ["entity.name.type.alias.tsx", "entity.name.type.module.tsx", "support.type.primitive.tsx", "support.type.builtin.tsx", "support.type.primitive.ts", "support.type.builtin.ts", "entity.name.type.ts", "entity.name.type.tsx"], {"foreground": s["type"], "fontStyle": "italic"}),
        token("Type Primitive", ["support.type.primitive", "support.type.builtin"], {"foreground": s["type"], "fontStyle": "italic"}),
        token("Definition", ["meta.definition.variable", "meta.definition.function", "meta.definition.method", "meta.definition.property"], {"foreground": s["variable"]}),
        token("Member Access", ["variable.other.object.property", "variable.other.property.tsx", "variable.other.property.ts"], {"foreground": s["property"]}),
        token("React Hook", ["support.function.react", "support.variable.react"], {"foreground": s["function"], "fontStyle": "underline"}),
        token("Attribute", ["entity.other.attribute-name", "entity.other.attribute-name.class", "entity.other.attribute-name.id", "entity.other.attribute-name.pseudo-class", "entity.other.attribute-name.pseudo-element"], {"foreground": s["attribute"]}),
        token("CSS Property", ["support.type.property-name.css", "support.type.vendored.property-name.css"], {"foreground": s["property"]}),
        token("CSS Value", ["support.constant.property-value.css", "support.constant.color.w3c-standard-color-name.css"], {"foreground": s["constant"]}),
        token("CSS Selector", ["entity.name.tag.css", "entity.other.attribute-name.class.css", "entity.other.attribute-name.id.css"], {"foreground": s["tag"]}),
        token("JSON Key", ["support.type.property-name.json", "meta.object-literal.key string", "string.quoted.double.json punctuation", "meta.mapping.key.json"], {"foreground": s["property"]}),
        token("JSON String", ["meta.structure.dictionary.json string.quoted.double.json", "string.quoted.double.json"], {"foreground": s["string"]}),
        token("Python Decorator", ["meta.function.decorator.python entity.name.function", "entity.name.function.decorator.python", "punctuation.definition.decorator.python"], {"foreground": s["decorator"]}),
        token("Python Magic", ["support.function.magic.python", "support.variable.magic.python"], {"foreground": s["function"]}),
        token("Rust Macro", ["entity.name.function.macro.rust", "support.function.macro.rust"], {"foreground": s["macro"]}),
        token("Go Package", ["entity.name.package.go"], {"foreground": s["namespace"]}),
        token("Shell Shebang", ["comment.line.shebang", "comment.line.shebang punctuation"], {"foreground": s["comment"], "fontStyle": "italic"}),
        token("Markdown Heading", ["markup.heading", "markup.heading.1", "markup.heading.2", "markup.heading.3", "markup.heading.4", "markup.heading.5", "markup.heading.6", "markup.heading.setext"], {"foreground": s["function"], "fontStyle": "bold"}),
        token("Markdown Bold", ["markup.bold"], {"foreground": s["default"], "fontStyle": "bold"}),
        token("Markdown Italic", ["markup.italic"], {"foreground": s["default"], "fontStyle": "italic"}),
        token("Markdown Link", ["markup.underline.link", "string.other.link", "markup.underline.link.markdown"], {"foreground": s["string"], "fontStyle": "underline"}),
        token("Markdown Code", ["markup.inline.raw", "markup.fenced_code.block", "markup.raw.block"], {"foreground": s["constant"]}),
        token("Markdown Quote", ["markup.quote"], {"foreground": s["comment"], "fontStyle": "italic"}),
        token("Markdown List", ["markup.list", "punctuation.definition.list.begin"], {"foreground": s["operator"]}),
        token("Diff", ["meta.diff", "meta.diff.header"], {"foreground": s["comment"]}),
        token("Diff Deleted", ["markup.deleted"], {"foreground": s["invalid"]}),
        token("Diff Inserted", ["markup.inserted"], {"foreground": s["function"]}),
        token("Diff Changed", ["markup.changed"], {"foreground": s["string"]}),
        token("Invalid", ["invalid", "invalid.illegal"], {"foreground": s["invalid"], "fontStyle": "underline"}),
        token("Deprecated", ["invalid.deprecated"], {"foreground": s["comment"], "fontStyle": "strikethrough"}),
        token("Punctuation", ["punctuation", "punctuation.separator", "punctuation.terminator", "punctuation.accessor", "punctuation.definition.block", "punctuation.definition.parameters", "punctuation.definition.arguments", "punctuation.definition.array", "punctuation.definition.string", "punctuation.section", "meta.brace"], {"foreground": s["punctuation"]}),
        token("Bracket", ["punctuation.definition.tag", "punctuation.definition.tag.begin", "punctuation.definition.tag.end"], {"foreground": s["operator"]}),
        token("Find in Files", ["constant.numeric.line-number.find-in-files - match", "entity.name.filename.find-in-files"], {"foreground": s["number"]}),
        token("Log Tokens", ["token.info-token"], {"foreground": s["function"]}),
        token("Log Warn", ["token.warn-token"], {"foreground": s["string"]}),
        token("Log Error", ["token.error-token"], {"foreground": s["invalid"]}),
        token("Log Debug", ["token.debug-token"], {"foreground": s["comment"]}),
        # SQL
        token("SQL Keyword", ["keyword.other.DML.sql", "keyword.other.DDL.sql", "keyword.other.sql"], {"foreground": s["keyword"], "fontStyle": "bold"}),
        token("SQL Function", ["support.function.aggregate.sql", "support.function.scalar.sql"], {"foreground": s["function"]}),
        token("SQL Table", ["entity.name.type.table.sql"], {"foreground": s["type"], "fontStyle": "italic"}),
        token("SQL Column", ["entity.name.type.column.sql"], {"foreground": s["property"]}),
        # Java / Kotlin / Scala
        token("JVM Annotation", ["storage.type.annotation.java", "storage.type.annotation.kotlin", "meta.annotation.scala"], {"foreground": s["decorator"], "fontStyle": "bold"}),
        token("JVM Package", ["entity.name.namespace.java", "entity.name.package.kotlin", "entity.name.namespace.scala"], {"foreground": s["namespace"]}),
        token("JVM Generic", ["entity.name.type.parameter.java", "entity.name.type.parameter.kotlin", "entity.name.type.parameter.scala"], {"foreground": s["type"], "fontStyle": "italic"}),
        # C / C++ / C#
        token("C Preprocessor", ["meta.preprocessor", "keyword.control.directive", "entity.name.function.preprocessor"], {"foreground": s["decorator"], "fontStyle": "bold"}),
        token("C++ Scope Resolution", ["keyword.operator.scope-resolution.cpp"], {"foreground": s["operator"]}),
        token("C# Attribute", ["entity.name.type.class.attribute-name.cs"], {"foreground": s["decorator"], "fontStyle": "bold"}),
        # Rust / Go
        token("Rust Lifetime", ["storage.modifier.lifetime.rust"], {"foreground": s["type"], "fontStyle": "italic"}),
        token("Rust Trait", ["entity.name.type.trait.rust"], {"foreground": s["type"], "fontStyle": "italic"}),
        token("Go Builtin", ["support.function.builtin.go", "support.type.builtin.go"], {"foreground": s["function"]}),
        # Python
        token("Python Type Hints", ["meta.function.parameters.python support.type", "meta.annotation.python"], {"foreground": s["type"], "fontStyle": "italic"}),
        token("Python Self", ["variable.parameter.function.language.special.self.python", "variable.language.special.self.python"], {"foreground": s["constant"], "fontStyle": "italic"}),
        # PHP / Ruby / Elixir
        token("PHP Variable", ["variable.other.php"], {"foreground": s["variable"]}),
        token("PHP Namespace", ["support.other.namespace.php"], {"foreground": s["namespace"]}),
        token("Ruby Symbol", ["constant.other.symbol.ruby"], {"foreground": s["constant"]}),
        token("Elixir Atom", ["constant.other.symbol.elixir"], {"foreground": s["constant"]}),
        # Swift
        token("Swift Attribute", ["keyword.other.attribute.swift"], {"foreground": s["decorator"], "fontStyle": "bold"}),
        token("Swift Type", ["entity.name.type.swift", "support.type.swift"], {"foreground": s["type"], "fontStyle": "italic"}),
        # Shell / Docker / Makefile
        token("Shell Variable", ["variable.other.normal.shell", "variable.parameter.positional.shell"], {"foreground": s["variable"]}),
        token("Shell Command", ["support.function.builtin.shell", "support.function.alias.shell"], {"foreground": s["function"]}),
        token("Docker Instruction", ["keyword.other.special-method.dockerfile"], {"foreground": s["keyword"], "fontStyle": "bold"}),
        token("Makefile Target", ["entity.name.function.target.makefile"], {"foreground": s["function"], "fontStyle": "underline"}),
        # YAML / TOML / INI
        token("YAML Key", ["entity.name.tag.yaml", "meta.mapping.key.yaml"], {"foreground": s["property"]}),
        token("YAML Anchor", ["entity.name.type.anchor.yaml"], {"foreground": s["decorator"]}),
        token("TOML Key", ["support.type.property-name.table.toml", "support.type.property-name.toml"], {"foreground": s["property"]}),
        token("INI Section", ["entity.name.section.group-title.ini"], {"foreground": s["type"], "fontStyle": "bold"}),
        # Web / config
        token("GraphQL Type", ["entity.name.type.graphql"], {"foreground": s["type"], "fontStyle": "italic"}),
        token("GraphQL Field", ["entity.name.field.graphql"], {"foreground": s["property"]}),
        token("GraphQL Directive", ["entity.name.function.directive.graphql"], {"foreground": s["decorator"], "fontStyle": "bold"}),
        token("Lua Function", ["support.function.lua", "entity.name.function.lua"], {"foreground": s["function"]}),
        token("HCL Block", ["entity.other.attribute-name.block.hcl", "entity.name.block.hcl"], {"foreground": s["type"]}),
        token("Regex Charset", ["constant.other.character-class.regexp"], {"foreground": s["number"]}),
        token("Punctuation Comma", ["punctuation.separator.comma"], {"foreground": s["punctuation"]}),
        token("Punctuation Dot", ["punctuation.accessor.dot"], {"foreground": s["punctuation"]}),
    ]


def build_semantic_token_colors(name: str, c1: str, c2: str, c3: str, c4: str, c5: str, c6: str) -> dict:
    s = build_syntax_colors(name, c1, c2, c3, c4, c5, c6)

    return {
        "variable": s["variable"],
        "variable.readonly": semantic_style(s["constant"], "italic"),
        "variable.defaultLibrary": semantic_style(s["function"], "underline"),
        "property": s["property"],
        "property.readonly": s["constant"],
        "function": semantic_style(s["function"], "underline"),
        "method": semantic_style(s["method"], "underline"),
        "function.declaration": semantic_style(s["function"], "bold underline"),
        "method.declaration": semantic_style(s["method"], "bold underline"),
        "class": semantic_style(s["type"], "bold"),
        "class.declaration": semantic_style(s["type"], "bold"),
        "interface": semantic_style(s["interface"], "italic"),
        "interface.declaration": semantic_style(s["interface"], "italic"),
        "enum": semantic_style(s["type"], "italic"),
        "enumMember": s["constant"],
        "struct": semantic_style(s["type"], "bold"),
        "type": semantic_style(s["type"], "italic"),
        "typeParameter": semantic_style(s["interface"], "italic"),
        "parameter": semantic_style(s["parameter"], "italic"),
        "namespace": s["namespace"],
        "macro": semantic_style(s["macro"], "bold"),
        "keyword": semantic_style(s["keyword"], "bold"),
        "comment": semantic_style(s["comment"], "italic"),
        "string": s["string"],
        "number": s["number"],
        "regexp": s["regex"],
        "operator": s["operator"],
        "decorator": semantic_style(s["decorator"], "bold"),
        "member": s["property"],
        "member.readonly": s["constant"],
        "member.defaultLibrary": semantic_style(s["function"], "underline"),
        "event": s["property"],
        "modifier": semantic_style(s["keyword"], "bold"),
        "label": s["label"],
        "builtinType": semantic_style(s["type"], "italic"),
        "selfKeyword": semantic_style(s["constant"], "italic"),
        "property.defaultLibrary": s["property"],
        "enumMember.defaultLibrary": s["constant"],
        "parameter.readonly": semantic_style(s["parameter"], "italic"),
        "namespace.defaultLibrary": s["namespace"],
        "variable.global": s["variable"],
        "variable.local": s["variable"],
        "string.escape": s["escape"],
        "type.defaultLibrary": semantic_style(s["type"], "italic"),
        "class.defaultLibrary": semantic_style(s["type"], "bold"),
        "*.declaration": semantic_style(s["function"], "bold underline"),
        "*.definition": semantic_style(s["function"], "bold underline"),
        "*.readonly": semantic_style(s["constant"], "italic"),
        "*.static": semantic_style(s["constant"], "italic"),
        "*.async": semantic_style(s["keyword"], "bold"),
        "*.deprecated": semantic_style(s["comment"], "strikethrough"),
    }


def muted_error(color: str) -> str:
    r, g, b = hex_to_rgb(color)
    return rgb_to_hex(max(0, r - 40), max(0, g - 20), max(0, b - 20))


def build_theme(name: str, palette: list[str]) -> dict:
    c1, c2, c3, c4, c5, c6 = palette

    return {
        "$schema": "vscode://schemas/color-theme",
        "name": f"Bloc {name}",
        "type": "dark",
        "semanticHighlighting": True,
        "colors": build_colors(name, c1, c2, c3, c4, c5, c6),
        "tokenColors": build_token_colors(name, c1, c2, c3, c4, c5, c6),
        "semanticTokenColors": build_semantic_token_colors(name, c1, c2, c3, c4, c5, c6),
    }


def main() -> None:
    THEMES_DIR.mkdir(parents=True, exist_ok=True)

    legacy = THEMES_DIR / "Bloc-color-theme.json"
    if legacy.exists():
        legacy.unlink()

    for name, palette in PALETTES.items():
        slug = name.lower()
        path = THEMES_DIR / f"bloc-{slug}.json"
        theme = build_theme(name, palette)
        path.write_text(json.dumps(theme, indent="\t") + "\n", encoding="utf-8")
        print(f"Wrote {path.name}")


if __name__ == "__main__":
    main()
