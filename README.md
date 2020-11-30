# Investnow To Sharesight

Converts Investnow Investor Report pdf into trades and subsequently adds any trades not already on your Sharesight holdings to the respective holdings.

Requires usage of the Sharesight API and corresponding API details (Client ID, Client Secret). The script assumes authentication details are stored in a .env file:

```
CLIENT_ID=<your sharesight client id>
CLIENT_SECRET=<your sharesight client secret>
```

To run, install package dependencies with `pip install -r requirements.txt`. 

Authentication details for Share

## Assumptions

* The user only has one Sharesight Portfolio.
* Holdings on the users Investnow report already exist on their Sharesight Portfolio.
* The user is using Sharesight to do auto dividend reinvestments, so the script does not process these.
