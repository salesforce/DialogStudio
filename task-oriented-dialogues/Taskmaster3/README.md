# COPYRIGHT NOTICE

This is the work of Bill Byrne, Karthik Krishnamoorthi, and Saravanan Ganesh from Google LLC, made available under the Creative Commons Attribution 4.0 License. A full copy of the license can be found at https://creativecommons.org/licenses/by/4.0/

# DATA

## BASICS
The Taskmaster-3 (aka TicketTalk) dataset consists of 23,789 movie ticketing dialogs (located in Taskmaster/TM-3-2020/data/). By "movie ticketing" we mean conversations where the  customer's goal is to purchase tickets after deciding on theater, time, movie name, number of tickets, and date, or opt out of the transaction.

## COLLECTION METHODOLOGY
This collection was created using the "self-dialog" method. This means a single, crowd-sourced worker is paid to create a conversation writing turns for both speakers, i.e. the customer and the ticketing agent. In order to gather a wide range of conversational scenarios and linguistic phenomena, workers were given both open-ended as well as highly structured conversational tasks. In all, we used over three dozen sets of instructions while building this corpus. The "instructions" field in data.json provides the exact scenario workers were given to complete each dialog. In this way, conversations involve a wide variety of paths, from those where the customer decides on a movie based on genre, their location, current releases, or from what they already have in mind. In addition, dialogs also include error handling with repect to repair (e.g. "No, I said Tom Cruise."), clarifications (e.g. "Sorry. Did you want the AMC 16 or Century City 16?") and other common conversational hiccups. In some cases instructions are completely open ended e.g. "Pretend you are taking your friend to a movie in Salem, Oregon. Create a conversation where you end up buying two tickets after finding out what is playing in at least two local theaters. Make sure the ticket purchase includes a confirmation of the deatils by the agent before the purchase, including date, time, movie, theater, and number of tickets." In other cases we restrict the conversational content and structure by offering a partially completed conversation that the workers must finalize or fill in based a certain parameters. These partially completed dialogs are labeled "Auto template" in the "scenario" field shown for each conversation in the data.json file. In some cases, we provided a small KB from which workers would choose movies, theaters, etc. but in most cases (pre-pandemic) workers were told to use the internet to get accurate current details for their dialogs. In any case, all relevant entities are annotated. 

## STRUCTURE
Each conversation in the data file has the following structure:
* __conversation_id:__ A universally unique identifier with the prefix 'dlg-'. The ID has no meaning.
* __utterances:__ An array of utterances that make up the conversation.
* __vertical:__ In this dataset the vertical for all dialogs is "Movie Tickets".
* __scenario:__ This is the title of the instructions for each dialog.
* __instructions:__ Instructions for the crowdsourced worker used in creating the conversation.

Each utterance has the following fields:
* __index:__ A 0-based index indicating the order of the utterances in the conversation.
* __speaker:__ Either "user" or "assistant", indicating which role generated this utterance.
* __text:__ The raw text of the utterance.
* __apis:__ An array of API invocations made during the utterance. 
* __segments:__ An array of various text spans with semantic annotations.

Each API has the following structure:
* __name:__ The name of the API invoked (e.g. find_movies).
* __index:__ The index of the parent utterance.
* __args:__ Key-Value pairs representing the argument names and values for the API.
* __response:__ Key-Value pairs containing the API response.

Each segment has the following fields:
* __start_index:__ The position of the start of the annotation in the utterance text.
* __end_index:__ The position of the end of the annotation in the utterance text.
* __text:__ The raw text that has been annotated.
* __annotations:__ An array of annotation details for this segment.

Each annotation has a single field:

* __name:__ The annotation name.

# ONTOLOGY
Dialog annotations focus on common movie ticketing entities and API calls and responses. For more details, check the entities.json and apis.json.

## ENTITIES (see entities.json for more detail)
* __name.movie:__ Name of the movie, e.g. Joker, Parasite, The Avengers
* __name.theater:__ Name of the theater, e.g. Century City, AMC Mercado 20
* __num.tickets:__ Number of tickets, e.g. two, me and my friend, John and I
* __time.preference:__ Preferred time or range, e.g. around 2pm, later in the evening, 4:30pm
* __time.showing:__ The showtimes published by the theater, e.g. 5:10pm, 8:30pm
* __date.showing:__ the date or day of the showing, e.g. today, tonight, tomrrow, April 12th.
* __location:__ The city, or city and state, zip code and sometimes more specific regions, e.g. downtown
* __type.screening:__ IMAX, Dolby, 3D, standard, or similar phrases for technology offerings
* __seating:__ Various phrases from specific "row 1" to "near the back", "on an aisle", etc.
* __date.release:__ Movie attribute published for the official movie release date.
* __price.ticket:__ Price per ticket
* __price.total:__ The total for the purchase of all tickets
* __name.genre:__ Includes a wide range from classic genres like action, drama, etc. to categories like "slasher" or series like Marvel or Harry Potter
* __description.plot:__ The movie synopsis or shorter description
* __description.other:__ Any other movie description that is not captured by genre, name, plot.
* __duration.movie:__ The movie runtime, e.g. 120 minutes
* __name.person:__ Names of actors, directors, producers but NOT movie characters
* __name.character:__ Character names like James Bond, Harry Potter, Wonder Woman
* __review.audience:__ The audience review
* __review.critic:__ Critic reviews like those from Rotten Tomatoes, IMDB, etc.
* __rating.movie:__ G, PG, PG-13, R, etc.

## API Calls (see apis.json for more detail)
* __resolve_movie:__ To check the movie name given by the customer in the dialo against the official name published, e.g. The new James Bond Movie --> No Time To Die
* __resolve_location:__ Returns location name given by the customer in the dialo against the official name, e.g. SF --> San Francisco California
* __resolve_theater:__ Returns theater name given by the customer in the dialog against the official name, e.g. the AMC --> AMC Mercado 20
* __find_movies:__ Returns a list of movies given a set of parameters (see apis.json on the ontology folder)
* __find_theaters:__ Returns a list of movies given a location and optionally a movie name
* __find_showtimes:__ Returns a list of movies given a theater and movie name
* __get_movie_attribute:__ Returns a value based on a movie name for one of the following attributes--name.genre, name.person, name.character, date.release, description.plot, duration.movie, review.audience, review.critic, rating.movie
* __check_tickets:__ Returns available/unavailable based on movie, time, theater, number of tickets, and date. If date or ticket number are missing from the dialog, the defaults of "today" and "1" are used.
* __book_tickets:__ Returns success/failure based on movie, time, theater, number of tickets, and date. If date or ticket number are missing from the dialog, the defaults of "today" and "1" are used.

# NOTES
<ul>
<li>Dialogs were checked for errors but may still include an occasional typo, misspelling or ungrammatical sequence. Shorthand typing conventions originally used by the  such as 'cuz', 'lol' and other non-standard English phrases were left as is.,/li>
<li>The dataset does not contain conversations with successive user utterances (even though in actual interactions, the user often provides input over two disjointed utterances).</li>
<li>There are many conversations where the agent has more than one utterance in an interaction. In all of these cases, the first utterance is about asking the user to wait until the agent obtains the API response, with something like “Let me look that up”. The second utterance in the interaction incorporates the actual API response (“I found two theaters near you.”).</li>
</ul>


_Comments or questions? Join taskmaster-datasets@googlegroups.com to discuss._

