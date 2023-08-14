import openai
import os
import json
from typing import Union
from dotenv import load_dotenv, find_dotenv

from char_gen.entity.location import Location
from char_gen.entity.organization import Organization
from char_gen.entity.character import Character

load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")


class OpenAiGenerator:
    def __init__(self):
        self.conversation_history = []

    @staticmethod
    def collect_context(
        location: Union[int, None] = None, organization: Union[int, None] = None
    ) -> dict:
        if location:
            loc_content = Location(id=location).promptPackage()
        if organization:
            org_content = Organization(id=organization).promptPackage()

            members = Organization.getAllMembers(organization)
            member_content = [member.promptPackage() for member in members]

        context = {
            "location": loc_content if loc_content else None,
            "organization": org_content if org_content else None,
            "members": member_content if member_content else None,
        }
        return context

    def generate_character(self, query: dict):
        # reset
        self.conversation_history = []

        prompt = f"You are a character generator tool that is trying to generate a character based in the Dungeons and Dragons universe. \
        You will be provided with information about the characters location, organization, and other characters in the organization as well \
        as a prompt to steet the character in a certain direction based on user desires. \
        \n\n \
        Location: {query['location']}\
        \n\n \
        Organization: {query['organization']}\
        \n\n \
        Organization Members: {query['members']}\
        \n\n \
        Prompt: {query['prompt']}\
        \n\n \
        Format: \
        return a json object with the following fields: \
        name: name of the character (first and last) \
        description: description of the characters apperance \
        backstory: backstory for the character, a paragraph or two \
        race: race of the character (keep dnd 5e races in mind) \
        age: age of the character \
        title: title of the character \
        sex: gender of the character \
        organization_role: role of the character in the organization \
        "
        self.conversation_history.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # The chat model to use
            messages=self.conversation_history,
        )
        return json.loads(response.choices[0].message["content"])


