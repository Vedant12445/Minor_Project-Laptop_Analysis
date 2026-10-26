import pandas as pd

categories = {
    "laptop": ("laptop.csv", "cleaned_laptop.csv"),
    "mouse": ("mouse.csv", "cleaned_mouse.csv"),
    "keyboard": ("keyboard.csv", "cleaned_keyboard.csv")
}

def clean_price(p):
    try:
        return float(str(p).replace("₹", "").replace(",", "").strip())
    except:
        return 0.0

def clean_discount(d):
    try:
        if "%" in str(d):
            return int(str(d).split("%")[0].strip())
    except:
        pass
    return 0

def clean_rating(r):
    try:
        return float(r)
    except:
        return None

for category, (input_csv, output_csv) in categories.items():
    print(f"\nReading and cleaning data for `{category}`...")

    # Read CSV safely
    try:
        df = pd.read_csv(input_csv, encoding='utf-8')
    except Exception as e:
        print(f"Failed to read {input_csv}: {e}")
        continue

    # Clean columns
    df['price'] = df['price'].apply(clean_price)
    df['original_price'] = df['original_price'].apply(clean_price)
    df['discount'] = df['discount'].apply(clean_discount)
    df['rating'] = df['rating'].apply(clean_rating)

    # Fill missing data
    df['price'] = df['price'].fillna(0.0)
    df['original_price'] = df['original_price'].fillna(0.0)
    df['rating'] = df['rating'].fillna(df['rating'].median())
    df['title'] = df['title'].fillna("Unknown Product")

    if 'brand' not in df.columns:
        df['brand'] = df['title'].apply(lambda x: x.split()[0] if pd.notnull(x) else "Unknown Brand")
    else:
        df['brand'] = df['brand'].fillna("Unknown Brand")

    # Save cleaned file
    df.to_csv(output_csv, index=False)
    print(f"Saved cleaned data to `{output_csv}`.")

print("\n✅ All categories cleaned and saved.")
