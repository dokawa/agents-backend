import unittest

from apps.agents.constants import MAX_TOKENS, VECTOR_DIMENSION
from apps.agents.memory_structures.utils import (
    create_chunks,
    get_embedding,
    get_tokenizer,
)


class TestEmbedding(unittest.TestCase):
    def test_embedding(self):
        sentence = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "
            "ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco "
            "laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in "
            "voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat "
            "non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        )
        embedding = get_embedding(sentence)
        assert len(embedding) == VECTOR_DIMENSION

    # def test_embed_tokens_and_text_are_the_same(self):
    #     sentence = (
    #         "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "
    #     )
    #
    #     embedding = get_embedding(sentence, average=True)
    #     embedding_2 = get_embedding(sentence, average=False)
    #     assert np.equal(embedding, embedding_2)

    def test_early_chunk_if_end_of_sentence_dot(self):
        tokenizer = get_tokenizer()
        sentence = "1.23456"

        chunks, lens = create_chunks(sentence, 2, tokenizer)

        assert any([tokenizer.decode(c) == "1." for c in chunks])

    def test_early_chunk_if_end_of_sentence_linebreak(self):
        tokenizer = get_tokenizer()
        sentence = "1\n23456"

        chunks, lens = create_chunks(sentence, 2, tokenizer)

        for c in chunks:
            print(tokenizer.decode(c))

        assert any(
            [tokenizer.decode(c) == "1" for c in chunks]
        )  # linebreak is not included in chunk

    def test_chunks_always_less_than_max(self):
        tokenizer = get_tokenizer()
        sentence = "123456789"

        max = 3

        chunks, lens = create_chunks(sentence, max, tokenizer)

        for c in chunks:
            assert len(c) < max

    def test_create_chunks(self):
        tokenizer = get_tokenizer()
        sentence = (
            "your task is to help a marketing team create a description for a retail website of a product based on a "
            "technical fact sheet. write a product description based on the information provided in the technical "
            "specifications delimited by triple backticks. the description is intended for furniture retailers, "
            "so should be technical in nature and focus on the materials the product is constructed from. "
            "at the end of the description, include every 7 - character product id in the technical specification. "
            "use at most 50 words. technical specifications : ` ` ` / overview - part of a beautiful family of "
            "mid - century inspired office furniture, including filing cabinets, desks, bookcases, meeting tables, "
            "and more. - several options of shell color and base finishes. "
            "- available with plastic back and front upholstery ( swc - 100 ) or full upholstery ( swc - 110 ) "
            "in 10 fabric and 6 leather options. - base finish options are : stainless steel, matte black,"
            " "
            "gloss white, or chrome. - chair is available with or without armrests. "
            "- suitable for home or business settings. - qualified for contract use. construction "
            "- 5 - wheel plastic coated aluminum base. - pneumatic chair adjust for easy raise / lower action. "
            "dimensions - width 53 cm | 20. 87 ” - depth 51 cm | 20. 08 ” - height 80 cm | 31. 50 ” "
            "- seat height 44 cm | 17. 32 ” - seat depth 41 cm | 16. 14 ” options - soft or hard "
            "- floor caster options. - two choices of seat foam densities : medium ( 1. 8 lb / ft3 ) or "
            "high ( 2. Your task is to help a marketing team create a "
            "description for a retail website of a product based "
            "on a technical fact sheet. Write a product description based on the information "
            "provided in the technical specifications delimited by "
            "triple backticks. The description is intended for furniture retailers, "
            "so should be technical in nature and focus on the "
            "materials the product is constructed from. At the end of the description, include every 7-character "
            "Product ID in the technical specification. Use at most 50 words. Technical specifications: ```/"
            "OVERVIEW"
            "- Part of a beautiful family of mid-century inspired office furniture, "
            "including filing cabinets, desks, bookcases, meeting tables, and more."
            "- Several options of shell color and base finishes."
            "- Available with plastic back and front upholstery (SWC-100) "
            "or full upholstery (SWC-110) in 10 fabric and 6 leather options."
            "- Base finish options are: stainless steel, matte black, "
            "gloss white, or chrome."
            "- Chair is available with or without armrests."
            "- Suitable for home or business settings."
            "- Qualified for contract use. CONSTRUCTION"
            "- 5-wheel plastic coated aluminum base."
            "- Pneumatic chair adjust for easy raise/lower action. DIMENSIONS"
            "- WIDTH 53 CM | 20.87”"
            "- DEPTH 51 CM | 20.08”"
            "- HEIGHT 80 CM | 31.50”"
            "- SEAT HEIGHT 44 CM | 17.32”"
            "- SEAT DEPTH 41 CM | 16.14” OPTIONS"
            "- Soft or hard-floor caster options."
            "- Two choices of seat foam densities: "
            " medium (1.8 lb/ft3) or high (2.8 lb/ft3)"
            "- Armless or 8 position PU armrests  MATERIALS"
            "SHELL BASE GLIDER"
            "- "
        )

        chunks, lens = create_chunks(sentence, MAX_TOKENS, tokenizer)
        for c in chunks:
            print(tokenizer.decode(c))
            assert len(c) < MAX_TOKENS
