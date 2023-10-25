# Set up

## SD Keys, no set up needed. Read this repo for explanation

[Super Duper Keys Repo](https://github.com/jasonrudolph/keyboard)

## App launching

Can be done by pressing right ⌘ + any keys

### Current configuration

#### Left Home row

1. a - ai (chatgpt)
2. s - shell (iterm)
3. d - development (vscode)
4. f - chat app (feishu)
5. g - google chrome

#### Less frequently used

6. m - music
7. l - to do list

### Set up and tweaks

#### Chat gpt ( right ⌘ + A )

Settings > More tools > Create shortcut > Move from chrome apps to application (or set the path to use chrome app)

#### ( right ⌘ + f )

original > use

```json
{
    "shell_command": "open -a 'LarkSuite.app'"
}
```

the current version doubles as launcher and global search toggle. To set this up in lark
1. Go to lark > settings shortcut
2. Change Quick Search to ⌘ + shift + a
3. Change to use global shortcut