import re
from pathlib import Path
from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)


def get_response_text(result):
    """Extract readable text from a LangChain agent response."""
    if isinstance(result, dict) and "messages" in result:
        messages = result["messages"]
        if not messages:
            return ""
        content = messages[-1].content
    else:
        content = getattr(result, "content", result)

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))
            elif isinstance(item, str):
                text_parts.append(item)
        return "\n".join(text_parts)

    return str(content)


def extract_urls(text):
    """Extract unique HTTP/HTTPS URLs from search results."""
    urls = re.findall(r"https?://[^\s<>\"']+", text)
    urls = [url.rstrip(".,;:!?)\u005d}") for url in urls]
    return list(dict.fromkeys(urls))


def main():
    topic = input("Enter your research topic: ").strip()

    if not topic:
        print("Please enter a research topic.")
        return

    try:
        # STEP 1: Search the web.
        print("\n[1/4] Starting search agent...")

        search_agent = build_search_agent()

        search_result = search_agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Research the topic: {topic}. "
                        "Use the web_search tool to find relevant sources. "
                        "Summarize the findings and include the source URLs."
                    ),
                }
            ]
        })

        search_text = get_response_text(search_result)
        print("Search stage completed.")

        # STEP 2: Read webpages.
        print("\n[2/4] Starting reader agent...")

        urls = extract_urls(search_text)

        if urls:
            urls_to_read = urls[:5]
            reader_agent = build_reader_agent()

            reader_result = reader_agent.invoke({
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            f"Research topic: {topic}\n"
                            "Use the scrape_url tool to read these pages. "
                            "Summarize their relevant information and "
                            "preserve their source URLs.\n\n"
                            + "\n".join(urls_to_read)
                        ),
                    }
                ]
            })

            reader_text = get_response_text(reader_result)
            print(f"Reading stage completed. URLs supplied: {len(urls_to_read)}")
        else:
            print("No URLs found in search output.")
            print("Using the search results as research material.")
            reader_text = search_text

        research = (
            f"SEARCH RESULTS:\n{search_text}\n\n"
            f"WEBPAGE READING:\n{reader_text}"
        )

        # STEP 3: Write the research report.
        print("\n[3/4] Generating research report...")

        report = writer_chain.invoke({
            "topic": topic,
            "research": research,
        })

        print("Report generation completed.")

        # STEP 4: Critically evaluate the report.
        print("\n[4/4] Reviewing report...")

        review = critic_chain.invoke({
            "report": report,
        })

        print("Critic review completed.")

        # Display the report.
        print("\n" + "=" * 60)
        print("FINAL RESEARCH REPORT")
        print("=" * 60)
        print(report)

        # Display the review.
        print("\n" + "=" * 60)
        print("CRITIC REVIEW")
        print("=" * 60)
        print(review)

        # Save both outputs to a text file.
        output = (
            f"RESEARCH TOPIC: {topic}\n\n"
            f"{'=' * 60}\n"
            f"FINAL RESEARCH REPORT\n"
            f"{'=' * 60}\n\n"
            f"{report}\n\n"
            f"{'=' * 60}\n"
            f"CRITIC REVIEW\n"
            f"{'=' * 60}\n\n"
            f"{review}\n"
        )

        output_path = Path(__file__).resolve().parent / "research_report.txt"
        output_path.write_text(output, encoding="utf-8")

        print("\nSUCCESS: Research workflow completed!")
        print(f"Report saved to: {output_path}")

    except Exception as error:
        print("\nERROR: Research workflow failed.")
        print(f"{type(error).__name__}: {error}")
        print(
            "\nCheck agents.py, tools.py, your internet connection, "
            "and your Gemini API configuration."
        )


if __name__ == "__main__":
    main()
