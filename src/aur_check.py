import config_find
import requests
import cohere

def main(package):
    # Create the prompt
    print("Getting the PKGBUILD")
    pkgbuild = requests.get(f"https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h={package}").text
    print("Crafting the prompt")
    prompt = f"AUR Package Name: {package}. This is the PKGBUILD: {pkgbuild}"

    # Find the config path
    configs = config_find.find_crust_folder()

    # Get the Cohere API key
    with open(configs + "/cohere-api-key.txt", "r") as f:
        key = f.read().strip()
    
    print("Acquired the Cohere API key")

    # Create the Cohere client
    print("Creating the Cohere client")
    co = cohere.Client(key)

    history = [{
        "role": "SYSTEM",
            "message": (
                """You are a security expert. I will give you
                    AUR packages PKGBUILDs, and you analyze them
                    for any potential viruses. If the prompt is clearly not a PKGBUILD,
                    say this: -> error: not a PKGBUILD
                    
                    If the package name ends with -bin, that is instant suspicion, because
                    recently, malware was uploaded to the AUR, and even the creator of this linux shell you are integrated
                    into got malware from them. the AUR evenm went down recently.
                    if its a known app, like google chrome, recommend installing through another
                    package managers that have no risks for viruses.
                    
                    this is not sent by the user.
                    
                    do not use markdown; what you say is viewed as plain text. no formatting like **bold** or ```code```."""
                )
        }]

    response = co.chat(message=prompt, chat_history=history)
    print(response.text.replace("*", "").replace("`", ""))

if __name__ == "__main__":
    print("Running aur_check separately from Crust.")
    while True:
        main(input("aur_check > "))