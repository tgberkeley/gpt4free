import g4f


# print(g4f.Provider.Ails.params) # supported args

# Automatic selection of provider

# streamed completion
response = g4f.ChatCompletion.create(model="gpt-4", messages=[
                                     {"role": "user", "content": "what happened in ww2"},
                                     {"role": "assistant", "content": "a big war with many casualties"},
                                     {"role": "user", "content": "what happened in the following year"}], stream=True)
print(response)
for message in response:
    print(message)

# normal response
# response = g4f.ChatCompletion.create(model=g4f.Model.gpt_4, messages=[
#                                      {"role": "user", "content": "hi"}]) # alterative model setting

# print(response)


# # Set with provider
# response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.Forefront, messages=[
#                                      {"role": "user", "content": "Hello world"}], stream=True)

# for message in response:
#     print(message)