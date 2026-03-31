import pandas as pd


class DataAuditor:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    def get_audit_summary(self):
        """Creates a summary of the data for the AI to read."""
        summary = []
        for col in self.df.columns:
            # Check for nulls
            null_count = self.df[col].isnull().sum()
            # Get data type
            dtype = str(self.df[col].dtype)
            # Get a sample of unique values
            sample_values = self.df[col].dropna().unique()[:3].tolist()

            col_info = f"Column: {col} | Type: {dtype} | Nulls: {null_count} | Sample: {sample_values}"
            summary.append(col_info)

        return "\n".join(summary)

    def fix_column_value(self, column_name, old_value, new_value):
        """Replaces a specific messy value with a clean one and tries to fix the type."""
        print(f"--- ACTION: Replacing '{old_value}' with '{new_value}' in {column_name} ---")

        # 1. Replace the value
        self.df[column_name] = self.df[column_name].replace(old_value, new_value)

        # 2. Smart Type Casting: If it's the monthly_spend, try to make it a float
        if column_name == 'monthly_spend':
            self.df[column_name] = pd.to_numeric(self.df[column_name], errors='coerce')

        # 3. Save the 'Cleaned' version
        self.df.to_csv("cleaned_data.csv", index=False)
        return f"Successfully updated {column_name}."


# Test it!
auditor = DataAuditor("sample_data.csv")
print(auditor.get_audit_summary())


