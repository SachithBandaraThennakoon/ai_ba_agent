from agents.client_agent import client_agent
from agents.ba_agent import ba_agent
from agents.solution_architect_agent import solution_architect_agent
from agents.final_proposal_agent import final_proposal_agent
from utils.file_saver import save_markdown

if __name__ == "__main__":
    print("=== Client → Client Agent → BA Agent → Solution Architect ===\n")

    client_input = input("Client: ")

    print("\n--- Client Agent Output ---")
    client_output = client_agent(client_input)
    print(client_output)

    print("\n--- BA Agent Output ---")
    ba_output = ba_agent(client_output)
    print(ba_output)

    print("\n--- Solution Architect Output ---")
    architect_output = solution_architect_agent(ba_output)
    print(architect_output)

    

    print("\n--- Final Proposal ---")
    final_output = final_proposal_agent(ba_output, architect_output)
    print(final_output)

    # Save to markdown
    file_path = save_markdown(final_output)
    print(f"\n✅ Proposal saved as Markdown: {file_path}")


