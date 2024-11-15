config = """
llm:
 provider: ollama
 config:
   model: 'phi3.5:3.8b-mini-instruct-q4_K_M'
   temperature: 0.1
   max_tokens: 500
   top_p: 0.1
   stream: false
   base_url: 'http://localhost:11434'  # Add this line
embedder:
 provider: huggingface
 config:
   model: 'sentence-transformers/all-mpnet-base-v2'
"""


# Write the multi-line string to a YAML file
with open('phi35_ollama.yaml', 'w') as file:
   file.write(config)

