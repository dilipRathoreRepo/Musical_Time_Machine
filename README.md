# Musical_Time_Machine

1. This app asks a user for the date in YYYY-MM-DD format for which he wants to search the top 100 Billboard songs.
2. It then uses BeautifulSoup library to scrape the top 100 songs from https://www.billboard.com/charts/hot-100 and
create a list of these songs (str).
3. It will then authenticate with Spotify using client id and secret and will generate a token and fetch user id. 
4. It will then loop through the list of top 100 BillBoard songs from above and search the URI from spotify for each 
song.
5. It will then create a new Spotify playlist for these songs.
