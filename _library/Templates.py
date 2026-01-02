from . import Preferences as myPreferences
from . import Terminal as myTerminal
from . import Inputs as myInput
import os
import re

# Import NoteData from Notes module
from .Tools import generate_unique_identifier, letters_and_numbers_only

def read_Template(templatePath: str) -> str:
    """
    Reads the content of a template file.
    
    Args:
        templatePath (str): The path to the template file.
        
    Returns:
        str: The content of the template file.
        
    Raises:
        FileNotFoundError: If the template file does not exist.
    """
    
    if os.path.exists(templatePath) is False:
        print (f"{myTerminal.ERROR}Template file '{templatePath}' does not exist.{myTerminal.RESET}")
        return ""
    else:
        with open(templatePath, 'r', encoding='utf-8') as f:
            return f.read()
        
def get_mergeable_tags_from_template(template: str) -> list:
    """
    Extracts mergeable tags from a template string.
    
    Args:
        templateBody (str): The template string containing placeholders.
    Returns:
        list: A list of unique mergeable tags found in the template.
    """
    templateTags = re.findall(r"\[(.*?)\]", template)
    uniqueTags = list(set(templateTags))
    uniqueTags = [f"[{tag}]" for tag in uniqueTags]
    return uniqueTags


def merge_template_with_values(timestamp_id, timestamp_full, selectedProjectName, 
                               template: str, 
                               mergeData: dict,
                               runSilent: bool = False,
                               processUnPopulatedNoteBodyMergeTags: bool = True) -> tuple[str, str]:
    """
    Merges a template string with values from a dictionary.
    
    Args:
        template (str): The template string containing placeholders.
        values (dict): A dictionary containing values to replace the placeholders.
        runSilent (bool): If True, skips prompting for missing tags, replacing them with blank strings.
        processUnPopulatedNoteBodyMergeTags (bool): If False, skips prompting for missing tags in the body, use this
        option when building an atomic note from an existing body to avoid treating backlinks as mergeable tags.

    Returns:
        str: The merged string with placeholders replaced by actual values.
    """
     
    #handle the common date tags with hard coded values 
    timestamp_id = timestamp_id.split("_")[0]  # Ensure timestamp_id is just the date part
    template = template.replace("[YYYYMMDDHHMMSS]", timestamp_id)
    template = template.replace("[TIMESTAMP_ID]", timestamp_id)
    template = template.replace("[YYYY-MM-DD HH:MM:SS]", timestamp_full)
    template = template.replace("[DATETIME]", timestamp_full)
    template = template.replace("[YYYY-MM-DD]", timestamp_full.split(" ")[0])
    template = template.replace("[DATE]", timestamp_full.split(" ")[0])
    template = template.replace("[Current User]", myPreferences.author_name())

    #handle the project, author and tags with synonyms    
    projectTag_synonyms = ["Project Name", "ProjectName", "Project"]
    authorTag_synonyms = ["Current User", "User", "Username", "Author", "author"]
    tagTag_synonyms = ["tags", "Tags", "TAGS"]
    checkboxTag_synonyms = ["CHECKBOX_UNCHECKED", "CHECKBOX INCOMPLETE"] 
    checkboxCompleteTag_synonyms = ["CHECKBOX_CHECKED", "CHECKBOX COMPLETE"] 
    title = ""

    mergeData["Current User"] = myPreferences.author_name()

    for key, value in mergeData.items():
        if key in projectTag_synonyms:
            for synonym in projectTag_synonyms:
                placeholder = f"[{synonym}]"
                template = template.replace(placeholder, value)
        elif key in authorTag_synonyms:
            for synonym in authorTag_synonyms:
                placeholder = f"[{synonym}]"
                template = template.replace(placeholder, value)
        elif key in tagTag_synonyms:
            for synonym in tagTag_synonyms:
                placeholder = f"[{synonym}]"
                template = template.replace(placeholder, value)
                tags = ""
                for tag in value.split(","):
                    tag = tag.strip().replace(" ","_")
                    tags += f"#{tag} "
                template = template.replace(placeholder, tags.strip())
        else:
            if key.upper() == "TITLE":
                title = value
            placeholder = f"[{key}]"
            # Case-insensitive replace for placeholders
            pattern = re.compile(re.escape(placeholder), re.IGNORECASE)
            template = pattern.sub(str(value), template)
    
    
    #replace empty tags with a blank string
    if processUnPopulatedNoteBodyMergeTags:
        mergeableTemplateTags = get_mergeable_tags_from_template(template)
        for tag in mergeableTemplateTags:
            if tag in checkboxTag_synonyms:
                for synonym in checkboxTag_synonyms:
                    template = template.replace(tag, "- [ ] ")
            elif tag in checkboxCompleteTag_synonyms:
                for synonym in checkboxCompleteTag_synonyms:
                    template = template.replace(tag, "- [x] ")
            else:
                if runSilent:
                    #template = template.replace(f"{tag}", f"debug-empty-{tag}")
                    template = template.replace(f"{tag}", "")
                else:
                    userInput = myInput.ask_for_template_Tag_Value_from_user(tag,"")
                    template = template.replace(f"{tag}", userInput)
    
    titleLettersAndNumbers = letters_and_numbers_only(title)  # Limit to 200 characters and remove special characters
    uniqueIdentifier = generate_unique_identifier(timestamp_id, ("task" if processUnPopulatedNoteBodyMergeTags else "atomic"), titleLettersAndNumbers)

    return uniqueIdentifier, template
