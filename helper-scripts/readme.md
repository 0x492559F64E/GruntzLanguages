# Collection of scripts and tips

Currently this guide assumes you know how to use VSCode to manage files and use git. Use the "chat" window on the right side to ask copilot for help with any of these features or tasks when stuck. To use the following prompts with high workloads, use the "Open in Agents (ctrl+shift+A)" window as it will provide you with more space and details on the running work processes.

## Scripts for language file handling

When using LLM to translate, I recommend to only feed it the raw lines without the xml to avoid confusion.

The extraction script `extract_resx_values.py` will put all values contents in a newline in one textfile. easy for an LLM to work with. It will create a second file for all name tags of the data node. By aligning both files the translated values can quickly and easily be reinserted when the work process requires that the strings are not in order or only a subset of the language file.

Reinsert with the `restore_resx_values.py` script, which puts all values from the values file back into the xml in order of appearance. Or use the `restore_rex_values_byID.py` script which takes both aforementioned files to insert by matching its data name ID. Which means for that script the order doesn't matter - but note that ofc the linenumber of the value/ID pair in the respective files need to match up. Which they will as long as you don't manually add/remove newlines.

The scripts look for a file called `syncversion.txt` in the repository root. If they find one they will append that version string to the file name. I save the last game version that I worked on in this file.

## Work flow and dealing with untranslated entries

### Identical value/comment pairs

When you start initial translation work on the language file you will have a great deal of untranslated entries left over. Clearly all data nodes where the `value` and `comment` fields are identical are untranslated. But you will no doubt eventually decide to leave some entries untranslated on purpose. To avoid later problems you should start work on an empty translation file. Meaning: You generate your first language file with the `languages generate <lang>` command ingame, then create a new file with the header of that xml (everything up to the first data node), and then only copy those data nodes to this new file that you want to submit to translation. Assuming you work with individual strings. When using a half-automated approach as outlined below you will need to make sure to finish the entire file before trying to merge it with a new version.

You can use the `find_ident_commentValue.py` script to get a list of all untranslated values without the surrounding xml. This can help you in finding strings that you wanted to translate but haven't yet for whatever reason. If you intent to leave them untranslated for now (like I currently do with `EmitterWindow.BriefBody`), delete the full data node from your language file before submitting it for a pull request. Doing this ensures that you can run `languages missing` to get a list of all untranslated strings that still need to be translated. When using this workflow, use the ingame command `languages merge <lang> <full path to missing file>` to merge your new translations into the game file. Use the following command to find all unique strings in the commentValue output file:

```Powershell
Get-Content .\<langFolder>\<lang>_ident_commentValue.txt | Select-Object -Unique
```

### Find an already translated value for which the original text has changed

In order to find strings whose orginal text has changed in an update, use a diff-tool to find all values where the `comment` tag has changed. Meaning: You have your own language file in your working directory, generate a new language file for the current game version ingame with the console with `languages generate <lang>` again, then compare both files. In VSCode you right-click on one file first and pick "Select for Compare" then on the other file "Compare with Selected". The diff-window has a button where you can easily jump to each individual change and review them.

### Notes

 Don't forget to update your working directory file with translations that you made ingame when using the `languages edit on` feature. The diff-tool workflow helps in this task.

 It can make sense to save a list of all strings that you didn't translate on purpose. In case of large changes or something in your work flow mixed up. To do this, once you have a file that contains only values you have translated, including intentionally untranslated values, use the `find_ident_commentValue.py` script on it and save the file with a descriptive title like "intentionally-untranslated".

## Using automated translation tools

### Short guide to using VSCode+Codepilot for half-automated translation

So of course there are many offers for LLM translation out there. And even Deepl would suffice, if you make an account with them. I however already have a Microsoft and Github account from development in the past. So using them comes naturally to me.
I figured the new Copilot should be able to translate it without external services. But when asking it, it tried to contact Google Translate and Deepl. So it took a while of playing around with the prompt until I got one that gave me a satisfactory result.

#### General high volume changes

The following prompt is now my default starting point for larger changes. I have it saved in a textfile in the same directory as my translation files called, excluded via gitignore from release and direct the LLM to translate using this file as a guideline. For the first initial translation, I will make a separate post right after because it's a special case.

```Text
I want you to translate from English to German here in copilot without contacting an external service.
Formatting like full capitalisation or // for text structure need to be kept.
The text contains special keywords in curly brackets, they need to be kept in the final translation at the same position.
The text contains the comma and decimal formatting typical for English text; German uses the dot (.) as a thousands separator, and the comma (,) as a decimal separator.
Note that the text contains proper names from the Aliens universe, like "w-y net", weyland-yutani or xenomorph and the SS13 games.
When using a hyphen to connect words make sure it's the actual "-" and not a similar looking version.

Explain to me any problems or conflicts with this prompt, or continue and show me an example of the first 50 lines. Ask me to finish the rest of file.
```

#### Special case: Translation of the entire language file for the first time

The first draft of the entire file is a problem because of its length and the default model it used on my machine was Luna, which is rather simplistic.

So, either do it yourself or ask the model first to extract the value entries from the xml to a simple plaintext file. One line per entry.
There is the special case that the first two entries are empty. For a 1:1 replacement back into the xml they should be kept as empty newlines in the text file too.

After that you can use a slightly modified version of above to start the process.

It will ask MANY times for confirmation of what to do. in my case easily 100 times. I had to check a lot while it was working. But eventually it got everything right. After that I did a couple of passes asking it to check the entire file for consistency (how german reader will perceive it; franchise context), errors, grammatics, hyphen mistakes. And such. At least 3 passes. And went over it myself for about 2 hours.

```Text
I want you to translate <this file> from English to German here in copilot without contacting an external service.
Each line is its own string for a UI label in the game.
Formatting like full capitalisation or // for text structure need to be kept.
The text contains special keywords in curly brackets, they need to be kept in the final translation at the same position.
The text contains the comma and decimal formatting typical for English text; German uses the dot (.) as a thousands separator, and the comma (,) as a decimal separator.
Note that the text contains proper names from the Aliens universe, like "w-y net", weyland-yutani or xenomorph and the SS13 games.
When using a hyphen to connect words make sure it's the actual "-" and not a similar looking version.

The file is very large, it contains <lines> with <number of characters>. Separate work into batches.

Explain to me any problems or conflicts with this prompt, or continue and show me an example of the first 50 lines. Ask me to finish the rest of file.```
