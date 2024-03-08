import CSV
import DataFrame
using GeoJSON


# Read files
df_reviewDetailed = CSV.File("data/reviews_detailed.csv") |> DataFrame
df_review = CSV.File("data/reviews_detailed.csv") |> DataFrame
df_neighbourhoods = CSV.File("data/neighbourhoods.csv") |> DataFrame
df_neighbourhoodsGeo = DataFrame(GeoJSON.read("data/neighbourhoods.geojson"))
df_listings = CSV.File("data/listings.csv") |> DataFrame
df_listingsDetailed = CSV.File("data/listings_detailed.csv") |> DataFrame

# Show a little resume of each
function show_resume(df)
    pass
end;

resume_txt = ""