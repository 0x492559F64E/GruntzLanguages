### What to know

I'm not a professional translator. It's been a while since I worked with development tools and rarely use LLM models. But I have some time on my hands, I'm very firm with my languages, so why not give it a try to provide a first draft.

### Known Issues

The known issues are basically the same as with the Spanish translation. Some strings are too long for the UI, some strings are not exposed to the localisation file.
Often the translation reads kind of simplistic or poor in its given context, as the only maintainer I have for now decided to lean towards accuracy of the translations to avoid possible conflicts with the development side.
There is currently a mismatch in consistency of the use of ss/ß. At some point the entire file should be given a full pass to normalise this.

## Individual issues

Removed 'SHRINKAGE IS THEFT AND THEFT IS TREASON' from Register.TickerLine to stay within the character limit.
The ERT window text is not translatable and the button label does not fit inside.
Some hover texts would render inside their own frame, but not fit in the window containing them (e.g. ghost menu).
~I'm very unhappy with the translation for "Facehugs taken" to "Gesichtsklammern erhalten" but can't find a fitting translation right now either.~
"VEND" in vending machines does not have a direct equivalent. Two options would be BUY/KAUFEN or DISPENSE/AUSGEBEN. I went with the latter for now.

## Known missing translations

EmitterWindow.BriefBody
Surgery.WithAnAwfulTool
Surgery.WithAHackingTool
Surgery.BySurgeonProperToolsSuffix
Surgery.BySurgeonBestAvailableToolsSuffix
Surgery.About
Surgery.InAll
Surgery.LimbGoneClean
Surgery.Clean
Surgery.ACleanZone

9659
9146
73862
76886
77038

### Details

For the first translation pass the procedure was to check if any of the large online services could help me in this task. But they either had a low limit at requests/second or required an account. I considered testing if the VSCode CoPilot might be up to the task. The full procedure with queries, interactions and problems can be explained if desired.
In short I first extracted the strings and have it work in batches of 300 lines to manage the workload on the model. The translation was done line by line and so no data was lost or overlooked.
Then directed it to provide translations a game set in the aliens/ss13 franchise, to preserve proper names, formatting and placeholders. I've had it check the file multiple times for accuracy, consistency, grammatics and errors. And finally went over it myself for a while to give it a good but not complete check.

I've made a lot of manual edits to fix some details, provide translations for almeyer lockers, classes and end of rounds achievements. I have used my own experience, google translate, leo dictionary and google ai summary as a reference to decide when to go with a literal or figurative translation here.
Games have taken very different approaches to this here. Some leave achievements like "Apex Predator" in English and it might sound odd with a proper translation. However for the most part I felt it seemed more authentic to have them translated faithfully where possible. Only for "First Blood" (First one to die) it felt like any possible translation ("First casualty" would fit) would stray from the original source or create a possible conflict with future achievements, and since it's a common term in German games I left this one untranslated.

Generally I use all my applications and media in English so I'm not used to see the game in German. But so far the translations feel very natural. The codex helped me find some immediate mistakes, such as an incorrect translation for fracture and brute damage in odd places. Sometimes codex descriptions read in very simple terms (such as the medical procedure explanations). Right now I feel, translating them any more to provide more clarity would stray too far from the actual English source. As such I leave this as it is for someone else to work on, or translate as the text gets updated in the future.