def read_file(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def read_enterprise_updates(file_path, query):
    file_data = read_file(file_path)
    if file_data.startswith("Error reading file:"):
        return file_data

    query_terms = [term.lower() for term in query.split() if len(term) > 3]
    matched_lines = []

    for line in file_data.splitlines():
        lower_line = line.lower()
        if any(term in lower_line for term in query_terms):
            matched_lines.append(line)

    if matched_lines:
        return "\n".join(matched_lines[:8])

    return "\n".join(file_data.splitlines()[:8])