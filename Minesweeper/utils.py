

def make_sectional_content(data : list) -> list:
    sections = []
    section = []
    for item in data:
        if item == "~~~":
            sections.append(section)
            section = []
            continue
        section.append(item)
    
    return sections


def print_sectional_content(sections : list) -> None:
    for section in sections:
        for item in section:
            print(item)
        input("Enter to continue...")