import pickle
import browser_cookie3

def get_cookies():
    # Specify the domain you want to extract cookies for
    domain = "airtasker.com"  # Replace with the actual domain

    # Load cookies from the user's browser
    # This will load cookies from all supported browsers
    cookies = browser_cookie3.load()

    # Filter cookies for the specified domain
    domain_cookies = [cookie for cookie in cookies if domain in cookie.domain]

    # Save the filtered cookies to a file using pickle
    with open('cookies.pkl', 'wb') as f:
        pickle.dump(domain_cookies, f)

    print(f"Cookies for {domain} have been saved to cookies.pkl")


def show_cookie_names():
    with open('cookies.pkl', 'rb') as f:
        cookies = pickle.load(f)

    # Print the key (name) of each cookie
    for cookie in cookies:
        print(cookie.name)
        
def get_cookie():
    import browser_cookie3

    # Specify the domain you want to extract cookies for
    domain = "airtasker.com"  # Replace with the actual domain (e.g., 'example.com')

    # Load cookies from the user's browser
    cookies = browser_cookie3.load(domain_name=domain)

    # Look for the sessionid cookie
    sessionid = None
    for cookie in cookies:
        if cookie.name == 'at_sid':
            sessionid = cookie.value
            break

    # Check if the sessionid was found
    if sessionid:
        print(f"Session ID: {sessionid}")
    else:
        print("Session ID not found for the specified domain.")
        
get_cookie()