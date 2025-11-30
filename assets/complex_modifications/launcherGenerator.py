import json
import os

class LauncherItem:
    def __init__(self, keyStroke: str, applicationName: str, hideIfOpen: bool = True):
        self.keyStroke = keyStroke
        self.applicationName = applicationName
        self.hideIfOpen = hideIfOpen

# region : Modify this only then run :  python3 assets/complex_modifications/launcherGenerator.py
fileName = 'launcher-generated.json'
launcherItems = [
    # Code editors
    LauncherItem("d", "CLion"),
    LauncherItem("v", "Visual Studio Code"),

    # Chat and Email
    LauncherItem("e", "Gmail.app"), 
    LauncherItem("c", "Telegram.app"), 

    LauncherItem("a", "ChatGPT"),
    LauncherItem("m","YouTube Music"),
    LauncherItem("s", "iTerm"),
    LauncherItem("g", "Google Chrome"),
    LauncherItem("l", "Obsidian"),
]
# endregion

# ------------------------------
# Helper: generate shell command for a launcher item
# ------------------------------
def create_shell_command(item: LauncherItem) -> str:
    if item.hideIfOpen:
        return (
            f"osascript -e 'tell application \"System Events\"' "
            f"-e 'if (name of first application process whose frontmost is true) "
            f"is \"{item.applicationName}\" then' "
            f"-e 'tell application process \"{item.applicationName}\" to set visible to false' "
            f"-e 'else' "
            f"-e 'do shell script \"open -a \\\"{item.applicationName}\\\"\"' "
            f"-e 'end if' "
            f"-e 'end tell'"
        )
    else:
        return f"open -a '{item.applicationName}'"

# ------------------------------
# Generate manipulators from launcher items
# ------------------------------
manipulators = []
for item in launcherItems:
    manipulators.append({
        "conditions": [
            {"name": "launcher_mode", "type": "variable_if", "value": 1}
        ],
        "from": {
            "key_code": item.keyStroke,
            "modifiers": {"optional": ["any"]}
        },
        "to": [
            {"shell_command": create_shell_command(item)},
            {"set_variable": {"name": "launcher_mode", "value": 0}}
        ],
        "type": "basic"
    })

# ------------------------------
# Full Karabiner JSON structure
# ------------------------------
karabiner_json = {
    "title": "Launcher",
    "rules": [
        {
            "description": "Double-tap Left Command to set Launcher mode",
            "manipulators": [
                {
                    "type": "basic",
                    "from": {
                        "key_code": "left_command",
                        "modifiers": {"optional": ["any"]}
                    },
                    "to": [
                        {"set_variable": {"name": "launcher_mode", "value": 1}}
                    ],
                    "conditions": [
                        {"type": "variable_if", "name": "key_pressed", "value": 1}
                    ]
                },
                {
                    "type": "basic",
                    "from": {
                        "key_code": "left_command",
                        "modifiers": {"optional": ["any"]}
                    },
                    "to": [
                        {"set_variable": {"name": "key_pressed", "value": 1}},
                        {"key_code": "left_command"}
                    ],
                    "description": "to_delayed_action is set to 5000 in karabiner.json",
                    "to_delayed_action": {
                        "to_if_invoked": [
                            {"set_variable": {"name": "key_pressed", "value": 0}}
                        ],
                        "to_if_canceled": [
                            {"set_variable": {"name": "key_pressed", "value": 0}}
                        ]
                    }
                }
            ]
        },
        {
            "description": "Launcher (Open): press keys to launch apps",
            "manipulators": manipulators
        }
    ]
}

# ------------------------------
# Write JSON to file
# ------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, fileName)

with open(file_path, "w") as f:
    json.dump(karabiner_json, f, indent=4)

print(f"Karabiner JSON written to {file_path}")