if __name__ == "__main__":
    gen = OpenAiGenerator()

    test_query = {
        "location": {
            "name": "Moonshadow Grove",
            "description": "Description: Moonshadow Grove is a sanctuary of tranquility on the edge of the foreboding Dark Forest, a place where the veil between the material plane and the Feywild is thin. This location, teetering on the precipice of wild, untamed magic, lends the grove a sense of otherworldly beauty and an undercurrent of potent, raw energy. The grove is a labyrinth of towering ancient trees, their bark silvered in the moonlight and their leaves casting dappled shadows on the forest floor. The air is filled with the scent of pine and damp earth, and the quiet rustle of leaves is occasionally punctuated by the distant call of a nocturnal creature. A clear, sparkling stream winds its way through the grove, its waters reflecting the moon and stars above. At the heart of the grove stands a majestic moonstone monolith, bathed in ethereal light. This sacred site is where the druids of the Circle of the Moon perform their moonlit rituals, drawing upon the potent magic of the location to enhance their spells. Despite its serene beauty, Moonshadow Grove is not without danger. Its proximity to the Dark Forest means that powerful creatures often stray into the grove. The druids live in a delicate balance with these creatures, respecting their power and giving them a wide berth. The grove is also home to a variety of magical flora and fauna. Luminescent mushrooms and flowers provide a soft glow, and creatures such as fey panthers and verdant striders can be seen stalking through the underbrush. The grove is alive with the sounds of nature, from the hooting of owls to the gentle rustle of leaves in the wind. Moonshadow Grove is a place of potent magic, serene beauty, and hidden dangers, a testament to the raw, untamed power of nature. History: Founding of the Grove (100 years ago): Davnan , a wise and powerful Firbolg druid, discovered the location that would become Moonshadow Grove. Recognizing the potent magic of the place, he decided to establish a sanctuary for all creatures. He spent many months nurturing the land, encouraging the growth of the ancient trees and purifying the stream that ran through it. Formation of the Circle of the Moon (75 years ago): After 25 years of living in the grove, Davnan felt the need to share the wisdom and beauty of the grove with others. He founded the Circle of the Moon , a druidic order dedicated to the preservation and understanding of the natural world. The Circle quickly attracted druids from far and wide, who were drawn to the grove's potent magic and serene beauty. The Night of Silver Shadows (60 years ago): A rare celestial event occurred where the moon was particularly bright and large in the sky. This night was marked by a surge in magical energy within the grove, leading to an outburst of growth and an influx of fey creatures from the Dark Forest. This event further solidified the grove's connection to the moon and the Feywild. Vorgansharax's Assault (50 years ago): A powerful green dragon named Vorgansharax attacked the grove, drawn by its potent magic. The Circle of the Moon, led by Davnan, managed to repel the dragon after a fierce battle. This event led to the strengthening of the grove's defenses and a deeper commitment from the Circle to protect their sanctuary. The Fey Incursion (40 years ago): A group of mischievous fey creatures from the Dark Forest caused chaos in the grove, playing tricks on the druids and disturbing the natural balance. The Circle managed to negotiate with the fey, establishing a pact of mutual respect and non-interference that still holds to this day. Arrival of Thistle (20 years ago): A young fey named Thistle arrived in the grove, seeking guidance from the Circle. Davnan took him under his wing, hoping to guide him on the path of harmony with nature. However, Thistle's heart was corrupted over time, leading to the current crisis in the grove. The Grove's Corruption (Present): Thistle, now a powerful archfey, has begun to corrupt the grove, twisting its magic for his own purposes. The Circle of the Moon, led by Davnan, is now facing its greatest challenge as it strives to save the grove and redeem Thistle.",
            "type": "Village",
        },
        "organization": {
            "name": "Circle of the Moon",
            "description": "The Circle of the Moon is a revered and ancient druidic order dedicated to the preservation and understanding of the natural world. The members of this circle, known as Moon Druids, are guardians of the wild, using their abilities to maintain the balance of nature and combat those who would disrupt it. Moon Druids are known for their deep connection to the lunar cycle, believing that the phases of the moon are a reflection of the life cycle in nature. They hold their most sacred rituals during the full moon, where they harness its energy to enhance their magic and commune with nature spirits. Moonshadow Grove the home of the Circle of the Moon, is a place of serene beauty. Nestled deep within an ancient forest, the grove is a sanctuary for all creatures. The trees are tall and ancient, their leaves shimmering silver in the moonlight. A clear stream winds its way through the grove, its waters pure and sparkling under the moon's glow. At the heart of the grove stands a majestic moonstone monolith, a sacred site where the druids perform their moonlit rituals. The Circle of the Moon is led by Davnan , a wise and venerable Firbolg druid. Under his guidance, the druids of the Circle live in harmony with the forest, studying the secrets of nature and providing aid to the creatures of the grove. Despite recent challenges, the Circle remains steadfast in their duty, ready to protect Moonshadow Grove from any threats.",
            "type": "Druid Grove",
        },
        "members": [
            {
                "name": "Davnan",
                "description": "Description: Davnan is a towering figure, standing at nearly eight feet tall, as is typical for his Firbolg kin. His skin is a soft grey, dappled with patches of green moss-like hair that gives him a natural camouflage in his beloved grove. His eyes are a deep, tranquil blue, reflecting the wisdom and sorrow of his many years. His hair is long and white, often adorned with flowers and leaves, and his beard is thick and bushy, braided with beads made from the bones of fallen animals. Despite his size, Davnan moves with a gentle grace, treading lightly on the forest floor and speaking in a soft, soothing voice. His presence is calming, and animals are naturally drawn to him. Backstory: Davnan was born into a peaceful Firbolg clan that lived in harmony with nature. From a young age, he showed a deep connection to the natural world and was trained as a druid by the elders of his clan. Over the years, he grew in power and wisdom, becoming a respected member of his community. Nearly a century ago, Davnan left his clan to establish a sanctuary for all creatures, a place where the balance of nature could be preserved and respected. He found an ancient ruin, a fort with a deep connection to the divine, and around it, he built his grove ( Moonshadow Grove ). Druids from far and wide were drawn to Davnan's grove, seeking to learn from his wisdom and live in harmony with nature. Before long his numbers grew and the Circle of the Moon was formed as a governing body to protect and provide for the inhabitants of the grove. Davnan has been the Archdruid of this grove since it's inception 75 years ago. However, everything changed when the archfey Thistle arrived. He was summoned through the collective power of the circle as a protector 20 years ago after the fall of Krastdale . However the longer Thistle has stayed in the material realm the more warped his power and intentions have become, and now his actions have been polluting the minds of those in the grove negatively impacting the balance with nature. Now, Davnan is torn between his loyalty to his flock and his duty to preserve the balance of nature. He has seen the corruption spreading through his grove and knows that he must take a stand against Thistle. But he also knows that this will not be an easy fight, and that he may have to make great sacrifices to save his grove.",
                "backstory": None,
                "title": "Archdruid of the Moon",
                "age": "253",
                "sex": "Male",
            },
            {
                "name": "Thistle",
                "description": "Thistle, once a figure of fey beauty and charm, has been twisted by corruption into a monstrous form. He now stands as a grotesque parody of a centaur, his upper body that of a twisted elf and his lower body that of a monstrous, thorny beast. His skin is a sickly, luminescent green, mottled with patches of dark, thorny bark. His hair, once vibrant red, now resembles a tangled mass of thorny vines, writhing as if alive. His eyes, once a mesmerizing violet, now glow with a malevolent, poisonous green light. Thistle's centaur body is a terrifying sight. His equine lower half is covered in a rough, bark-like hide, sprouting twisted thorns and gnarled roots. His hooves are jagged and sharp, leaving deep gouges in the earth with every step. Despite his monstrous form, Thistle retains a disturbing elegance. His movements are fluid and graceful, belying the raw power that lurks beneath his thorny hide. His voice, though now carrying a chilling echo, still holds a hypnotic quality, weaving a dangerous allure around his words. Thistle's transformation is a stark reminder of the corruption that has taken hold of him, turning a once noble fey into a monstrous creature. Yet, despite his terrifying appearance, there is a tragic sense of loss about Thistle, a faint echo of the fey lord he once was.",
                "backstory": None,
                "title": "Protector of the Moon",
                "age": None,
                "sex": None,
            },
        ],
        "prompt": "Create another druid in the circle. They should be a medium to high level with decent reputation.",
    }

    query = gen.collect_context(location=1112563, organization=237897)
    query[
        "prompt"
    ] = "Create another druid in the circle. They should be a medium to high level with decent reputation."
    resp = gen.generate_character(query)
    char = Character(props=resp)
    resp2 = char.upload()
    # update the character with the id
    char.id = resp2["id"]
    char.location_id = 1112563
    char.linkToOrganization(237897)
    # char.delete()
    print(resp)
