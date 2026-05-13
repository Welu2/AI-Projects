from transformers import pipeline

# This line "downloads" a mini AI model to your notebook
classifier = pipeline("sentiment-analysis")

# This is where the magic happens
result = classifier("I am normal")
print(result)


#day1 :)
