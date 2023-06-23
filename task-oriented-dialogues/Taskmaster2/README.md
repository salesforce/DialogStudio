# COPYRIGHT NOTICE

This is the work of Bill Byrne, Karthik Krishnamoorthi, Saravanan Ganesh, Amit Dubey, Kyu-Young Kim and Andy Cedilnik from Google LLC, made available under the Creative Commons Attribution 4.0 License. A full copy of the license can be found at https://creativecommons.org/licenses/by/4.0/

# DATA

## NUMBERS
The Taskmaster-2 dataset consists of 17,289 dialogs in the seven domains below. Dialogs for each domain can be found in the seven json files located in this directory's "data" folder, i.e. Taskmaster/TM-2-2-20/data/.
* restaurants (3276)
* food ordering (1050)
* movies (3047)
* hotels (2355)
* flights (2481)
* music (1602)
* sports (3478)

## STRUCTURE
Each conversation in the data file has the following structure:
* __conversation_id:__ A universally unique identifier with the prefix 'dlg-'. The ID has no meaning.
* __utterances:__ An array of utterances that make up the conversation.
* __instruction_id:__ A reference to the file(s) containing the user (and, if applicable, agent) instructions for this conversation.

Each utterance has the following fields:
* __index:__ A 0-based index indicating the order of the utterances in the conversation.
* __speaker:__ Either USER or ASSISTANT, indicating which role generated this utterance.
* __text:__ The raw text of the utterance. 'ASSISTANT' turns are originally written (then played to the user via TTS) and 'USER' turns are transcribed from the spoken recordings of crowdsourced workers.
* __segments:__ An array of various text spans with semantic annotations.

Each segment has the following fields:
* __start_index:__ The position of the start of the annotation in the utterance text.
* __end_index:__ The position of the end of the annotation in the utterance text.
* __text:__ The raw text that has been annotated.
* __annotations:__ An array of annotation details for this segment.

Each annotation has a single field:
* __name:__ The annotation name.

## COLLECTION METHODOLOGY
Unlike [Taskmaster-1](../TM-1-2019), which includes both written "self-dialogs" and spoken two-person dialogs, Taskmaster-2 consists entirely of spoken two-person dialogs. In addition, while Taskmaster-1 is almost exclusively task-based, Taskmaster-2 contains a good number of search- and recommendation-oriented dialogs, as seen for example in the restaurants, flights, hotels, and movies verticals. The music browsing and sports conversations are almost exclusively search- and recommendation-based. 
All dialogs in this release were created using a Wizard of Oz (WOz) methodology in which crowdsourced workers played the role of a 'user' and trained call center operators played the role of the 'assistant'. In this way, users were led to believe they were interacting with an automated system that “spoke” using text-to-speech (TTS) even though it was in fact a human behind the scenes. As a result, users could express themselves however they chose in the context of an automated interface. 

## INSTRUCTIONS
As with Taskmaster-1, crowdsourced workers and agents alike were given instructions prior to being connected in order to set up the role play scenario and to explain additional details. In most cases users and assistants alike were given free reign to make the conversation as realistic and typical as possible by basing their ideas and results on real flight data from the Internet instead of being restricted to a small knowledge base. However, in some cases certain variables such as location were restrcited to a handful of choices to make it easier for the worker playing 'assistant' to respond results in a rasonable time frame. In other words, knowing ahead of time which cities are in play for a given search makes it easier to anticipate and search for results. Note that, even though dialogs for each domain are consolidated in just one json file, there are actually many versions of each type of dialog which correspond to slight variations in the instructions. You can identify each set within a given domain by searching for "instruction_id". For example, in food ordering Below we give additional details about the instructions for each domain:
* **Restaurants**: Most dialogs in this set involve the user asking for recommendations for a particular type of cuisine in a given city. Users were asked to ask for  2-3 choices up front and then compare them by asking the assistant questions about price, atmosphere, menu items and the like.
* **Food ordering**: Users pretended they were ordering take-out using an automated assistant for a particular cuisine choice. (One cuisine was randomly generated for each set of instruction to ensure variety.) They discussed dishes or items, size, toppings, etc.
* **Hotels**: As with flights below, users choose from a list of cities to anchor their search. They are encouraged to compare several different hotels using typical preferences such as ratings, price, availability, and other amenities.
* **Flights**: Users typically choose from a list of cities or continents for round trip or multi-city flights and based their final choice on a number of additional preferences such as dates, flight time, price, layovers, seating class, airline, etc.
* **Movies**: This domain consists mostly of recommendation dialogs where users are trying to find a movie to watch in theaters or using a streaming service at home. 
  * In theaters: instruction_id = movie-{2-7, 9-12 14-15, 17, 20-22, 24e, 25-26, 30, 31e, 33e}
  * At home: instruction_id = movie-{8, 18, 19, 27-29}
* **Music**: For the music domain, users were asked to browse (i.e. listen to) several tracks based on their choice of artist, track, album, or genre, and then comment on each one. To recommend tracks, agents were able to send users Youtube videos which they in turn could control once launched. The dialogs do not include when the links, however.
* **Sports**: Sports dialogs are informational conversations discussing facts and stats about players, teams, games, etc. in the English Premiere League (EPL), Major Leage Baseball, Major League Soccer, National Basketball Association, and National Football League. Dialogs for each can be selected by the following prefixes: league epl, mlb, mls, nba, nfl.
  
# ONTOLOGY
Dialog annotations focus on basic variables for each domain. Unlike with Taskmaster-1, we do not indicate API calls or "accept/reject" of particular API parameters in transactional dialogs. Each conversation was annotated by two workers. Both annotations are included in this collection. The exact schema file used for each domain can be found in [the ontology folder](https://github.com/google-research-datasets/Taskmaster/tree/master/TM-2-2020/ontology).

# TRANSCRIPTION NOTES
As with Taskmaster-1, in a separate task, transcription of crowdsourced user utterances from these two-person dialogs were checked for errors but may still include an occasional typo, misspelling or ungrammatical sequence. In cases where a dialog failed to make sense, workers doing these corrections were given the freedom to insert or delete turns or replace entire phrases with language that made the dialog follow a more sensible path. Shorthand typing conventions originally used by the call center operators such as 'cuz', 'lol' and other non-standard English phrases were left as is. Disfluencies such as 'they um, they want Korean cuisine' were also usually transcribed as spoken, but sometimes transcribers corrected them.

_Comments or questions? Join taskmaster-datasets@googlegroups.com to discuss._

