# Create Anki decks for learning the standard chữ Hán Nôm

# TODO
- Tra cứu từ láy
- Tra cứu chữ phiên âm
- Tra cứu tên các quốc gia và vùng lãnh thổ trên thế giới

# 2025/11/21

-   Hey chat, I'm making a website to look up Han Nom characters. Why tf did the original site not have that in the first place?

## Overview

-   Seeks to improve votaquangnhat's generated Anki decks.
-   The source list is from https://www.hannom-rcv.org/.

Notes:

1. Characters in brackets are the simplified version (giản thể)
2. Uppercase means standard Sino-Vietnamese (Hán Việt) readings of Chinese characters; lowercase means the reading of the Nom character or the non-standard Sino-Vietnamese sounds of the Chinese character.

## Notable improvements

-   Cards' ordering based on order of apperance in the adjusted grading sheet.
    -   This is _huge_, because the old decks don't consider the order of apperance in the old grading list.
-   Nicer card formatting.
    -   Supported fonts embedding in the deck by default (Minh Nguyen for the front, Gothic Nguyen for the back).
-   Notes and grading infos in Anki notes and card's formatting.
    -   Grade 7: Characters in the level 2 list.
    -   Grade 8: Characters not included in either list.
-   Added Audio and Picture fields.
    -   Allow adding audios (i.e. generating using HyperTTS)
    -   Allow adding pictures to better illustrate the meaning of the character
