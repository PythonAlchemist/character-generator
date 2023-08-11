import streamlit as st
import pandas as pd
import os
import json

from src.char_gen.entity.character import Character
from src.char_gen.entity.organization import Organization
from src.char_gen.entity.location import Location
from char_gen.models.open_ai_generator import OpenAIGenerator


def load_entity_list(entity_cls):
    resp = entity_cls.getEntityList()
    return {entity["name"]: entity["id"] for entity in resp}


def edit_character(character):
    character.name = st.text_input("Name", character.name)
    character.age = st.text_input("Age", character.age)
    character.description = st.text_area("Description", character.description)
    character.backstory = st.text_area("Backstory", character.backstory)
    character.title = st.text_input("Title", character.title)
    character.type = st.text_input("Type", character.type)
    character.sex = st.text_input("Sex", character.sex)
    character.race = st.text_input("Race", character.race)
    character.family = st.text_input("Family", character.family)
    character.location = st.text_input("Location", character.location)


def collect_pregen_data(org_selected, loc_selected):
    members = Organization.getAllMembers(org_map[org_selected]) if org_selected else []
    location = (
        Location(id=location_map[loc_selected]).promptPackage()
        if loc_selected
        else None
    )
    organization = (
        Organization(id=org_map[org_selected]).promptPackage() if org_selected else None
    )
    members_json = [member.promptPackage() for member in members]

    return location, organization, members_json


def main():
    st.sidebar.title("Pregen Parameters")

    # Check if the variables already exist in the session state
    if "org_selected" not in st.session_state:
        st.session_state.org_selected = st.sidebar.selectbox(
            "What Organizations is this character associated with?",
            list(org_map.keys()),
        )
    else:
        st.session_state.org_selected = st.sidebar.selectbox(
            "What Organizations is this character associated with?",
            list(org_map.keys()),
            index=list(org_map.keys()).index(st.session_state.org_selected),
        )

    if "loc_selected" not in st.session_state:
        st.session_state.loc_selected = st.sidebar.selectbox(
            "What Locations is this character associated with?",
            list(location_map.keys()),
        )
    else:
        st.session_state.loc_selected = st.sidebar.selectbox(
            "What Locations is this character associated with?",
            list(location_map.keys()),
            index=list(location_map.keys()).index(st.session_state.loc_selected),
        )

    prompt_text = st.sidebar.text_area(
        "Prompt", placeholder="Inform the models about the new character."
    )

    if st.sidebar.button("Collect Pregen Data"):
        st.session_state.data_packet = {}
        (
            st.session_state.data_packet["location"],
            st.session_state.data_packet["organization"],
            st.session_state.data_packet["members"],
        ) = collect_pregen_data(
            st.session_state.org_selected, st.session_state.loc_selected
        )
        st.session_state.data_packet["prompt"] = prompt_text

    st.title("Character Generator")

    generator = OpenAIGenerator()

    if "data_packet" in st.session_state:
        for key, value in st.session_state.data_packet.items():
            st.write(f"{key.capitalize()} Data:")
            st.write(value)

    if st.button("Generate Character"):
        with open("prompt.json", "w") as file:
            file.write(json.dumps(st.session_state.data_packet))
        response = generator.generate(st.session_state.data_packet)
        st.session_state.char = Character(props=response)

    if "char" in st.session_state:
        edit_character(st.session_state.char)

    if st.button("Update"):
        st.session_state.char.upload()
        st.write("Character Updated!")


def display_character_image(image_path):
    if os.path.exists(image_path):
        st.image(image_path, use_column_width=True)
    else:
        st.write("Image not found")


if __name__ == "__main__":
    org_map = load_entity_list(Organization)
    location_map = load_entity_list(Location)
    main()
