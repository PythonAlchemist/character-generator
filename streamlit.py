import streamlit as st
from src.character import Character
import os


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


# Streamlit app
def main():
    st.title("Character Generator")

    char = Character()

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

    st.write("Character Details:")
    display_character(char)


# Function to display character details
def display_character(char):
    # Check if the image file exists
    image_path = "character_image.jpg"
    if os.path.exists(image_path):
        st.image(image_path, use_column_width=True)
    else:
        st.write("Image not found")

    st.write(f"Name: {char.name}")
    st.write(f"Age: {char.age}")
    st.write(f"Description: {char.description}")
    st.write(f"Title: {char.title}")
    st.write(f"Type: {char.type}")
    st.write(f"Sex: {char.sex}")
    st.write(f"Race: {char.race}")
    st.write(f"Family: {char.family}")
    st.write(f"Location: {char.location}")


if __name__ == "__main__":
    main()
