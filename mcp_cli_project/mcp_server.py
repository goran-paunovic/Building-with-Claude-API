from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_content",
    description="Read the content of a document given its ID and return the content as a string.",
)
def read_document(
    doc_id: str = Field(description="The ID of the document to read.")
):
    if doc_id in docs:
        return docs[doc_id]
    raise ValueError(f"Document with ID {doc_id} not found.")

@mcp.tool(
    name="edit_doc_content",
    description="Edit the document by replacing a string in the document with a new string.",
)
def edit_document(
    doc_id: str = Field(description="The ID of the document to edit."),
    old_string: str = Field(description="The string to be replaced in the document."),
    new_string: str = Field(description="The new string to replace the old string with."),
):
    if doc_id in docs:
        docs[doc_id] = docs[doc_id].replace(old_string, new_string)
        return docs[doc_id]
    raise ValueError(f"Document with ID {doc_id} not found.")

@mcp.resource(
    "docs://documents",
    mime_type="application/json",
)
def list_docs():
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
)
def fetch_doc(doc_id: str) -> str:
    if doc_id in docs:
        return docs[doc_id]
    raise ValueError(f"Document with ID {doc_id} not found.")

# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name="format",
    description="Rewrite a document in markdown format.",
)
def format_document(
    doc_id: str = Field(description="The ID of the document to format.")
) -> list[base.Message]:
    prompt = f"""
    You are a document formatting assistant. 
    Your task is to rewrite the content of the document with ID 
    <document_id>
    {doc_id}
    </document_id> in markdown format.
    Add in headers, bullet points, and other markdown formatting as appropriate.
    Feel free to add in additional information that is relevant to the document's content.
    Use the edit_doc_content tool to make edits to the document as needed.
    """

    return [base.UserMessage(prompt)]


# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
