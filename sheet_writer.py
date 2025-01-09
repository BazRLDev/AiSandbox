import os
import google.auth
import google.generativeai as genai
import json
import re
import typing_extensions as typing

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class Suggestion(typing.TypedDict):
    prompt: str

class GeminiResponse(typing.TypedDict):
    suggestions: list[Suggestion]

def get_sheet_service():
    """Authenticates with Google using the service account and returns the Google Sheets API service."""
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        service = build("sheets", "v4", credentials=creds)
        return service
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

def read_sheet_data(service, spreadsheet_id, sheet_name):
     """Reads all data from the specified sheet and returns it as a list of rows."""
     try:
         sheet = service.spreadsheets()
         result = sheet.values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
         values = result.get("values", [])
         if not values:
           print("No data found")
           return None
         return values
     except HttpError as error:
       print(f"An error occurred: {error}")
       return None

def find_column_index(headers, column_name):
   """Finds the 0-indexed column index based on a column header name.

   Args:
       headers: A list of strings representing the column headers.
       column_name: The name of the column to find.

   Returns:
       The 0-indexed column index, or None if the column is not found.
   """
   try:
      return headers.index(column_name)
   except ValueError:
      print(f"Could not find column header: {column_name}")
      return None

def write_sheet_data(service, spreadsheet_id, sheet_name, data, target_column):
   """Writes data to a sheet into the specified column(s), overwriting any existing data.

   Args:
       service: The Google Sheets API service object.
       spreadsheet_id: The ID of the Google Sheet.
       sheet_name: The name of the sheet/tab.
       data: A list of lists representing the data to write.
       target_column: The starting column (0-indexed) where the write operation should begin.
   """
   try:
      sheet = service.spreadsheets()
      read_result = sheet.values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
      existing_values = read_result.get("values", [])
      row_count = len(existing_values)
      if row_count == 0:
        row_count = 1 # if there are no rows set it to 1

      start_column_letter = chr(ord('A') + target_column)
      end_column_letter = chr(ord('A') + target_column + len(data[0]) -1)

      # Construct the range where we'll write, e.g., "C1:C5"
      range_to_write = f"{start_column_letter}2:{end_column_letter}{row_count}"
      body = {"values": data}

      result = sheet.values().update(spreadsheetId=spreadsheet_id, range=range_to_write, valueInputOption="USER_ENTERED", body=body).execute()
      print(f"{result.get('updatedCells')} cells updated")

   except HttpError as error:
      print(f"An error occurred: {error}")
      return False

def ask_gemini(phrase):
    print('we asking gemini!!!' + phrase)
    genai.configure(api_key=GEMINI_API_KEY, transport='rest')
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt_background = """The images should be appropriate for a family-friendly context and should not depict any violence, hate speech, illegal activities, or sexually suggestive content.

    Please avoid making suggestions that are related to harmful substances, weapons, or offensive content.

    The images should be either:
    - Generic Irish scenery or imagery (i.e. rolling green hills, connemara landscape, or traditional buildings) or
    - Images related to the contents of the phrase (as long as they conform to the restrictions)
    - Overall the images should help a user feel a combination of inspired or reflective depending on the content of the phrase

    Can you suggest three possible images for the following phrase:

    {phrase}

    Note you only need to priovide the detailed image description, no need for 'Image 1:' or 'First image:' prefix.

    """
    full_prompt = prompt_background.format(phrase=phrase)
    print('@@@@@')
    # print(full_prompt)
    print('@@@@@')
    generation_config = genai.types.GenerationConfig(
       response_mime_type="application/json", response_schema=GeminiResponse
    )

    response = model.generate_content(full_prompt, generation_config = generation_config)
    print(f"Raw response from Gemini: {response.text}")

    try:
      json_response = json.loads(response.text)
      return formated_gemini_response_json(json_response)
    except json.JSONDecodeError as e:
      print(f"Error decoding JSON: {e}")
      print(f"Response text: {response.text}")
      return None

def formated_gemini_response_json(response_json):
    return [response_json['suggestions'][0]['prompt'], response_json['suggestions'][1]['prompt'], response_json['suggestions'][2]['prompt']]

def main():
    service = get_sheet_service()
    if not service:
        print('you done messed up')
        return

    print("Attempt to read from Google Sheets:")
    # Read data from the sheet
    sheet_data = read_sheet_data(service, SPREADSHEET_ID, SHEET_NAME)
    if sheet_data:
        print("Data read from Google Sheets:")
        headers = sheet_data[0]
        new_data = []
        for index,row in enumerate(sheet_data):
            print(row)
            if index == 0:
                continue
            else:
                phrase = row[0]
                print("Attempt to ask Gemini:")
                image_prompts = ask_gemini(phrase)
                new_data.append(image_prompts)
        # print('we are done')
        # print(new_data)
        target_column_header = "First Suggestion" # CHANGE ME!
        target_column_index = find_column_index(headers, target_column_header)
        if write_sheet_data(service, SPREADSHEET_ID, SHEET_NAME, new_data, target_column_index) == False:
            print("Could not write to sheet")

    else:
        print("Could not read sheet data")
        return

if __name__ == "__main__":
    main()