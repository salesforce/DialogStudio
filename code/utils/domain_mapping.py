"""
 Copyright (c) 2023, salesforce.com, inc.
 All rights reserved.
 SPDX-License-Identifier: Apache License 2.0
 For full license text, see the LICENSE file in the repo root or https://www.apache.org/licenses/LICENSE-2.0
"""


#!/usr/bin/env python3
import sys, os
import random

templates = [
    "This is a bot helping users to _____. Given the dialog context and external database, please generate a relevant system response for the user.",
    "This bot assists users to _____. Based on the dialogue context and information from the external database, please generate an appropriate response for the user.",
    "This bot helps users to _____. Based on the conversation history and available external data, please generate a relevant system response for the user.",
    "The purpose of this bot is to assist users to _____. Considering the dialogue context and the information available in the external database, please provide a fitting response for the user.",
    "This bot is designed to help users _____. By utilizing the current dialog context and external resources, generate a fitting response for the user."
]

mapping = {
    "ABCD":{
        "product_defect": "solve issues about refunds and returns",
        "storewide_query": "find answers to FAQ questions about pricing, timing, membership or features",
        "shipping_issue": "check out update a shipment of an item",
        "subscription_inquiry": "updates premium subscription",
        "account_access": "manage account access information",
        "troubleshoot_site": "solve website-related issues", # website slow, search not working, credit card, cart not updating
        "single_item_query": "find answers to FAQ questions about clothes",
        "order_issue": "get status of an order or change an order",
        "purchase_dispute": "dispute a purchase",
        "manage_account": "manage account profile",
    },
    "AirDialogue":{
        "flight": "book a flight ticket",
    },
    "BiTOD":{
        "restaurants": "find and book a restaurant",
        "attractions": "find a tourist attraction",
        "HKMTR": "find a metro line",
        "weathers": "search weather information",
        "hotels": "find and book a hotel",
    },
    "CaSiNo":{
        "negotiate": "take the role of campsite neighbors and negotiate for food, water, and firewood" # not help to finish task
    },
    "CraigslistBargains":{
        "bargain": "bargain for goods" # can be devided into different items e.g. housing, bike, electronics
    },
    "DSTC2-Clean":{
        "restaurant": "find a restaurant"
    },
    "FRAMES":{
        "trip": "book a trip"
    },
    "KVRET":{
        "schedule":"manage a calendar",
        "weather":"find weather information",
        "navigate":"get navigation",
    },
    "WOZ2_0":{
        "restaurant":"find a restaurant",
    },
    "SGD":{
        "alarm": "manage alarms",
        "banks": "manage bank accounts",
        "buses": "book a bus journey",
        "events": "book an event ticket",
        "flights": "book a flight ticket",
        "homes": "find an apartment or schedule an apartment viewing", # Homes_2 : Service for finding properties to buy and rent"
        "hotels": "book a hotel",
        "media": "rent a movie to watch",
        "music": "find a song",
        "rentalcars": "rent a car",
        "restaurants": "book a restaurant",
        "ridesharing": "book a ride",
        "services": "reserve a therapist, dentists, doctor or hair stylist", # Services_1: hair stylist; _2:dentists; Services_4: therapist
        "travel": "find a tourist attraction",
        "weather": "get weather information",
        "messaging": "connect and share locations", # Messaging_1:Connect and share locations with your contact
        "movies": "book a movie ticket",
        "payment": "manage a payment", # payment_1 The fast, simple way to pay in apps, on the web, and in millions of stores
        "trains": "book a train journey",
        "calendar": "manage a calendar",
    },
    "MetaLWOZ":{
        "update_calendar": "schedule meetings on a calendar",
        "order_pizza": "order a pizza",
        "movie_listings": "get movie information",
        "event_reserve": "make reservations for events",
        "weather_check": "get weather information",
        "update_contact": "update cell phone contacts",
        "make_restaurant_reservations": "reserve a restaurant",
        "edit_playlist": "manage music playlists",
        "look_up_info": "fetch information from the internet",
        "shopping": "order products from website",
        "store_details": "get information about stores and businesses",
        "sports_info": "get sports information",
        "quote_of_the_day_bot": "get a quote of the day",
        "how_to_basic": "get instructions for basic tasks",
        "prompt_generator": "get creative prompts",
        "library_request": "get library information",
        "bank_bot": "manage bank accounts",
        "restaurant_picker": "find a restaurant",
        "phone_plan_bot": "get mobile phone service",
        "name_suggester": "get names for things",
        "city_info": "get facts about different cities",
        "music_suggester": "get music suggestions",
        "agreement_bot": "get agreements",
        "pet_advice": "get pet advice",
        "apartment_finder": "find an apartment",
        "guiness_check": "get world records",
        "geography": "get to know where countries are",
        "alarm_set": "manage alarms",
        "contact_manager": "manage the user's contacts",
        "phone_settings": "manage the user's phone's settings",
        "appointment_reminder": "confirm their appointments",
        "home_bot": "manage the user's home",
        "policy_bot": "get information about a company's policies",
        "decider_bot": "make decisions for the user",
        "catalogue_bot": "search a catalogue",
        "ski_bot": "book skiing trips",
        "bus_schedule_bot": "manage public transit schedules",
        "insurance": "get insurance information",
        "what_is_it": "remember what a thing is.",
        "auto_sort": "sort things",
        "scam_lookup": "get about various scams",
        "time_zone": "get information about time zones",
        "play_times": "schedule shows during a theatre festival",
        "game_rules": "know the rules for games",
        "wedding_planner": "plan weddings",
        "check_status": "check the status of things",
        "present_ideas": "get advice on gift giving",
        "booking_flight": "book a flight ticket",
        "hotel_reserve": "book rooms in a hotel",
        "vacation_ideas": "plan for vacations and trips",
        "tourism": "get tourism related advices"
},
    "STAR":{
        "apartment": "find an apartment or schedule an apartment viewing",
        "bank": "manage bank accounts", # Check the balance / Report suspicious behavior 
        "doctor": "make an appointment with a doctor", # appointment Make an appointment with a doctor / followup doctor appointment Check instructions given by doctor upon last visit
        "hotel": "book a hotel", # find / book a hotel or call for room service
        "meeting": "schedule a meeting",
        "party": "plan a party", # plan Plan a party at a given venue, party rsvp RSVP to a party of a given host at a given venue
        "plane": "book a flight ticket", # search Find a flight between two cities / plane reserve Book a flight, given its id
        "restaurant": "reserve a restaurant", # search Find a restaurant / restaurant reserve Reserve a table at a restaurant
        "ride": "book a ride", #  book ride Call a Taxi/Uber/Lyft ride to any destination / ride change Change details of a Taxi/Uber/Lyft ride that had been called earlier / ride status Check the status of a ride you called earlier
        "spaceship": "solve issues with a spaceship", # life support Recover the spaceship’s life support / spaceship access codes Get a repair robot to open a door for you
        "trip": "get navigation", # directions Get walking/driving/transit directions between two locations (B).
        "trivia": "plan a game of trivia", # Play a game of trivia (C).
        "weather": "get weather information", # Check the weather (forecast) in various cities
    },
    "Taskmaster1":{
        "restaurant": "reserve a restaurant",
        "movie": "book a movie ticket",
        "pizza": "order a pizza",
        "coffee": "order coffee drinks",
        "auto": "make appointment for auto repair",
        "uber": "book a uber ride",
    },
    "Taskmaster2":{ # domains can be split further into subdomains based on instruction_id e.g. sports --> nba, nfl, epl
        "flights": "book a flight ticket",
        "food-ordering": "make a take-out order",
        "hotels":"find a hotel",
        "movies":"find a movie to watch",
        "music": "find music tracks",
        "restaurant-search": "find a restaurant",
        "sports": "get sports information",
    },
    "Taskmaster3":{
        "movie": "book a movie ticket",
    },
    "SimJointMovie":{
        "movie": "book a movie ticket",
    },
    "SimJointRestaurant":{
        "restaurant": "reserve a restaurant",
    },
    "SimJointGEN":{
        "movie": "book a movie ticket",
    },
    "MulDoGO":{
        "airline": "book a flight ticket", # e domain dialogues focus on booking airline flights, selecting or changing seat assignments, and requesting boarding passes;
        "fastfood": "order fast food", # domain is the least similar to the others, as the intents primarily involve ordering food and the slots quantify their order.
        "finance": "manage bank accounts", # domain simulates dialogues a customer may have with a bank. These include opening a bank account, checking their balance, and reporting a lost credit card;
        "insurance": "get insurance information", # domain simulates users calling about their insurance policy or requesting the fulfillment of a policy on their car or phone
        "media": "order a media service", # domain simulates dialogues a customer may have ordering a service or paying bills related to telecommunications. 
        "software": "get software service information", # domain involves customers inquiring about software services: products, outages, promotions, and bills
    },
    "MS-DC":{
        "restaurant": "reserve a restaurant",
        "taxi": "book a taxi",
        "movie": "book a movie ticket",
    },
    "SalesBot":{
        "GetTimesForMovie": "get information for a movie",
        "LookupSong": "find a song",
        "FindMovies": "find a movie to watch",
        "LookupMusic": "find and play a song",
        "PlaySong": "play a song",
        "FindAttractions": "find a tourist attraction",
    },
    "MuDoCo":{
        "calling": "make a call", # user initiates or manipulates a voice or video call
        "messaging": "send or read messages", # user sends or reads messages, asks for information about their message queue
        "music": "find a song", # user searches for music by a certain artist or in a certain genre, asks the system to play songs, etc.
        "news": "get news information", # user asks for information about current events related to a variety of topics
        "reminders": "modify a reminder", # user sets, modifies, queries or deletes reminders for a certain date or time
        "weather": "get weather information", # user asks about the current or future weather conditions in various locations
    },
    "MULTIWOZ2_2":{
        "restaurant": "find a restaurant",
        "hotel": "find a hotel",
        "attraction": "find an attraction",
        "train": "book a train ticket",
        "taxi": "find a taxi",
        "hospital": "find a hospital",
        "police": "find a police station",
        "bus": "find a bus",
    },
}

def generate_prompt(data_name, domains, num_sample=1):
    """
    Including all 5 types of prompt and output a list
    """
    # sampled_template = random.choice(templates)
    descriptions = [mapping[data_name][domain] for domain in domains]
    if len(descriptions) == 1:
        description_str = descriptions[0]
    elif len(descriptions) == 2:
        description_str = " and ".join(descriptions)
    elif len(descriptions) == 0:
        description_str = "complete specified tasks"
    else:
        description_str = "complete multiple tasks, e.g. " + ", ".join(descriptions[:-1]) + ", and " + descriptions[-1]
    return [sampled_template.replace("_____", description_str) for sampled_template in templates]