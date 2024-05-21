import subprocess
import pyperclip
import sys

def get_selected_text(previous_text,mode):
    if sys.platform == "linux":
        text = pyperclip.paste()
        try:
            primary_text = (
                subprocess.check_output(["xclip", "-o", "-selection", "primary"])
                .decode("utf-8")
                .strip()
            )
        except:
            primary_text = ""
        if mode == "Mixed" and primary_text != "":
            text = primary_text
        elif mode == "Clip":
            pass
        elif mode == "Mouse" and primary_text != "":
            text = primary_text
    else:
        text = pyperclip.paste()   
    return text


def copy_to_clipboard(text):
    text = str(text)
    pyperclip.copy(text)
