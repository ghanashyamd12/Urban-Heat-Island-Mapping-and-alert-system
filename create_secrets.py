import os

# Ensure .streamlit folder exists
secrets_dir = r"C:\Users\LENOVO\Downloads\UHI_Mapping_Project (3)\.streamlit"
os.makedirs(secrets_dir, exist_ok=True)

# Write the secrets.toml file
secrets_path = os.path.join(secrets_dir, "secrets.toml")
with open(secrets_path, "w", encoding="utf-8") as f:
    f.write('[default]\n')
    f.write('OPENWEATHER_API = "8ee3ec57d591ed4e62ac1c71266c339e"\n')

print("✅ secrets.toml created successfully.")
