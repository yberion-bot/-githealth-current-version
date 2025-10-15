import web

# Check the GitHub repository directly
url = "https://github.com/yberion-bot/yberion.git"
response = web.open_url(url)

# Simply print status of the repository page access
if response:
    print("GitHub repository is reachable. Check the commits tab for the latest push.")
else:
    print("Unable to reach the repository.")