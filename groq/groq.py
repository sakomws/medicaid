from groq.groq import Groq

client = Groq()
completion = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[
        {
            "role": "user",
            "content": "hey h\n"
        },
        {
            "role": "assistant",
            "content": "json"
        },
        {
            "role": "user",
            "content": ""
        },
        {
            "role": "assistant",
            "content": "{\n\"hey\": \"hey\"\n}"
        }
    ],
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    stream=False,
    response_format={"type": "json_object"},
    stop=None,
)

print(completion.choices[0].message)
