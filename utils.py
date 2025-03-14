def print_error(message):
    print("\n" + "=" * 60)
    print("\033[91m🚨 ERROR 🚨\033[0m")  # Red Bold Error Header
    print(f"\033[91m❌ {message}\033[0m")  # Red Text
    print("=" * 60 + "\n")

def print_success(message):
    print(f"\033[92m✅ {message}\033[0m")  # Green Text

def print_info(message):
    print(f"\033[94mℹ️  {message}\033[0m")  # Blue Text
    
def print_warning(message):
    print(f"\033[93m⚠️  {message}\033[0m")  # Yellow Text