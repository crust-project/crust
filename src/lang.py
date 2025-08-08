def detect(code: str) -> str:
    code = code.replace('"', "'").strip()

    python_keywords = ['def ', 'import ', 'print(', 'class ', 'self', 'lambda']
    bash_keywords   = ['#!/bin/bash', 'echo ', 'fi', 'then', '$(', '${', '[[', ']]']
    zsh_keywords    = ['#!/bin/zsh', 'autoload', 'zmodload', 'bindkey', 'compdef']
    fish_keywords   = ['#!/usr/bin/env fish', 'function ', 'set ', 'end', 'for ', 'in ']

    code_lc = code.lower()

    scores = {
        'python3': sum(kw in code for kw in python_keywords),
        'bash':   sum(kw in code for kw in bash_keywords),
        'zsh':    sum(kw in code for kw in zsh_keywords),
        'fish':   sum(kw in code for kw in fish_keywords),
    }

    print(scores)

    lang = max(scores, key=scores.get)
    if scores[lang] == 0:
        return "bash"
    return lang

