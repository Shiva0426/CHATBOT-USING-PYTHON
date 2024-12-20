#CHATBOT USING PYTHON


#Libraries Used:

#speech_recognition: Captures and converts speech input from the user into text.
#pyttsx3: Converts the chatbot's text responses into speech.
#openai: Utilizes OpenAI's GPT model to generate natural language responses.

#Initialization:

#The OpenAI API key is set using openai.api_key.
#pyttsx3 is configured to use a specific voice for text-to-speech conversion.
#The microphone and recognizer are initialized for audio input.

#Conversation Loop:

#The program listens to the user's speech via the microphone and processes it into text using Google Speech Recognition.
#The user's input, along with the chatbot's past responses, is sent as a prompt to OpenAI GPT, ensuring contextual understanding.
#GPT generates a response, which is appended to the conversation history.
#The chatbot's response is displayed as text and spoken aloud using pyttsx3.

#OpenAI GPT Integration:

#temperature: Controls the randomness of the output. A value of 0.7 balances creativity and relevance.
#max_tokens: Specifies the maximum number of tokens (words and punctuation) in the response.

#Error Handling:

#The program gracefully handles cases where audio cannot be understood by re-prompting the user.



import speech_recognition as sr  # For speech-to-text conversion
import pyttsx3  # For text-to-speech conversion
import openai  # For generating chatbot responses using OpenAI's GPT model

# Initialize OpenAI API key (replace with your own key)
openai.api_key = "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"  # Replace with your OpenAI API key

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set the voice (index 1 for female, index 0 for male)

# Initialize speech recognition
recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=1)  # Specify microphone device index

# Conversation tracking variables
conversation = ""  # Stores the entire conversation
user_name = "Nikky"  # Name of the user
bot_name = "Kittu"  # Name of the chatbot

# Continuous interaction loop
while True:
    # Capture audio input from the microphone
    print("\nListening...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.2)  # Adjust for background noise
        audio = recognizer.listen(source)  # Record user's audio
    print("Processing input...")

    try:
        # Convert user's speech to text
        user_input = recognizer.recognize_google(audio)
        print(f"{user_name}: {user_input}")
    except Exception:
        # If speech is not recognized, prompt the user again
        print("Sorry, I couldn't understand that. Please try again.")
        continue

    # Append the user's input to the conversation
    prompt = f"{user_name}: {user_input}\n{bot_name}:"
    conversation += prompt

    # Generate chatbot response using OpenAI GPT
    response = openai.Completion.create(
        model="text-davinci-003",  # OpenAI's language model
        prompt=conversation,  # Context of the conversation so far
        temperature=0.7,  # Controls randomness in responses
        max_tokens=256,  # Maximum length of the response
        top_p=1,  # Controls diversity of the output
        frequency_penalty=0,  # Penalizes repetitive phrases
        presence_penalty=0  # Encourages new topic generation
    )

    # Extract and process the response text
    response_text = response["choices"][0]["text"].strip()
    print(f"{bot_name}: {response_text}")
    
    # Add the chatbot's response to the conversation history
    conversation += f"{response_text}\n"

    # Convert the chatbot's response to speech
    engine.say(response_text)
    engine.runAndWait()
