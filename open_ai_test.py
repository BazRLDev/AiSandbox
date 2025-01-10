# from openai import OpenAI

# client = OpenAI(
#   api_key="MY_KEY"
# )

# completion = client.chat.completions.create(
#   model="gpt-4o-mini",
#   store=True,
#   messages=[
#     {"role": "user", "content": "provide a brief explaination of what AI is"}
#   ]
# )

# "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:
# A close-up shot of a willow tree gracefully bending in a strong wind, illustrating flexibility and resilience. The background features a soft, diffused light and a blurred landscape of rolling green hills. The overall mood is serene and inspiring.
# The image should evoke an inspirational or reflective mood in a viewer."


# print(completion.choices[0].message);
# "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:A close-up shot of a willow tree gracefully bending in a strong wind, illustrating flexibility and resilience. The background features a soft, diffused light and a blurred landscape of rolling green hills. The overall mood is serene and inspiring. The image should evoke an inspirational or reflective mood in a viewer."

from openai import OpenAI
client = OpenAI(api_key="MY_KEY")

response = client.images.generate(
    model="dall-e-3",
    prompt="A close-up shot of a willow tree gracefully bending in a strong wind, illustrating flexibility and resilience. The background features a soft, diffused light and a blurred landscape of rolling green hills. The overall mood is serene and inspiring. The image should evoke an inspirational or reflective mood in a viewer.",
    size="1024x1024",
    quality="standard",
    n=1,
    response_format="b64_json",
    # style="natural"
)

print(response.data[0].b64_json)
print(response.data[0].revised_prompt)
print(response.data[0].url)

