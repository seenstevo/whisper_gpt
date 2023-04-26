# Spanish Conversation Tutor

## Description

This is a gradio app that combines the speech to text model of Whisper with the GPT large language model plus voice synthesis to create a Spanish conversational practice partner and tutor. The idea is to create an ever available and comfortable to use language learning aid. The real power of such an aid will be unlocked by including a vector database for long term memory so the tutor partner can tap into previous conversations, keep track of recurring errors or weaknesses and therefore have more personalised conversations and feedback.

## Use

Upon launching the gradio app, click on the "start recording" button and give permissions for access to microphone if required. Speak in Spanish about what ever you like in a way that may set up a short conversation. After clicking on "stop recording" we need to submit the audio to the models. This is currently very slow and involves the decoding and transcribing of the audio, the passing of the text to GPT and the voice synthesis of the response. Simply "Clear" and record another audio to keep the conversation going. When you want to stop, you need to say "hemos terminado". This is the command for the tutor to end the conversation and give feedback on your Spanish.

## Current Status and Future Plans

- Currently, the app loads in the Whisper "small" model but this may be adapted or swithced to the API. 
- Whisper often makes transcribing errors which are likely unavoidable but in part due to a non-native speaking Spanish. There could be scope for allowing fine tuning of the model on each student by reading a set text to improve the accuracy.
- The great power of this app will be the intergration with a vector database to store all conversations.
- This may also include a "getting to know you" conversation which, once stored in the DB, allows the tutor to have more personalised and tailored conversations.
- The current "system prompt" could be improved and possibly a few sub-roles could be created for certain variations of conversation such as role play.
- The feedback could involve specific vocabulary lists for the user to focus on and exercises for practicing particular weaknesses.
