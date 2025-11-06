from mcp.server.fastmcp import FastMCP
import requests
import json
import os
import argparse

BASE_URL = "https://www.metabolomicsworkbench.org/rest"


# Initialize FastMCP with port configuration
def _init_mcp():
    """Initialize MCP server with host and port from environment"""
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_PORT", 8080))
    return FastMCP("Metabolomics Workbench API", host=host, port=port), host, port


mcp, HOST, PORT = _init_mcp()


@mcp.tool()
def get_all_studies() -> dict:
    """
    Show all publicly available studies (Project, Study, Analysis ID)

    Parameters:
    None

    Returns:
    dict: A dictionary containing all available studies or an error message.
    """
    return _get("study/study_id/ST/available")


@mcp.tool()
def get_study_summary(study_id: str = "ST") -> dict:
    """
    Fetch summary information for a study

    Parameters:
    study_id (str): The study ID to fetch. Can be a specific ID like 'ST000001'
                    or a partial ID like 'ST0004' to fetch multiple studies.
                    Defaults to 'ST' which retrieves all studies.

    Returns:
    dict: A dictionary containing the study summary or an error message.
    """
    return _get(f"study/study_id/{study_id}/summary")


@mcp.tool()
def get_study_samples_and_experimental_variables(study_id: str = "ST") -> dict:
    """
    Fetch samples and experimental variables (factors) for a study

    Parameters:
    study_id (str): The study ID to fetch. Can be a specific ID like 'ST000001'
                    or a partial ID like 'ST0004' to fetch multiple studies.
                    Defaults to 'ST' which retrieves all studies.

    Returns:
    dict: A dictionary containing the study factors or an error message.
    """
    return _get(f"study/study_id/{study_id}/factors")


@mcp.tool()
def get_all_study_summaries() -> dict:
    """
    Fetch summary information for all studies

    Parameters:
    None

    Returns:
    dict: A dictionary containing all study summaries or an error message.
    """
    return _get("study/study_id/ST/summary")


@mcp.tool()
def get_study_analysis(study_id: str = "ST") -> dict:
    """
    Fetch analysis information for a study

    Parameters:
    study_id (str): The study ID to fetch. Can be a specific ID like 'ST000001'
                    or a partial ID like 'ST0004' to fetch multiple studies.
                    Defaults to 'ST' which retrieves all studies.

    Returns:
    dict: A dictionary containing the study analysis or an error message.
    """
    return _get(f"study/study_id/{study_id}/analysis")


@mcp.tool()
def get_study_metabolites(study_id: str = "ST") -> dict:
    """
    Fetch metabolites and annotations detected in a study (one study at a time)

    Parameters:
    study_id (str): The study ID to fetch. Must be a specific ID like 'ST000001'

    Returns:
    dict: A dictionary containing the study metabolites or an error message.
    """
    return _get(f"study/study_id/{study_id}/metabolites")


@mcp.tool()
def get_study_metabolites_measurements(study_id: str = "ST") -> dict:
    """
    Fetch metabolites measurements for a study (one study at a time)

    Parameters:
    study_id (str): The study ID to fetch. Must be a specific ID like 'ST000001'

    Returns:
    dict: A dictionary containing the study metabolites or an error message.
    """
    return _get(f"study/study_id/{study_id}/data")


@mcp.tool()
def get_study_species(study_id: str = "ST") -> dict:
    """
    Fetch species information for a study

    Parameters:
    study_id (str): The study ID to fetch. Can be a specific ID like 'ST000001'
                    or a partial ID like 'ST0004' to fetch multiple studies.
                    Defaults to 'ST' which retrieves all studies.

    Returns:
    dict: A dictionary containing the study analysis or an error message.
    """
    return _get(f"study/study_id/{study_id}/species")


@mcp.tool()
def get_study_source(study_id: str = "ST") -> dict:
    """
    Fetch sample source information for a study

    Parameters:
    study_id (str): The study ID to fetch. Can be a specific ID like 'ST000001'
                    or a partial ID like 'ST0004' to fetch multiple studies.
                    Defaults to 'ST' which retrieves all studies.

    Returns:
    dict: A dictionary containing the study analysis or an error message.
    """
    return _get(f"study/study_id/{study_id}/source")


@mcp.tool()
def get_study_disease(study_id: str = "ST") -> dict:
    """
    Fetch disease association (where applicable) for a study

    Parameters:
    study_id (str): The study ID to fetch. Can be a specific ID like 'ST000001'
                    or a partial ID like 'ST0004' to fetch multiple studies.
                    Defaults to 'ST' which retrieves all studies.

    Returns:
    dict: A dictionary containing the study analysis or an error message.
    """
    return _get(f"study/study_id/{study_id}/disease")


@mcp.tool()
def get_all_studies_untargeted() -> dict:
    """
    Fetch list of studies with untargeted data in NMDR

    Parameters:
    None

    Returns:
    dict: A dictionary containing all available studies or an error message.
    """
    return _get("study/study_id/X/untarg_studies")


@mcp.tool()
def get_study_named_metabolites(study_id: str = "ST") -> dict:
    """
    Fetch list of studies with named metabolites in NMDR

    Parameters:
    study_id (str): The study ID to fetch. Can be a specific ID like 'ST000001'
                    or a partial ID like 'ST0004' to fetch multiple studies.
                    Defaults to 'ST' which retrieves all studies.

    Returns:
    dict: A dictionary containing the study analysis or an error message.
    """
    return _get(f"study/study_id/{study_id}/named_metabolites")


@mcp.tool()
def get_study_number_of_metabolites(study_id: str = "ST") -> dict:
    """
    Show number of named metabolites in a study

    Parameters:
    study_id (str): The study ID to fetch. Can be a specific ID like 'ST000001'
                    or a partial ID like 'ST0004' to fetch multiple studies.
                    Defaults to 'ST' which retrieves all studies.

    Returns:
    dict: A dictionary containing the study analysis or an error message.
    """
    return _get(f"study/study_id/{study_id}/number_of_metabolites")


def _get(endpoint, params=None):
    """
    Makes a GET request to the specified endpoint.

    Parameters:
    endpoint (str): The API endpoint to call.
    params (dict, optional): A dictionary of query parameters. Defaults to None.

    Returns:
    dict: The JSON response from the API.
    """
    url = f"{BASE_URL}/{endpoint}"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes

        # The API returns data as a list of studies
        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Failed to parse API response as JSON"}


def main():

    # Parse command-line arguments (default transport is 'stdio')
    parser = argparse.ArgumentParser(description="Run Metabolomics Workbench MCP server")
    parser.add_argument(
        "-t",
        "--transport",
        choices=["stdio", "streamable-http"],
        default=os.environ.get("MCP_TRANSPORT", "stdio"),
        help="Transport to use for MCP server. Default: 'stdio'",
    )
    args = parser.parse_args()
    transport = args.transport

    if transport == "stdio":
        """
        Run the MCP server with stdio transport.
        This is for local testing with an LLM that supports stdio transport.
        """
        print("Starting MCP server with stdio transport...")
        print("MCP Server is running...")

        # Use stdio transport
        mcp.run(transport="stdio")
    elif transport == "streamable-http":
        """
        Run the MCP server with streamable-http transport.
        This is for remote access through a reverse proxy like Nginx.
        """
        print("Starting MCP server with streamable-http transport...")
        print(f"MCP Server is running at http://{HOST}:{PORT}...")

        # Use streamable-http transport
        mcp.run(transport="streamable-http")
    else:
        print(f"Unknown transport: {transport}. Please use 'stdio' or 'streamable-http'.")
        return


if __name__ == "__main__":
    main()
