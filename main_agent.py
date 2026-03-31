from langchain_ollama import OllamaLLM
from auditor_tool import DataAuditor # This imports your code from earlier

# Then initialize it like this:
llm = OllamaLLM(model="llama3")

# 2. Get the Data Summary from our "Eyes"
auditor = DataAuditor("sample_data.csv")
data_summary = auditor.get_audit_summary()

# 3. Create a Professional Prompt
prompt = f"""
You are a Data Repair Agent. Look at this metadata summary and return ONLY a JSON list of fixes.
Do not write any conversational text.

DATA SUMMARY:
{data_summary}

RETURN ONLY A JSON LIST LIKE THIS:
[
  {{"column": "monthly_spend", "old_value": "FREE", "new_value": "0.0"}},
  {{"column": "signup_date", "old_value": "not_a_date", "new_value": "2023-01-01"}}
]
"""

# 4. Get the AI's Analysis
print("The AI is auditing your data...")
response = llm.invoke(prompt)
print("\n--- AI AUDIT REPORT ---")
print(response)
import json

# ... (your previous code) ...

print("\n--- EXECUTING AUTOMATED FIXES ---")

try:
    # 1. Clean the response (remove any extra text if the AI was chatty)
    # This finds the first '[' and last ']'
    json_start = response.find('[')
    json_end = response.rfind(']') + 1
    clean_json = response[json_start:json_end]

    # 2. Parse the string into a Python List
    fixes = json.loads(clean_json)

    # 3. The Automation Loop
    for fix in fixes:
        col = fix['column']
        old = fix['old_value']
        new = fix['new_value']

        # Call the tool we wrote in the auditor_tool file!
        result = auditor.fix_column_value(col, old, new)
        print(result)

    print("\nSUCCESS: All detected issues have been addressed.")
    print("Check 'cleaned_data.csv' to see the results!")

except Exception as e:
    print(f"Error parsing AI commands: {e}")
    print("Raw AI Output was:", response)
    # 3. The Automation Loop with HITL Safety
    for fix in fixes:
        col = fix['column']
        old = fix['old_value']
        new = fix['new_value']

        # Ask for Permission!
        print(f"\nPROPOSAL: Change '{old}' to '{new}' in column '{col}'?")
        user_choice = input("Approve this change? (y/n): ")

        if user_choice.lower() == 'y':
            result = auditor.fix_column_value(col, old, new)
            print(f"✅ {result}")
        else:
            print(f"❌ Skipping fix for {col}.")