import os
import sys


def replace_text_editor() -> None:
    """
    [TEST] replace data of replace_parameters.py
    """
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        raise Exception

    if mode == "forward":
        replace_text = (
            'NOTION_PAGE_URL = "https://www.notion.so/Notion-replace-test-page-69ee55888ed24158b687f16b13fd6e9f"\n'
            + 'BEFORE_TEXT = "AAA"\n'
            + 'AFTER_TEXT = "ZZZ"\n'
        )
    elif mode == "backward":
        replace_text = (
            'NOTION_PAGE_URL = "https://www.notion.so/Notion-replace-test-page-69ee55888ed24158b687f16b13fd6e9f"\n'
            + 'BEFORE_TEXT = "ZZZ"\n'
            + 'AFTER_TEXT = "AAA"\n'
        )
    else:
        raise Exception
    with open(os.path.join("..", "replace_parameters.py"), "w", encoding="utf-8") as f:
        f.write(replace_text)


if __name__ == "__main__":
    replace_text_editor()
