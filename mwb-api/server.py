from mcp.server.fastmcp import FastMCP
import requests
import json

mcp = FastMCP("Metabolomics Workbench API")

@mcp.tool()
async def fetch_studies(study_id: str = "ST") -> list:
    """
    Fetch study information from the Metabolomics Workbench API.
    
    Parameters:
    study_id (str): The study ID to fetch. Can be a specific ID like 'ST000001' 
                    or a partial ID like 'ST0004' to fetch multiple studies.
                    Defaults to 'ST' which retrieves all studies.
    
    Returns:
    list: A list of study information dictionaries
    """
    base_url = "https://www.metabolomicsworkbench.org/rest/study/study_id"
    url = f"{base_url}/{study_id}/summary"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx/5xx responses
        
        # The API returns data as a list of studies
        data = response.json()
        
        # Process the response to ensure it's always a list
        if isinstance(data, dict) and 'study' in data:
            # If there's only one study, the API might return it directly
            if isinstance(data['study'], list):
                return data['study']
            else:
                return [data['study']]
        elif isinstance(data, list):
            return data
        else:
            return [data]  # Wrap any unexpected format in a list
            
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Failed to parse API response as JSON"}

def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()