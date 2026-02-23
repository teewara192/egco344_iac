from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

client = MongoClient("mongodb://mongodb:27017/")
db = client["electricity_db"]

# 1. Get available years for the dropdown
@app.get("/api/years")
def get_years():
    years = db.usages.distinct("year")
    return sorted(years, reverse=True)

# 2. Get aggregated stats for Charts (Bar/Pie)
@app.get("/api/stats/{year}")
def get_stats(year: int):
    # Summing all categories for the selected year
    pipeline = [
        {"$match": {"year": year}},
        {"$group": {
            "_id": "$year",
            "Residential": {"$sum": "$residential_kwh"},
            "Small Business": {"$sum": "$small_business_kwh"},
            "Medium Business": {"$sum": "$medium_business_kwh"},
            "Large Business": {"$sum": "$large_business_kwh"},
            "EV Charging": {"$sum": "$ev_charging_kwh"}
        }}
    ]
    usage = list(db.usages.aggregate(pipeline))

    user_pipeline = [
        {"$match": {"year": year}},
        {"$group": {
            "_id": "$year",
            "Residential": {"$sum": "$residential_count"},
            "Small Business": {"$sum": "$small_business_count"},
            "Medium Business": {"$sum": "$medium_business_count"}
            }}
    ]
    users = list(db.users.aggregate(user_pipeline))

    return {
        "usage": usage[0] if usage else {},
        "users": users[0] if users else {}
    }

# 3. Get raw data for the Table
@app.get("/api/table/{year}")
def get_table_data(year: int):
    data = list(db.usages.find({"year": year}, {"_id": 0}).limit(20))
    return data