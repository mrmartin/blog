#!/usr/bin/env python3
# coding: utf-8

import sys
from langchain_community.llms.llamafile import Llamafile
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def main(topic, output_file):
    # Initialize the LLM
    llm = Llamafile(base_url="https://chat.lkrobots.com")

    # Define author and critic personas
    author_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a diligent worker, taking constructive criticism to heart in order to improve your argument. Take comments and work them out in depth."),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    author = author_prompt | llm

    critic_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a reviewer who focuses on finding flaws in arguments, and provides constructive criticism so that your interlocutor can improve. Let them figure out the answers and arguments to be made."),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    critic = critic_prompt | llm

    consensus_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are consensus-bot, a helpful assistant that chairs conversations. You analyze dialogue and decide whether or not it has ended. Your output is always a single word: either YES or NO."),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    consensus = consensus_prompt | llm

    # Initialize conversation history
    conversation_history = [f"{topic}<|eot_id|>"]

    # Main conversation loop
    for i in range(10):
        print(f"Iteration {i}: Critic's turn")
        
        # Critic responds
        messages_from_critic_perspective = [
            HumanMessage(content=msg) if j % 2 == 0 else AIMessage(content=msg)
            for j, msg in enumerate(conversation_history)
        ]
        critic_response = critic.invoke(messages_from_critic_perspective)
        print(f"Critic response: {critic_response}")
        conversation_history.append(critic_response)

        print(f"Iteration {i}: Author's turn")
        
        # Author responds
        messages_from_author_perspective = [
            AIMessage(content=msg) if j % 2 == 0 else HumanMessage(content=msg)
            for j, msg in enumerate(conversation_history)
        ]
        author_response = author.invoke(messages_from_author_perspective)
        print(f"Author response: {author_response}")
        conversation_history.append(author_response)

        # Check for consensus
        query_about_last_two_messages = f"""Consider the original topic of the discussion: "{conversation_history[0]}".

        The two sides' last messages were:
        one side: {conversation_history[-2]}

        and 
        other side: {conversation_history[-1]}

        Have they reached a consensus that means the conversation can end? Answer only YES or NO, no other text<|eot_id|>"""
        
        consensus_response = consensus.invoke([HumanMessage(content=query_about_last_two_messages)])
        print(f"Consensus response: {consensus_response}")
        
        if i>2 and "YES" in consensus_response:
            print("Consensus reached")
            break

    # Summarize the discussion into an article
    summary_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an editor for online articles. Your task is to take arbitrary text about a topic, and convert it into a well structured and engaging article to be published online. Your output must be valid Markdown."),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    summary = summary_prompt | llm

    summary_article_query = f"""Consider the original topic of the discussion: "{conversation_history[0]}".

    Now, consider the discussion that ensued:
    {" ".join(conversation_history[1:])}

    I'm not interested in the sides taken and in who said what, I am interested in the critical topics and arguments made. Write an engaging article about this topic, using the arguments, questions, and answers of the discussion.

    Write an article in Markdown<|eot_id|>"""
    
    final_article = summary.invoke([HumanMessage(content=summary_article_query)])

    # Save the final article to the output file
    with open(output_file, "w") as f:
        f.write(final_article)

    print("Final article saved to:", output_file)
    print("\nDiscussion preceding the article:")
    print("\n".join(conversation_history))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: generate_article.py <topic> <output_file>")
        sys.exit(1)
    
    topic = sys.argv[1]
    output_file = sys.argv[2]
    main(topic, output_file)
