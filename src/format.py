def time_format(seconds) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    parts = []
    if h:
        parts.append(f'{h:.0f}h')
    if m:
        parts.append(f'{m:.0f}m')
    if s:
        parts.append(f'{s:.2f}s')
    return ' '.join(parts)


def sanitized_filename(filename: str) -> str:
    replacements = [
        (' --show-log-on-error', ''),  # irrelevant in filename
        (' --test=root', ''),  # irrelevant in filename
        (' -n', ''),  # irrelevant in filename
        (' -v', ''),  # irrelevant in filename
        ('%', ''),  # causes problems in web browsers
        (' ', '_'),  # causes problems in bash
    ]
    for old, new in replacements:
        filename = filename.replace(old, new)
    return filename