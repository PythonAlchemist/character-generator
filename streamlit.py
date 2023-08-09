import streamlit as st
from src.char_gen.entity.character import Character
from src.char_gen.entity.organization import Organization
from src.char_gen.entity.location import Location
import pandas as pd
import os

# load lists
resp = Organization.getEntityList()
org_map = {}
for org in resp:
    org_map[org["name"]] = org["id"]

resp = Location.getEntityList()
location_map = {}
for location in resp:
    location_map[location["name"]] = location["id"]

# packet
packet = {
    "location": None,
    "organization": None,
    "prompt": None,
}


# Function to display and edit character details
def edit_character(char):
    char.name = st.text_input("Name", char.name)
    if char.age is not None:
        char.age = st.number_input("Age", min_value=0, value=char.age)
    else:
        char.age = st.number_input("Age", min_value=0)
    char.description = st.text_area("Description", char.description)
    char.title = st.text_input("Title", char.title)
    char.type = st.text_input("Type", char.type)
    char.sex = st.text_input("Sex", char.sex)
    char.race = st.text_input("Race", char.race)
    char.family = st.text_input("Family", char.family)
    char.location = st.text_input("Location", char.location)


def collect_pregen_data(org_sel, loc_sel):
    members = []
    members_resp = Organization.getAllMembers(org_map[org_sel]) if org_sel else []
    for member in members_resp:
        members.append(member)

    loc_json = Location(id=location_map[loc_sel]).promptPackage() if loc_sel else None
    org_json = Organization(id=org_map[org_sel]).promptPackage() if org_sel else None
    members_json = [member.promptPackage() for member in members]

    return loc_json, org_json, members_json


# Streamlit app
def main():
    pregen = False

    st.sidebar.title("Pregen Parameters")

    # define organizations character is associated with
    org_sel = st.sidebar.selectbox(
        "What Organizations is this character associated with?",
        list(org_map.keys()),
    )

    # define locations character is associated with
    loc_sel = st.sidebar.selectbox(
        "What Locations is this character associated with?",
        list(location_map.keys()),
    )

    # define prompt
    text = st.sidebar.text_area(
        "Prompt",
        placeholder="This is your chance to inform the models about anything you want about the new character.",
    )

    if st.sidebar.button("Collect Pregen Data"):
        (
            packet["location"],
            packet["organization"],
            packet["prompt"],
        ) = collect_pregen_data(org_sel, loc_sel)
        pregen = True

    st.title("Character Generator")

    char = Character()

    if pregen:
        st.write("Organization Data:")
        st.write(packet["organization"])
        st.write("Location Data:")
        st.write(packet["location"])
        st.write("Prompt Data:")
        st.write(packet["prompt"])

    # Check if the image file exists
    image_path = "character_image.jpg"
    if os.path.exists(image_path):
        st.image(image_path, use_column_width=True)
    else:
        st.write("Image not found")

    edit_character(char)

    if st.button("Update"):
        # TODO: Use the to update kanka
        st.write("Character Updated!")


if __name__ == "__main__":
    main()
