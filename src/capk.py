import requests

def check_pypi(pkg):
    print("[PyPI] Checking...")
    return requests.get(f"https://pypi.org/pypi/{pkg}/json").status_code == 200

def check_aur(pkg):
    print("[AUR] Checking...")
    r = requests.get(f"https://aur.archlinux.org/rpc/?v=5&type=info&arg[]={pkg}")
    return r.ok and r.json().get("resultcount", 0) > 0

def check_apt(pkg):
    print("[APT] Checking...")
    r = requests.get(f"https://packages.ubuntu.com/search?keywords={pkg}&searchon=names&suite=all&section=all")
    return f"<a href=\"/{pkg}\"" in r.text

def check_dnf(pkg):
    print("[DNF] Checking...")
    r = requests.get(f"https://apps.fedoraproject.org/packages/{pkg}")
    return r.status_code == 200 and f">{pkg}<" in r.text

def check_npm(pkg):
    print("[npm] Checking...")
    return requests.get(f"https://registry.npmjs.org/{pkg}").status_code == 200

def check_crates(pkg):
    print("[crates.io] Checking...")
    return requests.get(f"https://crates.io/api/v1/crates/{pkg}").status_code == 200

def check_packagist(pkg):
    print("[Packagist] Checking...")
    return requests.get(f"https://repo.packagist.org/p/{pkg}.json").status_code == 200

def check_homebrew(pkg):
    print("[Homebrew] Checking...")
    r = requests.get(f"https://formulae.brew.sh/api/formula/{pkg}.json")
    return r.status_code == 200

def check_cpan(pkg):
    print("[CPAN] Checking...")
    r = requests.get(f"https://fastapi.metacpan.org/v1/release/{pkg}")
    return r.status_code == 200

def check_hackage(pkg):
    print("[Hackage] Checking...")
    r = requests.get(f"https://hackage.haskell.org/package/{pkg}")
    return r.status_code == 200 and "404" not in r.text

def check_chocolatey(pkg):
    print("[Chocolatey] Checking...")
    r = requests.get(f"https://community.chocolatey.org/packages/{pkg}")
    return r.status_code == 200 and pkg.lower() in r.text.lower()

def check_rubygems(pkg):
    print("[RubyGems] Checking...")
    return requests.get(f"https://rubygems.org/api/v1/gems/{pkg}.json").status_code == 200

def check_nuget(pkg):
    print("[NuGet] Checking...")
    r = requests.get(f"https://api.nuget.org/v3/registration5-semver1/{pkg.lower()}/index.json")
    return r.status_code == 200

def check_all(pkg):
    checkers = {
        "PyPI": check_pypi,
        "AUR": check_aur,
        "APT": check_apt,
        "DNF": check_dnf,
        "npm": check_npm,
        "crates.io": check_crates,
        "Packagist": check_packagist,
        "Homebrew": check_homebrew,
        "CPAN": check_cpan,
        "Hackage": check_hackage,
        "Chocolatey": check_chocolatey,
        "RubyGems": check_rubygems,
        "NuGet": check_nuget,
    }

    results = {}
    for name, func in checkers.items():
        try:
            results[name] = func(pkg)
        except Exception as e:
            print(f"[{name}] Error: {e}")
            results[name] = False
    return results

def search(pkg):
    print(f"\n🔍 Checking availability of '{pkg}' across package managers...\n")
    results = check_all(pkg)
    print(f"\n📦 Results for '{pkg}':")
    for repo, found in results.items():
        status = "✅ Found" if found else "❌ Not Found"
        print(f"{repo:<12}: {status}")
